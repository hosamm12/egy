'use client';
import { useEffect, useState } from 'react';

export default function Dashboard() {
  const [me, setMe] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/auth/login';
      return;
    }
    const fetchMe = async () => {
      const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(`${api}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await res.json();
      if (res.ok) setMe(data);
      else setError(data.detail || 'Unauthorized');
    };
    fetchMe();
  }, []);

  return (
    <main style={{ padding: 24 }}>
      <a href="/">← Home</a>
      <h1>Dashboard</h1>
      {me ? (
        <pre>{JSON.stringify(me, null, 2)}</pre>
      ) : (
        <p>{error || 'Loading...'}</p>
      )}
    </main>
  );
}
