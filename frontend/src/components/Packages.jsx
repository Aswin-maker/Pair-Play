import React from 'react';

export default function Packages({ packages }) {
  if (!packages.length) return <p>No packages available.</p>;
  return (
    <div className="grid">
      {packages.map((p, i) => (
        <div key={i} className="card">
          {p.image_url && <img src={p.image_url} alt={p.package_name} />}
          <h3 style={{margin:'0 0 0.5rem'}}>{p.package_name}</h3>
          <div className="badge">{p.location}</div>
          <p style={{margin:'0.5rem 0'}}><strong>Days:</strong> {p.days ?? 'N/A'} | <strong>Budget:</strong> {p.budget ?? 'N/A'}</p>
          <p style={{flexGrow:1}}>{p.itinerary}</p>
          <button style={{marginTop:'auto'}} onClick={() => window.dispatchEvent(new CustomEvent('lead:create', { detail: p }))}>Enquire</button>
        </div>
      ))}
    </div>
  );
}
