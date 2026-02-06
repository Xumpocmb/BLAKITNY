import React from 'react';

export function DeliveryPaymentSection({ data, className }) {
  if (!data) return null;

  return (
    <section className={`deliverySection ${className || ''}`} id="delivery">
      <div className="container">
        <h2 className="sectionTitle">Доставка и оплата</h2>
        <div className="deliveryGrid">
          <div className="deliveryCol">
            <h3 className="deliveryTitle">Доставка</h3>
            <div className="deliveryContent" style={{ whiteSpace: 'pre-wrap' }}>
              {data.delivery_info}
            </div>
          </div>
          <div className="deliveryCol">
            <h3 className="deliveryTitle">Оплата</h3>
            <div className="deliveryContent" style={{ whiteSpace: 'pre-wrap' }}>
              {data.payment_info}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
