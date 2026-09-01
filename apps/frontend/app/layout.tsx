export const metadata = {
  title: 'أفضل رحلات في الغردقة | Hurghada',
  description: 'رحلات بحرية وسفاري وترفيه في الغردقة. الحجز على واتساب.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="ar" dir="rtl">
      <body style={{ margin: 0, fontFamily: 'Tahoma, Arial, sans-serif', background: '#f6f8fa', color: '#163041' }}>
        {children}
      </body>
    </html>
  );
}
