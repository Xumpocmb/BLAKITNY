import { memo, useMemo, useState } from "react";
import { useCart } from "../cart/CartContext";

type CartPageProps = {
  isAuthenticated: boolean;
  onCheckout?: () => void;
};

export function CartPage({ isAuthenticated, onCheckout }: CartPageProps) {
  const { state, getTotalPrice, updateQuantity, removeFromCart, clearCart } =
    useCart();
  const total = useMemo(() => getTotalPrice(), [getTotalPrice, state.items]);
  const [removing, setRemoving] = useState<number | null>(null);

  const handleRemove = async (id: number) => {
    setRemoving(id);
    setTimeout(async () => {
      await removeFromCart(id);
      setRemoving(null);
    }, 200);
  };

  return (
    <section style={{ display: "grid", gap: 18 }}>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          flexWrap: "wrap",
          gap: 12,
        }}
      >
        <div>
          <div style={{ fontSize: 24, fontWeight: 700 }}>Корзина</div>
          <div style={{ fontSize: 13, color: "var(--muted)" }}>
            {state.items.length > 0
              ? `Товаров: ${state.items.length}`
              : "Пока здесь пусто"}
          </div>
        </div>
        {state.items.length > 0 ? (
          <button
            style={{ borderRadius: 999, padding: "8px 14px" }}
            onClick={() => clearCart()}
          >
            Очистить
          </button>
        ) : null}
      </div>
      {state.error ? (
        <div
          style={{
            padding: 12,
            borderRadius: 12,
            background: "rgba(255, 107, 107, 0.12)",
            border: "1px solid rgba(255, 107, 107, 0.35)",
          }}
        >
          {state.error}
        </div>
      ) : null}
      {!isAuthenticated ? (
        <div
          style={{
            padding: 12,
            borderRadius: 12,
            background: "rgba(196, 151, 111, 0.12)",
            border: "1px solid rgba(196, 151, 111, 0.35)",
          }}
        >
          Для синхронизации корзины войдите в аккаунт
        </div>
      ) : null}
      {state.items.length === 0 ? (
        <div
          style={{
            padding: 18,
            borderRadius: 16,
            border: "1px dashed var(--border)",
            background: "var(--surface-2)",
            color: "var(--muted)",
          }}
        >
          Добавьте товары из каталога, чтобы оформить заказ
        </div>
      ) : (
        <div style={{ display: "grid", gap: 12 }}>
          {state.items.map((item) => (
            <CartRow
              key={item.productVariantId}
              item={item}
              removing={removing === item.productVariantId}
              onRemove={() => handleRemove(item.productVariantId)}
              onDecrease={() =>
                updateQuantity(
                  item.productVariantId,
                  Math.max(1, item.quantity - 1),
                )
              }
              onIncrease={() =>
                updateQuantity(item.productVariantId, item.quantity + 1)
              }
            />
          ))}
        </div>
      )}
      {state.items.length > 0 ? (
        <div
          style={{
            display: "grid",
            gap: 12,
            padding: 16,
            borderRadius: 16,
            border: "1px solid var(--border)",
            background: "var(--surface)",
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
            }}
          >
            <div style={{ color: "var(--muted)" }}>Промежуточный итог</div>
            <div style={{ fontWeight: 700, fontSize: 18 }}>
              {new Intl.NumberFormat("ru-RU").format(total)} ₽
            </div>
          </div>
          <button
            style={{
              borderRadius: 999,
              padding: "10px 16px",
              background: "var(--accent)",
              color: "#fff",
            }}
            onClick={onCheckout}
          >
            Оформить заказ
          </button>
        </div>
      ) : null}
    </section>
  );
}

const CartRow = memo(function CartRow({
  item,
  removing,
  onRemove,
  onDecrease,
  onIncrease,
}: {
  item: {
    productName: string;
    productImage?: string | null;
    sizeName?: string | null;
    quantity: number;
    price: number;
  };
  removing: boolean;
  onRemove: () => void;
  onDecrease: () => void;
  onIncrease: () => void;
}) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "90px 1fr auto",
        gap: 16,
        alignItems: "center",
        padding: 12,
        borderRadius: 16,
        border: "1px solid var(--border)",
        background: "var(--surface)",
        transition: "transform 0.2s ease, opacity 0.2s ease",
        transform: removing ? "scale(0.98)" : "scale(1)",
        opacity: removing ? 0.4 : 1,
      }}
    >
      <div
        style={{
          width: 90,
          height: 90,
          borderRadius: 12,
          overflow: "hidden",
          border: "1px solid var(--border)",
          background: "var(--surface-2)",
          display: "grid",
          placeItems: "center",
        }}
      >
        {item.productImage ? (
          <img
            src={item.productImage}
            alt={item.productName}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        ) : (
          <span style={{ fontSize: 12, color: "var(--muted)" }}>Нет фото</span>
        )}
      </div>
      <div style={{ display: "grid", gap: 6 }}>
        <div style={{ fontSize: 16, fontWeight: 600 }}>{item.productName}</div>
        <div style={{ fontSize: 13, color: "var(--muted)" }}>
          {item.sizeName || ""}
        </div>
        <div style={{ fontSize: 14, fontWeight: 600 }}>
          {new Intl.NumberFormat("ru-RU").format(item.price)} ₽
        </div>
      </div>
      <div style={{ display: "grid", gap: 8, justifyItems: "end" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <button onClick={onDecrease}>−</button>
          <span style={{ minWidth: 24, textAlign: "center" }}>
            {item.quantity}
          </span>
          <button onClick={onIncrease}>+</button>
        </div>
        <button style={{ background: "var(--surface-2)" }} onClick={onRemove}>
          Удалить
        </button>
      </div>
    </div>
  );
});
