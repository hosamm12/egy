import Image from 'next/image';

export default function Home() {
  return (
    <main style={{ display: 'grid', placeItems: 'center', height: '100vh', gap: 16 }}>
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
      </div>
    </main>
  );
}
