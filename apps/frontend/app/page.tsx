const WA = 'https://wa.me/201055569645';

const groups = [
  {
    title: 'رحلات بحرية',
    items: [
      ['جزيرة أورانج باي', 'مصريين 1100 جنيه / أجانب 22$'],
      ['مركب البايرتس إلى أورانج باي', 'مصريين 1700 جنيه / أجانب 70$'],
      ['جزيرة هولا هولا باليخت', 'مصريين 1100 جنيه / أجانب 22$'],
      ['جزيرة بارادايس باليخت', 'مصريين 2000 جنيه / أجانب 40$'],
      ['دولفين هاوس', 'مصريين 1000 جنيه / أجانب 20$'],
      ['الغطس في البحر الأحمر', 'مصريين 1200 جنيه / أجانب 24$'],
    ],
  },
  {
    title: 'رحلات ترفيهية',
    items: [
      ['باراشوت وبنانا بوت', '200–2000 جنيه'],
      ['عرض الدولفين', 'مصريين 250 جنيه / أجانب 12$'],
      ['أكوا بارك', 'مصريين 2000 جنيه / أجانب 40$'],
      ['جراند أكواريوم', 'مصريين 700 جنيه / أجانب 33$'],
    ],
  },
  {
    title: 'سفاري الغردقة',
    items: [
      ['سوبر سفاري', 'مصريين 900 جنيه / أجانب 20$'],
      ['سفاري عائلي', 'مصريين 750 جنيه / أجانب 16$'],
      ['بيتش باجي صباحي', 'مصريين 800 جنيه / أجانب 17$'],
      ['جيب سفاري ومشاهدة النجوم', 'مصريين 1550 جنيه / أجانب 32$'],
    ],
  },
];

export default function Home() {
  return (
    <main>
      <header style={{ background: '#0b3b4f', color: '#fff', padding: '18px 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <strong>EGY Discovery</strong>
        <a href={WA} style={{ background: '#25D366', color: '#082016', textDecoration: 'none', padding: '8px 14px', borderRadius: 999, fontWeight: 700 }}>
          واتساب
        </a>
      </header>

      <section style={{ background: 'linear-gradient(180deg,#0b3b4f,#14627d)', color: '#fff', padding: '56px 20px', textAlign: 'center' }}>
        <p style={{ color: '#e7c56a', letterSpacing: 2, margin: 0 }}>الغردقة</p>
        <h1 style={{ fontSize: 34, margin: '10px 0 12px' }}>أفضل رحلات في الغردقة</h1>
        <p style={{ maxWidth: 640, margin: '0 auto 22px', color: '#d7e8ef' }}>
          رحلات بحرية، سفاري، وترفيه. الأسعار واضحة والحجز على واتساب. فنادق وطيران عند الطلب.
        </p>
        <a href={WA} style={{ background: '#25D366', color: '#082016', textDecoration: 'none', padding: '12px 22px', borderRadius: 999, fontWeight: 700 }}>
          كلمنا على واتساب 01055569645
        </a>
      </section>

      {groups.map((group) => (
        <section key={group.title} style={{ maxWidth: 980, margin: '0 auto', padding: '28px 16px' }}>
          <h2 style={{ fontSize: 22, marginBottom: 14 }}>{group.title}</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 14 }}>
            {group.items.map(([name, price]) => (
              <article key={name} style={{ background: '#fff', borderRadius: 16, padding: 16, boxShadow: '0 6px 20px rgba(8,32,48,.08)' }}>
                <h3 style={{ margin: '0 0 8px', fontSize: 18 }}>{name}</h3>
                <p style={{ margin: '0 0 14px', color: '#2c6a86', fontWeight: 700 }}>{price}</p>
                <a href={`${WA}?text=${encodeURIComponent('عايز أحجز ' + name)}`} style={{ color: '#0b3b4f', fontWeight: 700 }}>
                  التفاصيل والحجز
                </a>
              </article>
            ))}
          </div>
        </section>
      ))}

      <footer style={{ textAlign: 'center', padding: '28px 16px 40px', color: '#5b7380' }}>
        الحجز على واتساب · 01055569645
      </footer>
    </main>
  );
}
