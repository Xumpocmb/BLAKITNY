import React from "react";

export function DeliveryPaymentSection({ data, className }) {
  if (!data) return null;
  const rawDeliveryText =
    typeof data.delivery_info === "string" ? data.delivery_info : "";
  const deliveryText = rawDeliveryText
    .split("\n")
    .filter((line) => !/(оплат|платеж|цен|стоимост)/i.test(line))
    .join("\n")
    .trim();
  const deliveryContent =
    deliveryText ||
    [
      "Сроки доставки по регионам: от 1 до 7 рабочих дней в зависимости от города.",
      "Способы доставки: курьером, в пункты выдачи заказов и почтовыми службами.",
      "Условия бесплатной доставки: действует при заказе от установленной суммы.",
      "География доставки: доставка по всей территории России.",
      "Отслеживание заказа: после отправки предоставляется трек-номер для статуса доставки.",
    ].join("\n\n");

  return (
    <section className={`deliverySection ${className || ""}`} id="delivery">
      <div className="container">
        <h1 className="sectionTitle">Доставка</h1>
        <div className="aboutContent" style={{ whiteSpace: "pre-wrap" }}>
          {deliveryContent}
        </div>
      </div>
    </section>
  );
}
