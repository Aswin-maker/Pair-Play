import React, { useEffect, useState } from 'react';
import Packages from './components/Packages';
import ChatWidget from './components/ChatWidget';
import { fetchPackages } from './api';

export default function App() {
  const [packages, setPackages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const data = await fetchPackages();
        setPackages(data.packages || []);
      } catch (e) {
        setError(e.message || 'Failed to load packages');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <div className="container">
      <ChatWidget />
      <h2>Featured Packages</h2>
      {loading && <p>Loading...</p>}
      {error && <p style={{color:'crimson'}}>{error}</p>}
      {!loading && !error && <Packages packages={packages} />}
    </div>
  );
}
