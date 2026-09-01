'use client';
import { FormEvent, useState } from 'react';
import { getApiBase } from '../../../lib/api';

export default function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [message, setMessage] = useState('');

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const api = getApiBase();
    if (!api.ok) {
      setMessage(api.reason);
      return;
    }
    const res = await fetch(`${api.base}/api/v1/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, full_name: fullName })
    });
    const data = await res.json();
    if (res.ok) {
      setMessage('Registered! You can log in now.');
    } else {
      setMessage(data.detail || 'Registration failed');
    }
  };

  return (
    <main style={{ display: 'grid', placeItems: 'center', height: '100vh' }}>
      <form onSubmit={onSubmit} style={{ display: 'grid', gap: 8, minWidth: 320 }}>
        <h2>Register</h2>
        <input value={email} onChange={(e)=>setEmail(e.target.value)} placeholder="email" />
        <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)} placeholder="password" />
        <input value={fullName} onChange={(e)=>setFullName(e.target.value)} placeholder="full name" />
        <button type="submit">Create account</button>
        {!!message && <p>{message}</p>}
      </form>
    </main>
  );
}
