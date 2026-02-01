import "./App.css";
import { useEffect, useMemo, useState } from "react";

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

function HeroSlider() {
  const [slides, setSlides] = useState([]);
  const [activeIndex, setActiveIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    async function load() {
      try {
        setLoading(true);
        setError(null);

        const res = await fetch("/api/slider/", { signal: controller.signal });
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`);
        }
        const data = await res.json();
        const nextSlides = Array.isArray(data?.sliders) ? data.sliders : [];
        setSlides(nextSlides);
        setActiveIndex(0);
      } catch (e) {
        if (e?.name === "AbortError") return;
        setError(e instanceof Error ? e.message : "Ошибка загрузки");
      } finally {
        setLoading(false);
      }
    }

    load();
    return () => controller.abort();
  }, []);

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
      {loading ? (
        <div className="slidePlaceholder">Загружаем слайдер…</div>
      ) : error ? (
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

function App() {
  const [themeName] = useState("cream");

  useEffect(() => {
    applyTheme(THEMES[themeName] ?? THEMES.cream);
  }, [themeName]);

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
          <div />
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
            <HeroSlider />
            <div className="statusRow">API: /api/slider/</div>
          </section>
        </div>
      </main>

      <footer className="footer">
        <div className="container footerInner">
          <div>© {new Date().getFullYear()} Blakitny</div>
          <div>Сделано на React</div>
        </div>
      </footer>
    </div>
  );
}

export default App;
