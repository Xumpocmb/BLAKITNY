export type CartItem = {
  id?: number;
  productId: number;
  productName: string;
  productImage?: string | null;
  productVariantId: number;
  sizeName?: string | null;
  price: number;
  quantity: number;
  availableStock?: number | null;
  attributes?: Record<string, string | number | boolean | null> | null;
};

export type CartState = {
  items: CartItem[];
  error?: string | null;
};

export type CartContextValue = {
  state: CartState;
  addToCart: (
    item: Omit<CartItem, "id" | "quantity">,
    quantity?: number,
  ) => Promise<void>;
  removeFromCart: (productVariantId: number) => Promise<void>;
  updateQuantity: (
    productVariantId: number,
    newQuantity: number,
  ) => Promise<void>;
  clearCart: () => Promise<void>;
  getTotalPrice: () => number;
  getCartItemsCount: () => number;
  reloadFromServer: () => Promise<void>;
};
