import './globals.css';
export const metadata = {
  title: 'StudyHub — AI Academic Assistant',
  description: 'AI-powered study tools: Study Assistant, Plagiarism Checker, CV Generator, Assignment Helper, Research Summarizer.',
};
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com"/>
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous"/>
        <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet"/>
      </head>
      <body style={{fontFamily:"'DM Sans',sans-serif"}}>{children}</body>
    </html>
  );
}
