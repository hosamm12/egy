"use client";

import Image from 'next/image';
import { useState, type ChangeEvent, type FormEvent } from 'react';

export default function Home() {
  const [form, setForm] = useState({
    location: '',
    hotel: '',
    checkIn: '',
    checkOut: '',
    persons: 1,
    phone: '',
    score: 70
  });

  function handleChange(e: ChangeEvent<HTMLInputElement>) {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  }

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (Number(form.score) < 70) {
      alert('Lead score must be at least 70 to trigger automation.');
      return;
    }
    const msg = `Location: ${form.location}%0AHotel: ${form.hotel}%0ADates: ${form.checkIn} to ${form.checkOut}%0APersons: ${form.persons}%0APhone: ${form.phone}`;
    window.open(`https://wa.me/201091474206?text=${msg}`, '_blank');
  }

  return (
    <main style={{ display: 'grid', placeItems: 'center', minHeight: '100vh', gap: 16 }}>
      <div style={{ textAlign: 'center' }}>
        <Image
          src="/hero.svg"
          alt="Colorful placeholder"
          width={600}
          height={400}
          style={{
            borderRadius: 8,
            boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
            marginBottom: 16
          }}
        />
        <h1>EgySaaS</h1>
        <p>Starter template is running.</p>
        <a href="/auth/login">Login</a> &nbsp;|&nbsp; <a href="/auth/register">Register</a>

        <form onSubmit={handleSubmit} style={{ marginTop: 24, display: 'grid', gap: 8 }}>
          <input
            name="location"
            value={form.location}
            onChange={handleChange}
            placeholder="Location"
            required
          />
          <input
            name="hotel"
            value={form.hotel}
            onChange={handleChange}
            placeholder="Hotel"
            required
          />
          <input
            type="date"
            name="checkIn"
            value={form.checkIn}
            onChange={handleChange}
            required
          />
          <input
            type="date"
            name="checkOut"
            value={form.checkOut}
            onChange={handleChange}
            required
          />
          <input
            type="number"
            name="persons"
            value={form.persons}
            onChange={handleChange}
            min={1}
            placeholder="Number of persons"
            required
          />
          <input
            type="tel"
            name="phone"
            value={form.phone}
            onChange={handleChange}
            placeholder="Contact number"
            required
          />
          <input
            type="number"
            name="score"
            value={form.score}
            onChange={handleChange}
            min={0}
            max={100}
            placeholder="Lead score"
          />
          <button type="submit">Send via WhatsApp</button>
        </form>
        <p style={{ marginTop: 8 }}>
          Or chat directly on{' '}
          <a href="https://wa.me/201091474206" target="_blank" rel="noopener noreferrer">
            WhatsApp
          </a>
        </p>
      </div>
    </main>
  );
}
