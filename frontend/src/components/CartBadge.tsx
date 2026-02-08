import { useMemo, useState } from "react";
import { useCart } from "../cart/CartContext";

export function CartBadge({ onClick }: { onClick?: () => void }) {
  const { getCartItemsCount } = useCart();
  const count = getCartItemsCount();
  const [open, setOpen] = useState(false);

  return (
    <div
      style={{ position: "relative" }}
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
    >
      <a
        className="navLink"
        href="#cart"
        onClick={onClick}
        aria-label="Корзина"
      >
        🛒
        {count > 0 ? (
          <span
            style={{
              marginLeft: 6,
              display: "inline-block",
              minWidth: 18,
              height: 18,
              borderRadius: 9,
              padding: "0 6px",
              fontSize: 12,
              lineHeight: "18px",
              textAlign: "center",
              color: "#fff",
              background: "rgba(196, 151, 111, 0.9)",
            }}
          >
            {count}
          </span>
        ) : null}
      </a>
      {open ? <MiniCartPopover /> : null}
    </div>
  );
}

function MiniCartPopover() {
  const { state, getTotalPrice, updateQuantity, removeFromCart } = useCart();
  const total = useMemo(() => getTotalPrice(), [getTotalPrice, state.items]);
  return (
    <div
      style={{
        position: "absolute",
        top: "100%",
        right: 0,
        zIndex: 20,
        borderRadius: 12,
        border: "1px solid var(--border)",
        background: "var(--surface)",
        boxShadow: "var(--shadow)",
        padding: 12,
        minWidth: 280,
      }}
    >
      {state.items.length === 0 ? (
        <div style={{ fontSize: 13, color: "var(--muted)" }}>Корзина пуста</div>
      ) : (
        <>
          <div
            style={{
              display: "grid",
              gap: 10,
              maxHeight: 260,
              overflow: "auto",
            }}
          >
            {state.items.map((item) => (
              <div
                key={item.productVariantId}
                style={{
                  display: "grid",
                  gridTemplateColumns: "40px 1fr auto",
                  gap: 10,
                  alignItems: "center",
                }}
              >
                <div
                  style={{
                    width: 40,
                    height: 40,
                    borderRadius: 10,
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
                      style={{
                        width: "100%",
                        height: "100%",
                        objectFit: "cover",
                        display: "block",
                      }}
                    />
                  ) : (
                    <span style={{ fontSize: 11, color: "var(--muted)" }}>
                      Нет фото
                    </span>
                  )}
                </div>
                <div style={{ display: "grid", gap: 4, minWidth: 0 }}>
                  <div
                    style={{
                      fontSize: 13,
                      fontWeight: 600,
                      whiteSpace: "nowrap",
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                    }}
                  >
                    {item.productName}
                  </div>
                  <div style={{ fontSize: 12, color: "var(--muted)" }}>
                    {item.sizeName || ""}
                  </div>
                </div>
                <div style={{ display: "grid", gap: 6, justifyItems: "end" }}>
                  <div style={{ fontSize: 13, fontWeight: 600 }}>
                    {new Intl.NumberFormat("ru-RU").format(item.price)} ₽
                  </div>
                  <div
                    style={{ display: "flex", gap: 6, alignItems: "center" }}
                  >
                    <button
                      style={{ padding: "2px 8px" }}
                      onClick={() =>
                        updateQuantity(
                          item.productVariantId,
                          Math.max(1, item.quantity - 1),
                        )
                      }
                    >
                      −
                    </button>
                    <span
                      style={{
                        minWidth: 20,
                        textAlign: "center",
                        fontSize: 12,
                      }}
                    >
                      {item.quantity}
                    </span>
                    <button
                      style={{ padding: "2px 8px" }}
                      onClick={() =>
                        updateQuantity(item.productVariantId, item.quantity + 1)
                      }
                    >
                      +
                    </button>
                    <button
                      style={{
                        padding: "2px 8px",
                        background: "var(--surface-2)",
                      }}
                      onClick={() => removeFromCart(item.productVariantId)}
                    >
                      ✕
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <div
            style={{
              marginTop: 10,
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
            }}
          >
            <div style={{ fontSize: 13, color: "var(--muted)" }}>Итого</div>
            <div style={{ fontSize: 14, fontWeight: 700 }}>
              {new Intl.NumberFormat("ru-RU").format(total)} ₽
            </div>
          </div>
          <a
            href="#cart"
            style={{ marginTop: 10, display: "block", textAlign: "center" }}
          >
            <button
              style={{ width: "100%", borderRadius: 999, padding: "8px 12px" }}
            >
              Оформить заказ
            </button>
          </a>
        </>
      )}
    </div>
  );
}
