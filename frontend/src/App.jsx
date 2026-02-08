import "./App.css";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { AboutSection } from "./components/AboutSection";
import { DeliveryPaymentSection } from "./components/DeliveryPaymentSection";
import { ContactsSection } from "./components/ContactsSection";
import { CategoriesSection } from "./components/CategoriesSection";
import { CartBadge } from "./components/CartBadge";
import { CartPage } from "./components/CartPage";
import { useCart } from "./cart/CartContext";

const THEMES = {
  cream: {
    "--bg": "#fbf7f0",
    "--surface": "#ffffff",
    "--surface-2": "#f6efe4",
    "--text": "#1f2328",
    "--muted": "#6b6f76",
    "--border": "rgba(31, 35, 40, 0.12)",
    "--accent": "#c4976f",
    "--accent-2": "#e3c6aa",
    "--shadow": "0 18px 40px rgba(31, 35, 40, 0.08)",
  },
  vanilla: {
    "--bg": "#fcf8f2",
    "--surface": "#ffffff",
    "--surface-2": "#f3eadc",
    "--text": "#1c1f24",
    "--muted": "#6a6f77",
    "--border": "rgba(28, 31, 36, 0.12)",
    "--accent": "#b78962",
    "--accent-2": "#ead4be",
    "--shadow": "0 18px 40px rgba(28, 31, 36, 0.08)",
  },
};

function applyTheme(theme) {
  const root = document.documentElement;
  for (const [key, value] of Object.entries(theme)) {
    root.style.setProperty(key, value);
  }
}

function toProxiedUrl(url) {
  if (typeof url !== "string" || url.length === 0) return url;
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

function preloadImages(urls, signal) {
  const tasks = urls.map((url) => {
    return new Promise((resolve) => {
      if (signal?.aborted) return resolve();
      const img = new Image();
      img.onload = () => resolve();
      img.onerror = () => resolve();
      img.src = url;
    });
  });
  return Promise.all(tasks).then(() => undefined);
}

function pause(ms, signal) {
  return new Promise((resolve) => {
    if (signal?.aborted) return resolve();
    const id = window.setTimeout(() => {
      if (signal) signal.removeEventListener("abort", onAbort);
      resolve();
    }, ms);
    const onAbort = () => {
      window.clearTimeout(id);
      if (signal) signal.removeEventListener("abort", onAbort);
      resolve();
    };
    if (signal) signal.addEventListener("abort", onAbort, { once: true });
  });
}

function formatPrice(value) {
  if (!Number.isFinite(value)) return "";
  return new Intl.NumberFormat("ru-RU").format(value);
}

function parsePrice(value) {
  if (typeof value !== "string") return null;
  const normalized = value.replace(",", ".").trim();
  if (!normalized) return null;
  const num = Number(normalized);
  return Number.isFinite(num) ? num : null;
}

function getActiveImages(product) {
  const images = Array.isArray(product?.images) ? product.images : [];
  return images.filter((img) => img && img.is_active !== false);
}

function getPriceRange(product) {
  const variants = Array.isArray(product?.variants) ? product.variants : [];
  const prices = variants
    .filter((variant) => variant && variant.is_active !== false)
    .map((variant) => Number(variant?.price))
    .filter((price) => Number.isFinite(price));
  if (prices.length === 0) return null;
  return {
    min: Math.min(...prices),
    max: Math.max(...prices),
  };
}

const ACCESS_TOKEN_KEY = "blakitny_access_token";
const REFRESH_TOKEN_KEY = "blakitny_refresh_token";

function readStoredTokens() {
  try {
    const access = localStorage.getItem(ACCESS_TOKEN_KEY);
    const refresh = localStorage.getItem(REFRESH_TOKEN_KEY);
    if (!access || !refresh) return null;
    return { access, refresh };
  } catch {
    return null;
  }
}

function readAccessToken() {
  try {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  } catch {
    return null;
  }
}

function storeTokens(tokens) {
  try {
    if (tokens?.access) localStorage.setItem(ACCESS_TOKEN_KEY, tokens.access);
    if (tokens?.refresh)
      localStorage.setItem(REFRESH_TOKEN_KEY, tokens.refresh);
  } catch {
    return;
  }
}

function clearTokens() {
  try {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
  } catch {
    return;
  }
}

function normalizeError(data, fallback) {
  if (!data) return fallback;
  if (typeof data === "string") return data;
  if (typeof data?.detail === "string") return data.detail;
  if (Array.isArray(data?.non_field_errors) && data.non_field_errors[0]) {
    return data.non_field_errors[0];
  }
  if (Array.isArray(data?.email) && data.email[0]) return data.email[0];
  if (Array.isArray(data?.password) && data.password[0])
    return data.password[0];
  if (Array.isArray(data?.password_confirm) && data.password_confirm[0]) {
    return data.password_confirm[0];
  }
  return fallback;
}

function HeroSlider({ slides, error }) {
  const [activeIndex, setActiveIndex] = useState(0);

  const canSlide = slides.length > 1;

  useEffect(() => {
    if (!canSlide) return;
    const id = window.setInterval(() => {
      setActiveIndex((i) => (i + 1) % slides.length);
    }, 6500);
    return () => window.clearInterval(id);
  }, [canSlide, slides.length]);

  const trackStyle = useMemo(() => {
    return { transform: `translateX(-${activeIndex * 100}%)` };
  }, [activeIndex]);

  const goPrev = () => {
    if (!canSlide) return;
    setActiveIndex((i) => (i - 1 + slides.length) % slides.length);
  };

  const goNext = () => {
    if (!canSlide) return;
    setActiveIndex((i) => (i + 1) % slides.length);
  };

  return (
    <div className="slider" aria-label="Слайдер">
      {error ? (
        <div className="slidePlaceholder">
          Не удалось загрузить слайдер: {error}
        </div>
      ) : slides.length === 0 ? (
        <div className="slidePlaceholder">Слайдер пока пуст</div>
      ) : (
        <>
          <div className="sliderTrack" style={trackStyle}>
            {slides.map((s) => (
              <div className="slide" key={s.id}>
                <img
                  className="slideMedia"
                  src={toProxiedUrl(s.image_url)}
                  alt={s.alt_text || "Слайд"}
                />
              </div>
            ))}
          </div>
          <div className="sliderOverlay" />
          <div className="sliderControls">
            <div className="dots" aria-label="Навигация по слайдам">
              {slides.map((s, idx) => (
                <button
                  key={s.id}
                  type="button"
                  className={idx === activeIndex ? "dot dotActive" : "dot"}
                  onClick={() => setActiveIndex(idx)}
                  aria-label={`Слайд ${idx + 1}`}
                />
              ))}
            </div>
            <div className="arrowGroup">
              <button
                type="button"
                className="arrowBtn"
                onClick={goPrev}
                aria-label="Предыдущий слайд"
              >
                ←
              </button>
              <button
                type="button"
                className="arrowBtn"
                onClick={goNext}
                aria-label="Следующий слайд"
              >
                →
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

function ProfileMenu({
  isAuthenticated,
  userEmail,
  onLogin,
  onRegister,
  onProfile,
  onLogout,
}) {
  const rootRef = useRef(null);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onMouseDown = (e) => {
      if (!rootRef.current) return;
      if (!(e.target instanceof Node)) return;
      if (!rootRef.current.contains(e.target)) setOpen(false);
    };
    const onKeyDown = (e) => {
      if (e.key === "Escape") setOpen(false);
    };

    document.addEventListener("mousedown", onMouseDown);
    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("mousedown", onMouseDown);
      document.removeEventListener("keydown", onKeyDown);
    };
  }, []);

  const handleLoginClick = () => {
    onLogin?.();
    setOpen(false);
  };

  const handleRegisterClick = () => {
    onRegister?.();
    setOpen(false);
  };

  const handleProfileClick = () => {
    onProfile?.();
    setOpen(false);
  };

  const handleLogoutClick = () => {
    onLogout?.();
    setOpen(false);
  };

  return (
    <div className="profileMenuWrap" ref={rootRef}>
      <button
        type="button"
        className="profileBtn"
        aria-label="Профиль"
        aria-haspopup="menu"
        aria-expanded={open}
        onClick={() => setOpen((v) => !v)}
      >
        <svg
          className="profileIcon"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          aria-hidden="true"
        >
          <path
            d="M20 21a8 8 0 0 0-16 0"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
          />
          <path
            d="M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </button>
      {open ? (
        <div className="profileDropdown" role="menu" aria-label="Меню профиля">
          {isAuthenticated ? (
            <>
              {userEmail ? <div className="menuInfo">{userEmail}</div> : null}
              <button
                type="button"
                className="menuItem"
                role="menuitem"
                onClick={handleProfileClick}
              >
                Профиль
              </button>
              <button
                type="button"
                className="menuItem"
                role="menuitem"
                onClick={handleLogoutClick}
              >
                Выход
              </button>
            </>
          ) : (
            <>
              <button
                type="button"
                className="menuItem"
                role="menuitem"
                onClick={handleLoginClick}
              >
                Вход
              </button>
              <button
                type="button"
                className="menuItem"
                role="menuitem"
                onClick={handleRegisterClick}
              >
                Регистрация
              </button>
            </>
          )}
        </div>
      ) : null}
    </div>
  );
}

function AuthModal({ open, mode, onClose, onLogin, onRegister, onSwitch }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!open) return;
    setEmail("");
    setPassword("");
    setPasswordConfirm("");
    setError("");
    setSubmitting(false);
  }, [open, mode]);

  if (!open) return null;

  const isRegister = mode === "register";

  const submit = async (event) => {
    event.preventDefault();
    if (submitting) return;
    setSubmitting(true);
    setError("");
    try {
      if (isRegister) {
        await onRegister?.({ email, password, passwordConfirm });
      } else {
        await onLogin?.({ email, password });
      }
      onClose?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка авторизации");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="authOverlay" role="dialog" aria-modal="true">
      <div className="authModal">
        <div className="authHeader">
          <div className="authTitle">{isRegister ? "Регистрация" : "Вход"}</div>
          <button
            type="button"
            className="authClose"
            aria-label="Закрыть"
            onClick={onClose}
          >
            ✕
          </button>
        </div>
        <div className="authTabs" role="tablist">
          <button
            type="button"
            className={`authTab ${!isRegister ? "authTabActive" : ""}`}
            role="tab"
            aria-selected={!isRegister}
            onClick={() => onSwitch?.("login")}
          >
            Вход
          </button>
          <button
            type="button"
            className={`authTab ${isRegister ? "authTabActive" : ""}`}
            role="tab"
            aria-selected={isRegister}
            onClick={() => onSwitch?.("register")}
          >
            Регистрация
          </button>
        </div>
        <form className="authForm" onSubmit={submit}>
          <label className="authField">
            <span>Email</span>
            <input
              className="authInput"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
              placeholder="name@email.com"
            />
          </label>
          <label className="authField">
            <span>Пароль</span>
            <input
              className="authInput"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={8}
              autoComplete={isRegister ? "new-password" : "current-password"}
              placeholder="Минимум 8 символов"
            />
          </label>
          {isRegister ? (
            <label className="authField">
              <span>Повторите пароль</span>
              <input
                className="authInput"
                type="password"
                value={passwordConfirm}
                onChange={(e) => setPasswordConfirm(e.target.value)}
                required
                minLength={8}
                autoComplete="new-password"
                placeholder="Повтор пароля"
              />
            </label>
          ) : null}
          {error ? <div className="authError">{error}</div> : null}
          <div className="authActions">
            <button type="submit" disabled={submitting}>
              {submitting
                ? "Отправляем..."
                : isRegister
                  ? "Создать аккаунт"
                  : "Войти"}
            </button>
            <button type="button" className="authGhost" onClick={onClose}>
              Отмена
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function ImageModal({ images, activeIndex, onClose, onPrev, onNext }) {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === "Escape") onClose();
      if (e.key === "ArrowLeft") onPrev();
      if (e.key === "ArrowRight") onNext();
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [onClose, onPrev, onNext]);

  if (!images || images.length === 0) return null;

  const currentImage = images[activeIndex];

  return (
    <div className="imageModalOverlay" onClick={onClose}>
      <div className="imageModalContent" onClick={(e) => e.stopPropagation()}>
        <button className="imageModalClose" onClick={onClose}>
          ✕
        </button>
        <button className="imageModalNav prev" onClick={onPrev}>
          ←
        </button>
        <div className="imageModalImageWrapper">
          <img
            src={toProxiedUrl(currentImage?.image)}
            alt="Просмотр"
            className="imageModalImage"
          />
        </div>
        <button className="imageModalNav next" onClick={onNext}>
          →
        </button>
        <div className="imageModalCounter">
          {activeIndex + 1} / {images.length}
        </div>
      </div>
    </div>
  );
}

