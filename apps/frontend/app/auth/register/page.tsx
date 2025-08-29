'use client';
import { useState, FormEvent } from 'react';

export default function Register() {
  const [email, setEmail] = useState('user@example.com');
  const [password, setPassword] = useState('Welcome123');
  const [fullName, setFullName] = useState('User');
  const [message, setMessage] = useState('');

  const onSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const api = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const res = await fetch(`${api}/auth/register`, {
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
