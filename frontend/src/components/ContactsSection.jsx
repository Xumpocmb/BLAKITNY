import React from 'react';

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

export function ContactsSection({ socialNetworks, phone, className }) {
  const activeNetworks = Array.isArray(socialNetworks) 
    ? socialNetworks.filter(n => n.is_active !== false) 
    : [];

  if (activeNetworks.length === 0 && !phone) return null;

  return (
    <section className={`contactsSection ${className || ''}`} id="contacts">
      <div className="container">
        <h2 className="sectionTitle">Контакты</h2>
        
        <div className="contactsGrid">
          {phone && (
            <div className="contactCard">
              <h3 className="contactLabel">Телефон</h3>
              <a href={`tel:${phone}`} className="contactValue phoneLink">
                {phone}
              </a>
              <div className="contactHint">Ежедневно с 10:00 до 20:00</div>
            </div>
          )}

          {activeNetworks.length > 0 && (
            <div className="contactCard">
              <h3 className="contactLabel">Мы в соцсетях</h3>
              <div className="socialLinks">
                {activeNetworks.map((net) => (
                  <a 
                    key={net.id} 
                    href={net.link} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="socialLinkCard"
                  >
                    {net.icon_url && (
                      <img 
                        src={toProxiedUrl(net.icon_url)} 
                        alt={net.name} 
                        className="socialIcon"
                      />
                    )}
                    <span className="socialName">{net.name}</span>
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