function CheckoutPage({ isAuthenticated, userEmail, onBack, onOrderCreated }) {
  const { state, getTotalPrice, reloadFromServer } = useCart();
  const total = useMemo(() => getTotalPrice(), [getTotalPrice]);
  const [deliveryOptions, setDeliveryOptions] = useState([]);
  const [loadingOptions, setLoadingOptions] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    firstName: "",
    lastName: "",
    email: userEmail || "",
    phone: "",
    address: "",
    deliveryOptionId: "",
  });

  useEffect(() => {
    if (!userEmail) return;
    setForm((prev) => ({ ...prev, email: prev.email || userEmail }));
  }, [userEmail]);

  useEffect(() => {
    let active = true;
    setLoadingOptions(true);
    fetch("/api/delivery-options/")
      .then((res) => res.json())
      .then((data) => {
        if (!active) return;
        const list = Array.isArray(data?.delivery_options)
          ? data.delivery_options
          : [];
        setDeliveryOptions(list);
        if (list.length > 0) {
          setForm((prev) =>
            prev.deliveryOptionId
              ? prev
              : { ...prev, deliveryOptionId: String(list[0].id) },
          );
        }
      })
      .catch(() => {
        if (!active) return;
        setDeliveryOptions([]);
      })
      .finally(() => {
        if (!active) return;
        setLoadingOptions(false);
      });
    return () => {
      active = false;
    };
  }, []);

  const handleChange = (field) => (event) => {
    setForm((prev) => ({ ...prev, [field]: event.target.value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (submitting) return;
    if (!isAuthenticated) {
      setError("Требуется авторизация");
      return;
    }
    if (state.items.length === 0) {
      setError("Корзина пуста");
      return;
    }
    if (!form.deliveryOptionId) {
      setError("Выберите способ доставки");
      return;
    }
    const token = readAccessToken();
    if (!token) {
      setError("Требуется авторизация");
      return;
    }
    setSubmitting(true);
    setError("");
    try {
      const res = await fetch("/api/orders/create/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          delivery_option_id: Number(form.deliveryOptionId),
          first_name: form.firstName,
          last_name: form.lastName,
          email: form.email,
          phone: form.phone,
          address: form.address,
        }),
      });
      const data = await res.json().catch(() => null);
      if (!res.ok) {
        setError(normalizeError(data, "Не удалось оформить заказ"));
        return;
      }
      await reloadFromServer();
      onOrderCreated?.(data);
    } catch {
      setError("Не удалось оформить заказ");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <section style={{ display: "grid", gap: 18 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <button type="button" onClick={onBack}>
          Назад в корзину
        </button>
        <div style={{ fontSize: 24, fontWeight: 700 }}>Оформление заказа</div>
      </div>
      {error ? (
        <div
          style={{
            padding: 12,
            borderRadius: 12,
            background: "rgba(255, 107, 107, 0.12)",
            border: "1px solid rgba(255, 107, 107, 0.35)",
          }}
        >
          {error}
        </div>
      ) : null}
      <div
        style={{
          display: "grid",
          gap: 16,
          gridTemplateColumns: "minmax(0, 1.2fr) minmax(0, 1fr)",
        }}
      >
        <form
          onSubmit={handleSubmit}
          style={{
            display: "grid",
            gap: 12,
            padding: 16,
            borderRadius: 16,
            border: "1px solid var(--border)",
            background: "var(--surface)",
          }}
        >
          <div style={{ fontWeight: 600, fontSize: 18 }}>Данные получателя</div>
          <label style={{ display: "grid", gap: 6 }}>
            <span style={{ fontSize: 13, color: "var(--muted)" }}>Имя</span>
            <input
              required
              value={form.firstName}
              onChange={handleChange("firstName")}
              className="authInput"
            />
          </label>
          <label style={{ display: "grid", gap: 6 }}>
            <span style={{ fontSize: 13, color: "var(--muted)" }}>Фамилия</span>
            <input
              required
              value={form.lastName}
              onChange={handleChange("lastName")}
              className="authInput"
            />
          </label>
          <label style={{ display: "grid", gap: 6 }}>
            <span style={{ fontSize: 13, color: "var(--muted)" }}>Email</span>
            <input
              type="email"
              required
              value={form.email}
              onChange={handleChange("email")}
              className="authInput"
            />
          </label>
          <label style={{ display: "grid", gap: 6 }}>
            <span style={{ fontSize: 13, color: "var(--muted)" }}>Телефон</span>
            <input
              required
              value={form.phone}
              onChange={handleChange("phone")}
              className="authInput"
            />
          </label>
          <label style={{ display: "grid", gap: 6 }}>
            <span style={{ fontSize: 13, color: "var(--muted)" }}>
              Адрес доставки
            </span>
            <textarea
              required
              value={form.address}
              onChange={handleChange("address")}
              className="authInput"
              rows={3}
              style={{ resize: "vertical" }}
            />
          </label>
          <label style={{ display: "grid", gap: 6 }}>
            <span style={{ fontSize: 13, color: "var(--muted)" }}>
              Вариант доставки
            </span>
            <select
              required
              value={form.deliveryOptionId}
              onChange={handleChange("deliveryOptionId")}
              className="authInput"
              disabled={loadingOptions || deliveryOptions.length === 0}
            >
              {deliveryOptions.length === 0 ? (
                <option value="">
                  {loadingOptions
                    ? "Загрузка вариантов доставки..."
                    : "Нет доступных вариантов"}
                </option>
              ) : null}
              {deliveryOptions.map((option) => (
                <option key={option.id} value={String(option.id)}>
                  {option.name}
                </option>
              ))}
            </select>
          </label>
          <button
            type="submit"
            disabled={submitting}
            style={{
              borderRadius: 999,
              padding: "10px 16px",
              background: "var(--accent)",
              color: "#fff",
            }}
          >
            {submitting ? "Оформляем..." : "Подтвердить заказ"}
          </button>
        </form>
        <div
          style={{
            display: "grid",
            gap: 12,
            padding: 16,
            borderRadius: 16,
            border: "1px solid var(--border)",
            background: "var(--surface)",
            alignContent: "start",
          }}
        >
          <div style={{ fontWeight: 600, fontSize: 18 }}>Состав заказа</div>
          {state.items.length === 0 ? (
            <div style={{ color: "var(--muted)", fontSize: 13 }}>
              В корзине нет товаров
            </div>
          ) : (
            state.items.map((item) => (
              <div
                key={item.productVariantId}
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr auto",
                  gap: 8,
                  paddingBottom: 8,
                  borderBottom: "1px dashed var(--border)",
                }}
              >
                <div style={{ fontSize: 14 }}>
                  <div style={{ fontWeight: 600 }}>{item.productName}</div>
                  <div style={{ color: "var(--muted)", fontSize: 12 }}>
                    Размер: {item.sizeName || "—"} · Кол-во: {item.quantity}
                  </div>
                </div>
                <div style={{ fontWeight: 600 }}>
                  {new Intl.NumberFormat("ru-RU").format(
                    item.price * item.quantity,
                  )}{" "}
                  ₽
                </div>
              </div>
            ))
          )}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              fontWeight: 700,
            }}
          >
            <span>Итого</span>
            <span>{new Intl.NumberFormat("ru-RU").format(total)} ₽</span>
          </div>
        </div>
      </div>
    </section>
  );
}

