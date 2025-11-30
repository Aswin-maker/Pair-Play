import React, { useEffect, useState } from 'react';
import { aiRecommend, createLead } from '../api';

/*
  ChatWidget integrates with Zoho SalesIQ global object once loaded.
  We set custom listeners bridging SalesIQ events to backend endpoints.
  Deluge scripts can invoke REST calls to our backend; here we offer a browser-side helper as well.
*/
export default function ChatWidget() {
  const [ready, setReady] = useState(false);
  const [status, setStatus] = useState('initializing');

  useEffect(() => {
    function handleZohoReady() {
      setReady(true);
      setStatus('online');
      // Example: expose a global to let Deluge (via widget APIs / custom script) call front-end functions
      window.TravelBot = {
        recommend: async (text) => {
          const res = await aiRecommend(text);
          return res.recommendation;
        },
        createLead: async (lead) => {
          const res = await createLead(lead);
          return res.status === 'lead_created';
        }
      };
      console.log('TravelBot bridge ready');
    }

    // Poll for SalesIQ readiness (since script is async defer loaded)
    const interval = setInterval(() => {
      if (window.$zoho && window.$zoho.salesiq && typeof window.$zoho.salesiq.ready === 'function') {
        clearInterval(interval);
        try { window.$zoho.salesiq.ready(handleZohoReady); } catch { handleZohoReady(); }
      }
    }, 500);

    // Listen for package lead creation events from UI cards
    const leadListener = async (e) => {
      const pkg = e.detail;
      setStatus('creating-lead');
      try {
        await createLead({
          name: 'Web User',
          email: 'webuser@example.com',
          phone: '0000000000',
          package_name: pkg.package_name
        });
        setStatus('lead-created');
      } catch (err) {
        console.error('Lead create failed', err);
        setStatus('lead-error');
      } finally {
        setTimeout(() => setStatus('online'), 1500);
      }
    };
    window.addEventListener('lead:create', leadListener);
    return () => {
      clearInterval(interval);
      window.removeEventListener('lead:create', leadListener);
    };
  }, []);

  return (
    <div style={{margin:'1rem 0', padding:'0.75rem 1rem', background:'#fff', border:'1px solid #e0e0e0', borderRadius:8}}>
      <strong>SalesIQ Status:</strong> {status}
      {!ready && <p style={{margin:'0.5rem 0 0', fontSize:'0.85rem'}}>Waiting for SalesIQ widget...</p>}
      {ready && <p style={{margin:'0.5rem 0 0', fontSize:'0.85rem'}}>Chat widget connected. Use chat to ask for package recommendations.</p>}
    </div>
  );
}
