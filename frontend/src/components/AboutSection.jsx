import React from 'react';

export function AboutSection({ data, className }) {
  if (!data) return null;

  return (
    <section className={`aboutSection ${className || ''}`} id="about">
      <div className="container">
        <h2 className="sectionTitle">{data.title}</h2>
        <div className="aboutContent" style={{ whiteSpace: 'pre-wrap' }}>
          {data.content}
        </div>
      </div>
    </section>
  );
}
