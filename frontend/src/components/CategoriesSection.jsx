import React from "react";

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

export function CategoriesSection({
  categories,
  className,
  onCategoryClick,
  limit = 4,
}) {
  const activeCategories = Array.isArray(categories)
    ? categories.filter((cat) => cat.is_active !== false)
    : [];

  if (activeCategories.length === 0) return null;

  const displayCategories =
    typeof limit === "number"
      ? activeCategories.slice(0, limit)
      : activeCategories;

  return (
    <section className={`categoriesSection ${className || ""}`} id="categories">
      <div className="container">
        <h2 className="sectionTitle">Категории</h2>
        <div className="categoriesGrid">
          {displayCategories.map((category) => (
            <div
              key={category.id}
              className="categoryCard"
              onClick={() => onCategoryClick?.(category.id)}
            >
              <div className="categoryImageWrapper">
                {category.image ? (
                  <img
                    src={toProxiedUrl(category.image)}
                    alt={category.name}
                    className="categoryImage"
                  />
                ) : (
                  <div className="categoryImagePlaceholder">Нет фото</div>
                )}
              </div>
              <h3 className="categoryTitle">{category.name}</h3>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
