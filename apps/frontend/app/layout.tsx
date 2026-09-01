export const metadata = {
  title: 'رحلات الغردقة | Hurghada',
  description: 'رحلات الغردقة والحجز على واتساب',
};

export default function RootLayout({ children }) {
  return (
    <html lang="ar" dir="rtl">
      <body style={{ fontFamily: 'sans-serif', margin: 0 }}>
        {children}
      </body>
    </html>
  );
}
