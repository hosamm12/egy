export default function Home() {
  return (
    <main style={{ fontFamily: 'sans-serif', margin: 0, minHeight: '100vh', background: '#0b1f2a', color: '#fff' }}>
      <section style={{ maxWidth: 720, margin: '0 auto', padding: '72px 24px', textAlign: 'center' }}>
        <p style={{ letterSpacing: 2, color: '#c9a227', marginBottom: 12 }}>HURGHADA</p>
        <h1 style={{ fontSize: 40, lineHeight: 1.2, margin: '0 0 16px' }}>رحلات الغردقة</h1>
        <p style={{ fontSize: 18, color: '#d7e4ea', margin: '0 0 32px' }}>
          رحلات بحرية، سفاري، وسنوركل. احجز مباشرة على واتساب.
        </p>
        <a
          href="https://wa.me/201055569645"
          target="_blank"
          rel="noreferrer"
          style={{
            display: 'inline-block',
            background: '#25D366',
            color: '#082016',
            textDecoration: 'none',
            fontWeight: 700,
            padding: '14px 28px',
            borderRadius: 999,
          }}
        >
          واتساب 01055569645
        </a>
        <p style={{ marginTop: 28, color: '#9fb3bd' }}>
          فنادق وطيران يمكن ترتيبهما عند الطلب.
        </p>
      </section>
    </main>
  );
}
