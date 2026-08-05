import type { Metadata } from "next";
import "./globals.css";
import PwaRegister from "./pwa-register";

export const metadata: Metadata = {
  applicationName: "DEUS ARCHIVE",
  title: {
    default: "DEUS ARCHIVE",
    template: "%s | DEUS ARCHIVE",
  },
  description: "Votre archive mobile pour jeux de rôle.",
  appleWebApp: {
    capable: true,
    statusBarStyle: "black-translucent",
    title: "DEUS ARCHIVE",
  },
  icons: {
    icon: "/assets/pwa/favicon.ico",
    apple: "/assets/pwa/apple-touch-icon.png",
  },
};

export const viewport = { themeColor: "#0B0F14" };

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr">
      <body>
        {children}
        <PwaRegister />
      </body>
    </html>
  );
}
