export default function Home() {
  return (
    <main style={{ display: 'grid', placeItems: 'center', height: '100vh', gap: 16 }}>
      <div>
        <h1>EgySaaS</h1>
        <p>Starter template is running.</p>
        <a href="/auth/login">Login</a> &nbsp;|&nbsp; <a href="/auth/register">Register</a>
      </div>
    </main>
  );
}
