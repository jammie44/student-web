import { Syne, DM_Sans } from 'next/font/google';
import './globals.css';

const syne = Syne({ subsets: ['latin'], variable: '--font-syne', weight: ['400','500','600','700','800'], display: 'swap' });
const dm   = DM_Sans({ subsets: ['latin'], variable: '--font-dm',   weight: ['300','400','500','600'],       display: 'swap' });

export const metadata = {
  title: 'StudyHub — AI Academic Assistant',
  description: 'Study smarter with AI-powered tools for every student.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${syne.variable} ${dm.variable}`}>
      <body>{children}</body>
    </html>
  );
}