function ProfilePage({ isAuthenticated, userEmail }) {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const accessToken = isAuthenticated ? readAccessToken() : null;
  const authError =
    isAuthenticated && !accessToken ? "Требуется авторизация" : "";

  useEffect(() => {
    if (!isAuthenticated) return;
    if (!accessToken) return;
    let active = true;
    fetch("/api/orders/", {
      headers: { Authorization: `Bearer ${accessToken}` },
    })
      .then((res) => res.json())
      .then((data) => {
        if (!active) return;
        const list = Array.isArray(data)
          ? data
          : Array.isArray(data?.results)
            ? data.results
            : [];
        setOrders(list);
      })
      .catch(() => {
        if (!active) return;
        setError("Не удалось загрузить заказы");
      })
      .finally(() => {
        if (!active) return;
        setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [isAuthenticated, accessToken]);

  const statusLabel = (status) => {
    const map = {
      pending: "В ожидании",
      confirmed: "Подтвержден",
      processing: "В обработке",
      shipped: "Отправлен",
      delivered: "Доставлен",
      cancelled: "Отменен",
    };
    return map[status] || status || "—";
  };

  return (
    <section style={{ display: "grid", gap: 18 }}>
      <div style={{ fontSize: 24, fontWeight: 700 }}>Профиль</div>
      {userEmail ? (
        <div style={{ color: "var(--muted)" }}>{userEmail}</div>
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
          Для просмотра профиля войдите в аккаунт
        </div>
      ) : authError ? (
        <div
          style={{
            padding: 12,
            borderRadius: 12,
            background: "rgba(255, 107, 107, 0.12)",
            border: "1px solid rgba(255, 107, 107, 0.35)",
          }}
        >
          {authError}
        </div>
      ) : error ? (
        <div
          style={{
            padding: 12,
            borderRadius: 12,
            background: "rgba(255, 107, 107, 0.12)",
            border: "1px solid rgba(255, 107, 107, 0.35)",
          }}
        >
          {error}
        </div>
      ) : loading ? (
        <div style={{ color: "var(--muted)" }}>Загрузка заказов...</div>
      ) : orders.length === 0 ? (
        <div style={{ color: "var(--muted)" }}>Заказов пока нет</div>
      ) : (
        <div style={{ display: "grid", gap: 12 }}>
          {orders.map((order) => (
            <div
              key={order.id}
              style={{
                display: "grid",
                gap: 10,
                padding: 16,
                borderRadius: 16,
                border: "1px solid var(--border)",
                background: "var(--surface)",
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  gap: 12,
                  flexWrap: "wrap",
                }}
              >
                <div style={{ fontWeight: 700 }}>Заказ #{order.id ?? "—"}</div>
                <div style={{ color: "var(--muted)" }}>
                  {statusLabel(order.status)}
                </div>
              </div>
              <div style={{ fontSize: 13, color: "var(--muted)" }}>
                Дата:{" "}
                {order.created_at
                  ? new Date(order.created_at).toLocaleString("ru-RU")
                  : "—"}
              </div>
              <div style={{ fontSize: 13, color: "var(--muted)" }}>
                Доставка: {order.delivery_option ?? "—"}
              </div>
              <div style={{ display: "grid", gap: 6 }}>
                {(order.order_items || []).map((item) => (
                  <div
                    key={item.id}
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      gap: 8,
                      fontSize: 13,
                    }}
                  >
                    <div>
                      Вариант #{item?.product_variant?.id ?? "—"} ·{" "}
                      {item?.product_variant?.product
                        ? `Товар #${item.product_variant.product}`
                        : "Товар"}
                      {item?.product_variant?.size?.name
                        ? ` · ${item.product_variant.size.name}`
                        : ""}
                      {item?.quantity ? ` · ${item.quantity} шт` : ""}
                    </div>
                    <div style={{ fontWeight: 600 }}>
                      {new Intl.NumberFormat("ru-RU").format(
                        Number(item?.total_price ?? 0),
                      )}{" "}
                      ₽
                    </div>
                  </div>
                ))}
              </div>
              <div style={{ fontWeight: 700 }}>
                Итого:{" "}
                {new Intl.NumberFormat("ru-RU").format(
                  Number(order.total_amount ?? 0),
                )}{" "}
                ₽
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

function App() {
  const { addToCart, reloadFromServer } = useCart();
  const [themeName] = useState("cream");
  const phone = "+79990000000";
  const [pageReady, setPageReady] = useState(false);
  const [sliderSlides, setSliderSlides] = useState([]);
  const [sliderError, setSliderError] = useState(null);
  const [siteLogo, setSiteLogo] = useState({ type: "text", value: "BLAKITNY" });
  const [companyDetails, setCompanyDetails] = useState(null);
  const [aboutUsData, setAboutUsData] = useState(null);
  const [deliveryData, setDeliveryData] = useState(null);
  const [socialNetworks, setSocialNetworks] = useState([]);
  const [categories, setCategories] = useState([]);
  const [authUser, setAuthUser] = useState(null);
  const [authModalOpen, setAuthModalOpen] = useState(false);
  const [authMode, setAuthMode] = useState("login");
  const [catalogProducts, setCatalogProducts] = useState([]);
  const [sizes, setSizes] = useState([]);
  const [fabrics, setFabrics] = useState([]);
  const [selectedSizes, setSelectedSizes] = useState([]);
  const [selectedFabrics, setSelectedFabrics] = useState([]);
  const [priceFrom, setPriceFrom] = useState("");
  const [priceTo, setPriceTo] = useState("");
  const [sortMode, setSortMode] = useState("newest");
  const [activeProductId, setActiveProductId] = useState(null);
  const [activeImageIndex, setActiveImageIndex] = useState(0);
  const [selectedVariantId, setSelectedVariantId] = useState(null);
  const [addQuantity, setAddQuantity] = useState(1);
  const [viewMode, setViewMode] = useState("home");
  const [modalOpen, setModalOpen] = useState(false);
  const sliderKey = useMemo(
    () => sliderSlides.map((s) => s.id).join("-"),
    [sliderSlides],
  );
  const activeProduct = useMemo(() => {
    return (
      catalogProducts.find((product) => product.id === activeProductId) || null
    );
  }, [catalogProducts, activeProductId]);
  const activeProductImages = useMemo(() => {
    return activeProduct ? getActiveImages(activeProduct) : [];
  }, [activeProduct]);
  const filteredProducts = useMemo(() => {
    const sizeSet = new Set(selectedSizes.map((id) => String(id)));
    const fabricSet = new Set(selectedFabrics.map((id) => String(id)));
    const minPrice = parsePrice(priceFrom);
    const maxPrice = parsePrice(priceTo);

    const filtered = catalogProducts.filter((product) => {
      if (fabricSet.size > 0) {
        const fabricId = product?.fabric_type?.id;
        if (!fabricId || !fabricSet.has(String(fabricId))) return false;
      }

      if (sizeSet.size > 0) {
        const variants = Array.isArray(product?.variants)
          ? product.variants
          : [];
        const hasSize = variants.some((variant) => {
          if (!variant || variant.is_active === false) return false;
          const sizeId = variant?.size?.id;
          return sizeId && sizeSet.has(String(sizeId));
        });
        if (!hasSize) return false;
      }

      const priceRange = getPriceRange(product);
      if (minPrice !== null) {
        if (!priceRange || priceRange.min < minPrice) return false;
      }
      if (maxPrice !== null) {
        if (!priceRange || priceRange.max > maxPrice) return false;
      }

      return true;
    });

    const sorted = [...filtered];
    sorted.sort((a, b) => {
      if (sortMode === "price_asc" || sortMode === "price_desc") {
        const priceA = getPriceRange(a)?.min ?? Number.POSITIVE_INFINITY;
        const priceB = getPriceRange(b)?.min ?? Number.POSITIVE_INFINITY;
        return sortMode === "price_asc" ? priceA - priceB : priceB - priceA;
      }
      if (sortMode === "name") {
        return String(a?.name || "").localeCompare(String(b?.name || ""), "ru");
      }
      if (sortMode === "promo") {
        return Number(b?.is_promotion) - Number(a?.is_promotion);
      }
      return Number(b?.is_new) - Number(a?.is_new);
    });
    return sorted;
  }, [
    catalogProducts,
    priceFrom,
    priceTo,
    selectedFabrics,
    selectedSizes,
    sortMode,
  ]);

  useEffect(() => {
    applyTheme(THEMES[themeName] ?? THEMES.cream);
  }, [themeName]);

  useEffect(() => {
    if (!activeProductId) return;
    setActiveImageIndex(0);
  }, [activeProductId]);

  useEffect(() => {
    if (!activeProduct) {
      setSelectedVariantId(null);
      setAddQuantity(1);
      return;
    }
    const variants = Array.isArray(activeProduct?.variants)
      ? activeProduct.variants.filter((v) => v?.is_active !== false)
      : [];
    setSelectedVariantId(variants[0]?.id ?? null);
    setAddQuantity(1);
  }, [activeProduct]);

  useEffect(() => {
    if (activeImageIndex < activeProductImages.length) return;
    setActiveImageIndex(0);
  }, [activeImageIndex, activeProductImages.length]);

  const isAuthenticated = !!authUser;

  const redirectToAuth = useCallback(() => {
    setAuthMode("login");
    setAuthModalOpen(true);
    setActiveProductId(null);
    setViewMode("home");
    window.location.hash = "";
  }, []);

  useEffect(() => {
    const updateFromHash = () => {
      const hash = window.location.hash || "";
      if (hash.startsWith("#product-")) {
        const match = hash.match(/product-(\d+)/);
        const nextId = match ? Number(match[1]) : null;
        if (Number.isFinite(nextId)) {
          setActiveProductId(nextId);
          setViewMode("product");
          return;
        }
      }
      if (hash === "#catalog") {
        setActiveProductId(null);
        setViewMode("catalog");
        return;
      }
      if (hash === "#about") {
        setActiveProductId(null);
        setViewMode("about");
        return;
      }
      if (hash === "#delivery") {
        setActiveProductId(null);
        setViewMode("delivery");
        return;
      }
      if (hash === "#contacts") {
        setActiveProductId(null);
        setViewMode("contacts");
        return;
      }
      if (hash === "#cart") {
        if (!isAuthenticated) {
          redirectToAuth();
          return;
        }
        setActiveProductId(null);
        setViewMode("cart");
        return;
      }
      if (hash === "#checkout") {
        if (!isAuthenticated) {
          redirectToAuth();
          return;
        }
        setActiveProductId(null);
        setViewMode("checkout");
        return;
      }
      if (hash === "#profile") {
        if (!isAuthenticated) {
          redirectToAuth();
          return;
        }
        setActiveProductId(null);
        setViewMode("profile");
        return;
      }
      setActiveProductId(null);
      setViewMode("home");
    };

    updateFromHash();
    window.addEventListener("hashchange", updateFromHash);
    return () => window.removeEventListener("hashchange", updateFromHash);
  }, [isAuthenticated, redirectToAuth]);

  useEffect(() => {
    const controller = new AbortController();

    async function loadSiteLogo(signal) {
      try {
        const res = await fetch("/api/site-logo/", { signal });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        if (data?.logo?.logo_url) {
          setSiteLogo({ type: "image", value: data.logo.logo_url });
          return;
        }
        if (data?.site_name) {
          setSiteLogo({ type: "text", value: data.site_name });
          return;
        }
        setSiteLogo({ type: "text", value: "BLAKITNY" });
      } catch {
        setSiteLogo({ type: "text", value: "BLAKITNY" });
      }
    }

    async function loadCompanyDetails(signal) {
      try {
        const res = await fetch("/api/company-details/", { signal });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const details = data?.company_details;
        if (details?.name || details?.description) {
          setCompanyDetails({
            name: details?.name || "",
            description: details?.description || "",
          });
          return;
        }
        setCompanyDetails(null);
      } catch {
        setCompanyDetails(null);
      }
    }

    async function loadAboutUs(signal) {
      try {
        const res = await fetch("/api/about-us/", { signal });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        if (data?.title || data?.content) {
          setAboutUsData(data);
        } else {
          setAboutUsData(null);
        }
      } catch {
        setAboutUsData(null);
      }
    }

    async function loadDeliveryPayment(signal) {
      try {
        const res = await fetch("/api/delivery-payment/", { signal });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        if (data?.delivery_info || data?.payment_info) {
          setDeliveryData(data);
        } else {
          setDeliveryData(null);
        }
      } catch {
        setDeliveryData(null);
      }
    }

    async function loadSocialNetworks(signal) {
      try {
        const res = await fetch("/api/social-networks/", { signal });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const list = Array.isArray(data) ? data : [];
        setSocialNetworks(list);
      } catch {
        setSocialNetworks([]);
      }
    }

    async function loadCategories(signal) {
      try {
        const res = await fetch("/api/catalog/categories/", { signal });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const list = Array.isArray(data) ? data : [];
        setCategories(list);
      } catch {
        setCategories([]);
      }
    }

    async function loadProfile(accessToken, refreshToken, signal) {
      try {
        const res = await fetch("/api/users/me/", {
          method: "GET",
          headers: { Authorization: `Bearer ${accessToken}` },
          signal,
        });
        if (res.ok) {
          const data = await res.json();
          setAuthUser({ id: data?.user_id, email: data?.email });
          return true;
        }
        if (res.status !== 401 || !refreshToken) return false;
        await pause(1000, signal);
        const refreshed = await refreshTokens(refreshToken, signal);
        if (!refreshed) return false;
        await pause(1000, signal);
        const retry = await fetch("/api/users/me/", {
          method: "GET",
          headers: { Authorization: `Bearer ${refreshed.access}` },
          signal,
        });
        if (!retry.ok) return false;
        const data = await retry.json();
        setAuthUser({ id: data?.user_id, email: data?.email });
        return true;
      } catch {
        return false;
      }
    }

    async function refreshTokens(refreshToken, signal) {
      try {
        const res = await fetch("/api/users/refresh/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ refresh: refreshToken }),
          signal,
        });
        const data = await res.json();
        if (!res.ok) return null;
        const nextTokens = {
          access: data?.access,
          refresh: data?.refresh || refreshToken,
        };
        if (!nextTokens.access) return null;
        storeTokens(nextTokens);
        return nextTokens;
      } catch {
        return null;
      }
    }

    async function bootstrapAuth(signal) {
      const tokens = readStoredTokens();
      if (!tokens) {
        return;
      }
      const ok = await loadProfile(tokens.access, tokens.refresh, signal);
      if (!ok) {
        clearTokens();
      }
    }

    async function loadSlider(signal) {
      try {
        const res = await fetch("/api/slider/", { signal });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const slides = Array.isArray(data?.sliders) ? data.sliders : [];
        setSliderSlides(slides);

        const imgUrls = slides
          .map((s) => toProxiedUrl(s?.image_url))
          .filter((u) => typeof u === "string" && u.length > 0);
        await preloadImages(imgUrls, signal);
      } catch (e) {
        if (e?.name === "AbortError") return;
        setSliderSlides([]);
        setSliderError(e instanceof Error ? e.message : "Ошибка загрузки");
      }
    }

    async function loadSizes(signal) {
      try {
        const res = await fetch("/api/catalog/sizes/", { signal });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const list = Array.isArray(data) ? data : [];
        setSizes(list.filter((item) => item?.is_active !== false));
      } catch {
        setSizes([]);
      }
    }

    async function loadFabrics(signal) {
      try {
        const res = await fetch("/api/catalog/fabrics/", { signal });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const list = Array.isArray(data) ? data : [];
        setFabrics(list.filter((item) => item?.is_active !== false));
      } catch {
        setFabrics([]);
      }
    }

    async function loadCatalogProducts(signal) {
      try {
        const res = await fetch("/api/catalog/products-with-variants/", {
          signal,
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const list = Array.isArray(data) ? data : [];
        setCatalogProducts(list);
      } catch {
        setCatalogProducts([]);
      }
    }

    async function bootstrap() {
      try {
        setPageReady(false);
        setSliderError(null);

        await loadSiteLogo(controller.signal);
        await pause(1000, controller.signal);
        await loadCompanyDetails(controller.signal);
        await pause(1000, controller.signal);
        await loadAboutUs(controller.signal);
        await pause(1000, controller.signal);
        await loadDeliveryPayment(controller.signal);
        await pause(1000, controller.signal);
        await loadSocialNetworks(controller.signal);
        await pause(1000, controller.signal);
        await loadCategories(controller.signal);
        await pause(1000, controller.signal);
        await bootstrapAuth(controller.signal);
        await pause(1000, controller.signal);
        await loadSlider(controller.signal);
        await pause(1000, controller.signal);
        await loadSizes(controller.signal);
        await pause(1000, controller.signal);
        await loadFabrics(controller.signal);
        await pause(1000, controller.signal);
        await loadCatalogProducts(controller.signal);
      } finally {
        if (!controller.signal.aborted) setPageReady(true);
      }
    }

    bootstrap();
    return () => controller.abort();
  }, []);

  const openAuth = (mode) => {
    setAuthMode(mode);
    setAuthModalOpen(true);
  };

  const handleLogin = async ({ email, password }) => {
    const res = await fetch("/api/users/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json().catch(() => null);
    if (!res.ok) {
      throw new Error(normalizeError(data, "Не удалось войти"));
    }
    const tokens = data?.tokens;
    if (!tokens?.access || !tokens?.refresh) {
      throw new Error("Некорректный ответ сервера");
    }
    const nextTokens = { access: tokens.access, refresh: tokens.refresh };
    storeTokens(nextTokens);
    setAuthUser({ id: data?.user_id, email: data?.email || email });
    await reloadFromServer();
  };

  const handleRegister = async ({ email, password, passwordConfirm }) => {
    const res = await fetch("/api/users/register/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email,
        password,
        password_confirm: passwordConfirm,
      }),
    });
    const data = await res.json().catch(() => null);
    if (!res.ok) {
      throw new Error(normalizeError(data, "Не удалось зарегистрироваться"));
    }
    const tokens = data?.tokens;
    if (!tokens?.access || !tokens?.refresh) {
      throw new Error("Некорректный ответ сервера");
    }
    const nextTokens = { access: tokens.access, refresh: tokens.refresh };
    storeTokens(nextTokens);
    setAuthUser({ id: data?.user_id, email: data?.email || email });
    await reloadFromServer();
  };

  const handleLogout = () => {
    setAuthUser(null);
    clearTokens();
    setViewMode("home");
    window.location.hash = "";
  };

  const handleResetFilters = () => {
    setSelectedSizes([]);
    setSelectedFabrics([]);
    setPriceFrom("");
    setPriceTo("");
    setSortMode("newest");
  };

  const openCatalog = () => {
    setViewMode("catalog");
    window.location.hash = "catalog";
  };

  const openCart = () => {
    if (!isAuthenticated) {
      redirectToAuth();
      return;
    }
    setViewMode("cart");
    window.location.hash = "cart";
  };

  const openCheckout = () => {
    if (!isAuthenticated) {
      redirectToAuth();
      return;
    }
    setViewMode("checkout");
    window.location.hash = "checkout";
  };

  const openProfile = () => {
    if (!isAuthenticated) {
      redirectToAuth();
      return;
    }
    setViewMode("profile");
    window.location.hash = "profile";
  };

  const openProduct = (id) => {
    setActiveProductId(id);
    setViewMode("product");
    window.location.hash = `product-${id}`;
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const closeProduct = () => {
    setActiveProductId(null);
    setViewMode("catalog");
    window.location.hash = "catalog";
  };

  const openImageModal = (index) => {
    setActiveImageIndex(index);
    setModalOpen(true);
  };

  const closeImageModal = () => {
    setModalOpen(false);
  };

  const prevImage = () => {
    setActiveImageIndex((prev) =>
      prev === 0 ? activeProductImages.length - 1 : prev - 1,
    );
  };

  const nextImage = () => {
    setActiveImageIndex((prev) => (prev + 1) % activeProductImages.length);
  };

  const goHome = (e) => {
    e.preventDefault();
    window.location.hash = "";
    setViewMode("home");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  if (!pageReady) {
    return (
      <div className="appLoading" aria-busy="true" aria-live="polite">
        <div className="spinner" />
        <div className="loadingText">Загружаем страницу…</div>
      </div>
    );
  }

  return (
    <div className="appShell">
      <header className="header">
        <div className="container headerInner">
          <div className="brand">
            <a
              href="#"
              className="brandLink"
              onClick={goHome}
              aria-label="На главную"
            >
              {siteLogo.type === "image" ? (
                <img
                  className="brandLogo"
                  src={toProxiedUrl(siteLogo.value)}
                  alt="BLAKITNY"
                />
              ) : (
                <div className="brandName">{siteLogo.value}</div>
              )}
            </a>
          </div>
          <nav className="nav" aria-label="Навигация">
            <a className="navLink" href="#catalog" onClick={openCatalog}>
              Каталог
            </a>
            <a className="navLink" href="#about">
              О нас
            </a>
            <a className="navLink" href="#delivery">
              Доставка и оплата
            </a>
            <a className="navLink" href="#contacts">
              Контакты
            </a>
            <a
              className="phoneIconLink"
              href={`tel:${phone}`}
              aria-label="Позвонить"
            >
              <svg
                className="phoneIcon"
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                aria-hidden="true"
              >
                <path
                  d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"
                  stroke="currentColor"
                  strokeWidth="1.8"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </a>
            <CartBadge onClick={openCart} />
            <ProfileMenu
              isAuthenticated={isAuthenticated}
              userEmail={authUser?.email}
              onLogin={() => openAuth("login")}
              onRegister={() => openAuth("register")}
              onProfile={openProfile}
              onLogout={handleLogout}
            />
          </nav>
        </div>
      </header>

      <main className="main">
        <div className="container">
          {viewMode === "product" ? (
            activeProduct ? (
              <section className="productPage">
                <button
                  type="button"
                  className="backBtn"
                  onClick={closeProduct}
                >
                  ← Вернуться в каталог
                </button>
                <div className="productLayout">
                  <div className="productGallery">
                    {activeProductImages.length > 0 ? (
                      <>
                        <div
                          className="productMainImage"
                          onClick={() => openImageModal(activeImageIndex)}
                        >
                          <img
                            src={toProxiedUrl(
                              activeProductImages[activeImageIndex]?.image,
                            )}
                            alt={activeProduct?.name || "Товар"}
                          />
                        </div>
                        <div className="productThumbs">
                          {activeProductImages.map((img, idx) => (
                            <button
                              key={img.id || idx}
                              type="button"
                              className={
                                idx === activeImageIndex
                                  ? "thumb thumbActive"
                                  : "thumb"
                              }
                              onClick={() => setActiveImageIndex(idx)}
                              aria-label={`Изображение ${idx + 1}`}
                            >
                              <img
                                src={toProxiedUrl(img.image)}
                                alt={activeProduct?.name || "Товар"}
                              />
                            </button>
                          ))}
                        </div>
                      </>
                    ) : (
                      <div className="productMainImage productImagePlaceholder">
                        Нет фото
                      </div>
                    )}
                  </div>
                  <div className="productInfo">
                    <div className="productBadges">
                      {activeProduct.is_new ? (
                        <span className="badge badgeNew">Новинка</span>
                      ) : null}
                      {activeProduct.is_promotion ? (
                        <span className="badge badgePromo">Акция</span>
                      ) : null}
                    </div>
                    <h1 className="productTitleLarge">{activeProduct.name}</h1>
                    <div className="productMetaLarge">
                      {activeProduct.category?.name || ""}{" "}
                      {activeProduct.subcategory?.name
                        ? `• ${activeProduct.subcategory.name}`
                        : ""}
                    </div>
                    <div className="productPriceLarge">
                      {(() => {
                        const range = getPriceRange(activeProduct);
                        if (!range) return "Цена уточняется";
                        if (range.min === range.max) {
                          return `${formatPrice(range.min)} ₽`;
                        }
                        return `${formatPrice(range.min)}–${formatPrice(
                          range.max,
                        )} ₽`;
                      })()}
                    </div>
                    <div className="productDetails">
                      {activeProduct.description ? (
                        <div className="productText">
                          {activeProduct.description}
                        </div>
                      ) : null}
                      {activeProduct.picture_title ? (
                        <div className="productSpec">
                          Рисунок: {activeProduct.picture_title}
                        </div>
                      ) : null}
                      {activeProduct.binding ? (
                        <div className="productSpec">
                          Переплёт: {activeProduct.binding}
                        </div>
                      ) : null}
                      {activeProduct.fabric_type?.name ? (
                        <div className="productSpec">
                          Ткань: {activeProduct.fabric_type.name}
                        </div>
                      ) : null}
                    </div>
                    {Array.isArray(activeProduct.variants) &&
                    activeProduct.variants.length > 0 ? (
                      <div className="productVariants">
                        <div className="variantsTitle">Размеры</div>
                        <div className="variantsList">
                          {activeProduct.variants
                            .filter((variant) => variant?.is_active !== false)
                            .map((variant) => (
                              <button
                                type="button"
                                className="variantChip"
                                key={variant.id}
                                onClick={() => setSelectedVariantId(variant.id)}
                                style={{
                                  borderColor:
                                    variant.id === selectedVariantId
                                      ? "rgba(196, 151, 111, 0.8)"
                                      : "color-mix(in srgb, var(--border) 70%, transparent)",
                                  boxShadow:
                                    variant.id === selectedVariantId
                                      ? "0 0 0 2px rgba(196, 151, 111, 0.2)"
                                      : "none",
                                }}
                              >
                                <span>{variant?.size?.name || "Размер"}</span>
                                <span>
                                  {formatPrice(Number(variant.price))} ₽
                                </span>
                              </button>
                            ))}
                        </div>
                      </div>
                    ) : null}
                    {activeProduct.variants &&
                    activeProduct.variants.length > 0 ? (
                      <div
                        style={{
                          display: "flex",
                          gap: 12,
                          flexWrap: "wrap",
                          alignItems: "center",
                        }}
                      >
                        <div style={{ display: "flex", gap: 8 }}>
                          <button
                            type="button"
                            onClick={() =>
                              setAddQuantity((prev) => Math.max(1, prev - 1))
                            }
                          >
                            −
                          </button>
                          <input
                            type="number"
                            min="1"
                            max="99"
                            value={addQuantity}
                            onChange={(e) => {
                              const next = Number(e.target.value);
                              setAddQuantity(
                                Number.isFinite(next)
                                  ? Math.min(99, Math.max(1, next))
                                  : 1,
                              );
                            }}
                            style={{
                              width: 70,
                              textAlign: "center",
                              borderRadius: 10,
                              border: "1px solid var(--border)",
                              padding: "8px 10px",
                              background: "var(--surface)",
                            }}
                          />
                          <button
                            type="button"
                            onClick={() =>
                              setAddQuantity((prev) => Math.min(99, prev + 1))
                            }
                          >
                            +
                          </button>
                        </div>
                        <button
                          type="button"
                          onClick={() => {
                            if (!isAuthenticated) {
                              redirectToAuth();
                              return;
                            }
                            const variants = Array.isArray(
                              activeProduct?.variants,
                            )
                              ? activeProduct.variants
                              : [];
                            const selected =
                              variants.find(
                                (variant) => variant?.id === selectedVariantId,
                              ) || variants[0];
                            if (!selected) return;
                            const images = Array.isArray(activeProduct?.images)
                              ? activeProduct.images
                              : [];
                            const activeImage = images.find(
                              (img) => img?.is_active !== false,
                            );
                            addToCart(
                              {
                                productId: activeProduct.id,
                                productName: activeProduct.name,
                                productImage: toProxiedUrl(activeImage?.image),
                                productVariantId: selected.id,
                                sizeName: selected?.size?.name || "",
                                price: Number(selected?.price ?? 0),
                                attributes: {
                                  binding: activeProduct.binding ?? null,
                                  pictureTitle:
                                    activeProduct.picture_title ?? null,
                                  fabric:
                                    activeProduct.fabric_type?.name ?? null,
                                  category:
                                    activeProduct.category?.name ?? null,
                                  subcategory:
                                    activeProduct.subcategory?.name ?? null,
                                },
                              },
                              addQuantity,
                            );
                          }}
                          style={{
                            borderRadius: 999,
                            padding: "10px 18px",
                            background: "var(--accent)",
                            color: "#fff",
                          }}
                        >
                          Добавить в корзину
                        </button>
                      </div>
                    ) : null}
                  </div>
                </div>
              </section>
            ) : (
              <section className="productPage">
                <button
                  type="button"
                  className="backBtn"
                  onClick={closeProduct}
                >
                  ← Вернуться в каталог
                </button>
                <div className="card" style={{ padding: 18 }}>
                  Товар не найден
                </div>
              </section>
            )
          ) : viewMode === "catalog" ? (
            <section className="catalogSection" id="catalog">
              <div className="sectionHeader">
                <div>
                  <div className="sectionTitle">Каталог</div>
                  <div className="sectionSubtitle">
                    Подберите комплект по размеру, ткани и цене
                  </div>
                </div>
              </div>
              <div className="catalogLayout">
                <aside className="catalogFilters">
                  <details className="filterGroup" open>
                    <summary className="filterSummary">
                      <span className="filterTitle">Размер</span>
                      {selectedSizes.length > 0 ? (
                        <span className="filterCount">
                          Выбрано: {selectedSizes.length}
                        </span>
                      ) : null}
                    </summary>
                    <div className="filterOptions">
                      {sizes.length === 0 ? (
                        <div className="filterEmpty">
                          Нет доступных размеров
                        </div>
                      ) : (
                        sizes.map((size) => (
                          <label className="filterOption" key={size.id}>
                            <input
                              type="checkbox"
                              checked={selectedSizes.includes(size.id)}
                              onChange={(e) => {
                                setSelectedSizes((prev) =>
                                  e.target.checked
                                    ? [...prev, size.id]
                                    : prev.filter((id) => id !== size.id),
                                );
                              }}
                            />
                            <span>{size.name}</span>
                          </label>
                        ))
                      )}
                    </div>
                  </details>
                  <details className="filterGroup" open>
                    <summary className="filterSummary">
                      <span className="filterTitle">Ткань</span>
                      {selectedFabrics.length > 0 ? (
                        <span className="filterCount">
                          Выбрано: {selectedFabrics.length}
                        </span>
                      ) : null}
                    </summary>
                    <div className="filterOptions">
                      {fabrics.length === 0 ? (
                        <div className="filterEmpty">Нет доступных тканей</div>
                      ) : (
                        fabrics.map((fabric) => (
                          <label className="filterOption" key={fabric.id}>
                            <input
                              type="checkbox"
                              checked={selectedFabrics.includes(fabric.id)}
                              onChange={(e) => {
                                setSelectedFabrics((prev) =>
                                  e.target.checked
                                    ? [...prev, fabric.id]
                                    : prev.filter((id) => id !== fabric.id),
                                );
                              }}
                            />
                            <span>{fabric.name}</span>
                          </label>
                        ))
                      )}
                    </div>
                  </details>
                  <details className="filterGroup" open>
                    <summary className="filterSummary">
                      <span className="filterTitle">Цена</span>
                    </summary>
                    <div className="priceRow">
                      <input
                        className="priceInput"
                        type="text"
                        inputMode="decimal"
                        placeholder="От"
                        value={priceFrom}
                        onChange={(e) => setPriceFrom(e.target.value)}
                      />
                      <span className="priceDivider">—</span>
                      <input
                        className="priceInput"
                        type="text"
                        inputMode="decimal"
                        placeholder="До"
                        value={priceTo}
                        onChange={(e) => setPriceTo(e.target.value)}
                      />
                    </div>
                  </details>
                  <button
                    type="button"
                    className="resetBtn"
                    onClick={handleResetFilters}
                  >
                    Сбросить фильтры
                  </button>
                </aside>
                <div className="catalogContent">
                  <div className="catalogToolbar card">
                    <div className="catalogCount">
                      Товаров: {filteredProducts.length}
                    </div>
                    <div className="sortRow">
                      <label className="sortLabel" htmlFor="catalogSort">
                        Сортировка
                      </label>
                      <select
                        id="catalogSort"
                        className="sortSelect"
                        value={sortMode}
                        onChange={(e) => setSortMode(e.target.value)}
                      >
                        <option value="newest">Сначала новинки</option>
                        <option value="promo">Сначала акции</option>
                        <option value="price_asc">Цена по возрастанию</option>
                        <option value="price_desc">Цена по убыванию</option>
                        <option value="name">По названию</option>
                      </select>
                    </div>
                  </div>
                  <div className="catalogGridWrap">
                    {filteredProducts.length === 0 ? (
                      <div className="catalogStatus">
                        Подходящих товаров пока нет
                      </div>
                    ) : null}
                    <div className="catalogGrid">
                      {filteredProducts.map((product) => {
                        const images = getActiveImages(product);
                        const range = getPriceRange(product);
                        const priceLabel = range
                          ? range.min === range.max
                            ? `${formatPrice(range.min)} ₽`
                            : `${formatPrice(range.min)}–${formatPrice(
                                range.max,
                              )} ₽`
                          : "Цена уточняется";
                        return (
                          <button
                            type="button"
                            className="productCard"
                            key={product.id}
                            onClick={() => openProduct(product.id)}
                          >
                            <div className="productMedia">
                              {images[0]?.image ? (
                                <img
                                  src={toProxiedUrl(images[0].image)}
                                  alt={product.name}
                                />
                              ) : (
                                <div className="productImagePlaceholder">
                                  Нет фото
                                </div>
                              )}
                              <div className="productBadges">
                                {product.is_new ? (
                                  <span className="badge badgeNew">
                                    Новинка
                                  </span>
                                ) : null}
                                {product.is_promotion ? (
                                  <span className="badge badgePromo">
                                    Акция
                                  </span>
                                ) : null}
                              </div>
                            </div>
                            <div className="productBody">
                              <div className="productTitle">{product.name}</div>
                              <div className="productMeta">
                                {product.subcategory?.name ||
                                  product.category?.name ||
                                  "Категория"}
                              </div>
                              <div className="productPrice">{priceLabel}</div>
                            </div>
                          </button>
                        );
                      })}
                    </div>
                  </div>
                </div>
              </div>
            </section>
          ) : viewMode === "about" ? (
            <AboutSection data={aboutUsData} className="card" />
          ) : viewMode === "delivery" ? (
            <DeliveryPaymentSection data={deliveryData} className="card" />
          ) : viewMode === "contacts" ? (
            <ContactsSection
              socialNetworks={socialNetworks}
              phone={phone}
              className="card"
            />
          ) : viewMode === "cart" ? (
            <CartPage
              isAuthenticated={isAuthenticated}
              onCheckout={openCheckout}
            />
          ) : viewMode === "checkout" ? (
            <CheckoutPage
              isAuthenticated={isAuthenticated}
              userEmail={authUser?.email}
              onBack={openCart}
              onOrderCreated={() => {
                setViewMode("profile");
                window.location.hash = "profile";
              }}
            />
          ) : viewMode === "profile" ? (
            <ProfilePage
              isAuthenticated={isAuthenticated}
              userEmail={authUser?.email}
            />
          ) : (
            <>
              <section className="card hero">
                <h1 className="heroTitle">Уют в светлых оттенках</h1>
                <p className="heroSubtitle">
                  Главная страница: слайдер подтягивается из бэкенда (app_home /
                  SliderListView). Остальные блоки добавим позже.
                </p>
                <HeroSlider
                  key={sliderKey}
                  slides={sliderSlides}
                  error={sliderError}
                />
                <div className="statusRow">API: /api/slider/</div>
              </section>
              <CategoriesSection categories={categories} />
              <AboutSection data={aboutUsData} />
              <DeliveryPaymentSection data={deliveryData} />
              <ContactsSection socialNetworks={socialNetworks} phone={phone} />
            </>
          )}
        </div>
      </main>

      <footer className="footer">
        <div className="container footerInner">
          <div className="footerGrid">
            <div className="footerCol">
              <div className="footerTitle">О нас</div>
              <a className="footerLink" href="#about">
                О бренде
              </a>
              <a className="footerLink" href="#about">
                Качество и материалы
              </a>
            </div>
            <div className="footerCol">
              <div className="footerTitle">Где купить</div>
              <a className="footerLink" href="#contacts">
                Адреса магазинов
              </a>
            </div>
            <div className="footerCol">
              <div className="footerTitle">Сотрудничество</div>
              <a className="footerLink" href="#contacts">
                Оптовым клиентам
              </a>
              <a className="footerLink" href="#contacts">
                Партнёрство
              </a>
            </div>
            <div className="footerCol">
              <div className="footerTitle">Информация</div>
              <a className="footerLink" href="#delivery">
                Доставка и оплата
              </a>
              <a className="footerLink" href="#contacts">
                Контакты
              </a>
            </div>
          </div>
          {companyDetails ? (
            <div className="footerDetails">
              {companyDetails.name ? (
                <div className="footerDetailsTitle">{companyDetails.name}</div>
              ) : null}
              {companyDetails.description ? (
                <div className="footerDetailsText">
                  {companyDetails.description}
                </div>
              ) : null}
            </div>
          ) : null}
          <div className="footerBottom">
            <div>© {new Date().getFullYear()} Blakitny</div>
            <div>Политика конфиденциальности</div>
          </div>
        </div>
      </footer>
      <AuthModal
        open={authModalOpen}
        mode={authMode}
        onClose={() => setAuthModalOpen(false)}
        onLogin={handleLogin}
        onRegister={handleRegister}
        onSwitch={(next) => setAuthMode(next)}
      />
      {modalOpen && (
        <ImageModal
          images={activeProductImages}
          activeIndex={activeImageIndex}
          onClose={closeImageModal}
          onPrev={prevImage}
          onNext={nextImage}
        />
      )}
    </div>
  );
}

export default App;
