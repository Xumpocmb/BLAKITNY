import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import type { CartContextValue, CartItem, CartState } from "./types";
const ACCESS_TOKEN_KEY = "blakitny_access_token";
function readAccessToken() {
  try {
    const access = localStorage.getItem(ACCESS_TOKEN_KEY);
    return access || null;
  } catch {
    return null;
  }
}

function toProxiedUrl(url: string | null | undefined) {
  if (!url) return url ?? null;
  try {
    const u = new URL(url);
    if (
      u.origin === "http://127.0.0.1:8000" ||
      u.origin === "http://localhost:8000"
    ) {
      return `${u.pathname}${u.search}${u.hash}`;
    }
    return url;
  } catch {
    return url;
  }
}

export const CartContext = createContext<CartContextValue | null>(null);

export function useCart() {
  const ctx = useContext(CartContext);
  if (!ctx) {
    throw new Error("CartContext is missing");
  }
  return ctx;
}

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<CartState>({ items: [], error: null });
  const loadingRef = useRef(false);
  const productCacheRef = useRef<
    Map<
      number,
      {
        name: string;
        image?: string | null;
        attributes?: CartItem["attributes"];
      }
    >
  >(new Map());

  const getTotalPrice = useCallback(() => {
    return state.items.reduce(
      (sum, item) => sum + item.price * item.quantity,
      0,
    );
  }, [state.items]);

  const getCartItemsCount = useCallback(() => {
    return state.items.reduce((sum, item) => sum + item.quantity, 0);
  }, [state.items]);

  const reloadFromServer = useCallback(async () => {
    const token = readAccessToken();
    if (!token) {
      setState({ items: [], error: null });
      return;
    }
    if (loadingRef.current) return;
    loadingRef.current = true;
    try {
      const res = await fetch("/api/cart/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) return;
      const data = await res.json();
      const serverItems: any[] = Array.isArray(data?.items) ? data.items : [];
      const productIds = serverItems
        .map((ci) => Number(ci?.product_variant?.product ?? 0))
        .filter((id) => Number.isFinite(id) && id > 0);
      const uniqueIds = Array.from(new Set(productIds));
      const missing = uniqueIds.filter(
        (id) => !productCacheRef.current.has(id),
      );
      if (missing.length > 0) {
        await Promise.all(
          missing.map(async (id) => {
            const productRes = await fetch(`/api/catalog/products/${id}/`);
            if (!productRes.ok) return;
            const product = await productRes.json();
            const images: Array<{ image?: string; is_active?: boolean }> =
              Array.isArray(product?.images) ? product.images : [];
            const activeImage = images.find((img) => img?.is_active !== false);
            productCacheRef.current.set(id, {
              name: String(product?.name ?? ""),
              image: toProxiedUrl(activeImage?.image),
              attributes: {
                binding: product?.binding ?? null,
                pictureTitle: product?.picture_title ?? null,
                fabric: product?.fabric_type?.name ?? null,
                category: product?.category?.name ?? null,
                subcategory: product?.subcategory?.name ?? null,
              },
            });
          }),
        );
      }
      const items: CartItem[] = serverItems.map((ci) => {
        const productId = Number(ci?.product_variant?.product ?? 0);
        const cached = productCacheRef.current.get(productId);
        return {
          id: ci?.id,
          productId,
          productName: cached?.name || "Товар",
          productImage: cached?.image ?? null,
          productVariantId: Number(ci?.product_variant?.id ?? 0),
          sizeName: String(ci?.product_variant?.size?.name ?? ""),
          price: Number(ci?.product_variant?.price ?? 0),
          quantity: Number(ci?.quantity ?? 1),
          attributes: cached?.attributes ?? null,
        };
      });
      setState({ items, error: null });
    } finally {
      loadingRef.current = false;
    }
  }, []);

  useEffect(() => {
    reloadFromServer();
  }, [reloadFromServer]);

  const addToCart = useCallback(
    async (item: Omit<CartItem, "id" | "quantity">, quantity: number = 1) => {
      if (quantity < 1) quantity = 1;
      if (
        typeof item.availableStock === "number" &&
        quantity > item.availableStock
      ) {
        setState((prev) => ({
          ...prev,
          error: "Недостаточно товара на складе",
        }));
        return;
      }
      const token = readAccessToken();
      if (!token) {
        setState((prev) => ({ ...prev, error: "Требуется авторизация" }));
        return;
      }
      try {
        const res = await fetch("/api/cart/add/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            product_variant_id: item.productVariantId,
            quantity,
          }),
        });
        if (!res.ok) {
          setState((prev) => ({
            ...prev,
            error: "Ошибка при добавлении товара",
          }));
          return;
        }
        await reloadFromServer();
      } catch {
        setState((prev) => ({
          ...prev,
          error: "Ошибка при добавлении товара",
        }));
      }
    },
    [reloadFromServer],
  );

  const removeFromCart = useCallback(
    async (productVariantId: number) => {
      const token = readAccessToken();
      const item = state.items.find(
        (i) => i.productVariantId === productVariantId,
      );
      if (!token) {
        setState((prev) => ({ ...prev, error: "Требуется авторизация" }));
        return;
      }
      if (!item?.id) {
        await reloadFromServer();
        return;
      }
      try {
        const res = await fetch(`/api/cart/remove/${item.id}/`, {
          method: "DELETE",
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) return;
        await reloadFromServer();
      } catch {
        return;
      }
    },
    [state.items, reloadFromServer],
  );

  const updateQuantity = useCallback(
    async (productVariantId: number, newQuantity: number) => {
      if (newQuantity < 1) {
        await removeFromCart(productVariantId);
        return;
      }
      const capped = Math.min(99, newQuantity);
      const token = readAccessToken();
      const item = state.items.find(
        (i) => i.productVariantId === productVariantId,
      );
      if (!token) {
        setState((prev) => ({ ...prev, error: "Требуется авторизация" }));
        return;
      }
      if (!item?.id) {
        await reloadFromServer();
        return;
      }
      try {
        const res = await fetch(`/api/cart/update/${item.id}/`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ quantity: capped }),
        });
        if (!res.ok) return;
        await reloadFromServer();
      } catch {
        return;
      }
    },
    [state.items, removeFromCart, reloadFromServer],
  );

  const clearCart = useCallback(async () => {
    const token = readAccessToken();
    if (!token) {
      setState((prev) => ({ ...prev, error: "Требуется авторизация" }));
      return;
    }
    try {
      await fetch("/api/cart/clear/", {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      await reloadFromServer();
    } catch {
      return;
    }
  }, [reloadFromServer]);

  const value = useMemo<CartContextValue>(
    () => ({
      state,
      addToCart,
      removeFromCart,
      updateQuantity,
      clearCart,
      getTotalPrice,
      getCartItemsCount,
      reloadFromServer,
    }),
    [
      state,
      addToCart,
      removeFromCart,
      updateQuantity,
      clearCart,
      getTotalPrice,
      getCartItemsCount,
      reloadFromServer,
    ],
  );

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}
