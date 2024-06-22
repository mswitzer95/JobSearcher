
export const metadata = {
  title: "JobSearcher",
  description: "JobSearcher",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
