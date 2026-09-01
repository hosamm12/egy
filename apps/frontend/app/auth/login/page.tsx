'use client';
import { FormEvent, useState } from 'react';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const res = await fetch(`${api}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: email, password })
    });
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem('token', data.access_token);
      window.location.href = '/dashboard';
    } else {
      setMessage(data.detail || 'Login failed');
    }
  };

  return (
    <main style={{ display: 'grid', placeItems: 'center', height: '100vh' }}>
      <form onSubmit={onSubmit} style={{ display: 'grid', gap: 8, minWidth: 320 }}>
        <h2>Login</h2>
        <input value={email} onChange={(e)=>setEmail(e.target.value)} placeholder="email" />
        <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)} placeholder="password" />
        <button type="submit">Sign in</button>
        {!!message && <p>{message}</p>}
      </form>
    </main>
  );
}
