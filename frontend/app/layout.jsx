import { Syne, DM_Sans } from 'next/font/google';
import './globals.css';

const syne = Syne({ subsets:['latin'], variable:'--font-syne', weight:['400','500','600','700','800'] });
const dm   = DM_Sans({ subsets:['latin'], variable:'--font-dm',  weight:['300','400','500','600'] });

export const metadata = {
  title: 'StudyHub — AI-Powered Learning Platform',
  description: 'Your intelligent study companion for academic excellence.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${syne.variable} ${dm.variable}`}>
      <body className="font-sans antialiased bg-ink-950 text-ink-100">{children}</body>
    </html>
  );
}
