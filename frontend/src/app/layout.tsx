import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  applicationName: "DEUS ARCHIVE",
  title: {
    default: "DEUS ARCHIVE",
    template: "%s | DEUS ARCHIVE",
  },
  description: "Votre archive mobile pour jeux de rôle.",
};

export const viewport = { themeColor: "#0a1016" };

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  );
}
