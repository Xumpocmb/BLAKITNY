import "./App.css";
import { useEffect, useMemo, useRef, useState } from "react";

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

const AUTH_STORAGE_KEY = "blakitny_auth_active";

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

function ProfileMenu() {
  const rootRef = useRef(null);
  const [open, setOpen] = useState(false);
  const [isActive, setIsActive] = useState(() => {
    try {
      return localStorage.getItem(AUTH_STORAGE_KEY) === "1";
    } catch {
      return false;
    }
  });

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

  const setActive = (next) => {
    setIsActive(next);
    try {
      if (next) localStorage.setItem(AUTH_STORAGE_KEY, "1");
      else localStorage.removeItem(AUTH_STORAGE_KEY);
    } catch {
      // ignore
    }
  };

  const onLogin = () => {
    setActive(true);
    setOpen(false);
  };

  const onRegister = () => {
    setActive(true);
    setOpen(false);
  };

  const onProfile = () => {
    setOpen(false);
  };

  const onLogout = () => {
    setActive(false);
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
          {isActive ? (
            <>
              <button
                type="button"
                className="menuItem"
                role="menuitem"
                onClick={onProfile}
              >
                Профиль
              </button>
              <button
                type="button"
                className="menuItem"
                role="menuitem"
                onClick={onLogout}
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
                onClick={onLogin}
              >
                Вход
              </button>
              <button
                type="button"
                className="menuItem"
                role="menuitem"
                onClick={onRegister}
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

function App() {
  const [themeName] = useState("cream");
  const phone = "+79990000000";
  const [pageReady, setPageReady] = useState(false);
  const [sliderSlides, setSliderSlides] = useState([]);
  const [sliderError, setSliderError] = useState(null);
  const sliderKey = useMemo(
    () => sliderSlides.map((s) => s.id).join("-"),
    [sliderSlides],
  );

  useEffect(() => {
    applyTheme(THEMES[themeName] ?? THEMES.cream);
  }, [themeName]);

  useEffect(() => {
    const controller = new AbortController();

    async function bootstrap() {
      try {
        setPageReady(false);
        setSliderError(null);

        const res = await fetch("/api/slider/", { signal: controller.signal });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const slides = Array.isArray(data?.sliders) ? data.sliders : [];
        setSliderSlides(slides);

        const imgUrls = slides
          .map((s) => toProxiedUrl(s?.image_url))
          .filter((u) => typeof u === "string" && u.length > 0);
        await preloadImages(imgUrls, controller.signal);
      } catch (e) {
        if (e?.name === "AbortError") return;
        setSliderSlides([]);
        setSliderError(e instanceof Error ? e.message : "Ошибка загрузки");
      } finally {
        if (!controller.signal.aborted) setPageReady(true);
      }
    }

    bootstrap();
    return () => controller.abort();
  }, []);

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
            <div className="brandName">BLAKITNY</div>
            <div className="brandTagline">
              Постельное бельё и домашний текстиль
            </div>
          </div>
          <nav className="nav" aria-label="Навигация">
            <a className="navLink" href="#catalog">
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
                  d="M7.1 3.9c.4-.4.9-.6 1.4-.4l2.7 1c.6.2 1 .8.9 1.4l-.5 2.4c-.1.5 0 1 .4 1.4l2.8 2.8c.4.4.9.5 1.4.4l2.4-.5c.6-.1 1.2.3 1.4.9l1 2.7c.2.5 0 1.1-.4 1.4l-1.4 1.4c-.9.9-2.2 1.2-3.4.8-3.2-1.1-6.3-3.2-9.1-6-2.8-2.8-4.9-5.9-6-9.1-.4-1.2-.1-2.5.8-3.4L7.1 3.9Z"
                  stroke="currentColor"
                  strokeWidth="1.8"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </a>
            <ProfileMenu />
          </nav>
        </div>
      </header>

      <main className="main">
        <div className="container">
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
              <a className="footerLink" href="#catalog">
                Каталог
              </a>
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
          <div className="footerBottom">
            <div>© {new Date().getFullYear()} Blakitny</div>
            <div>Сделано на React</div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
