import type { ReactNode } from "react";
import Image from "next/image";

import officialLogo from "../../ASSETS/LOGOS/logo_officiel_AKASHA.png";

type ArchiveShellProps = {
  children: ReactNode;
  compact?: boolean;
};

export default function ArchiveShell({ children, compact = false }: ArchiveShellProps) {
  return (
    <main className={`archive-screen${compact ? " archive-screen--compact" : ""}`}>
      <div className="star-field" aria-hidden="true" />
      <header className="archive-brand">
        <Image
          alt="AKASHA — DEUS ARCHIVE"
          className="archive-official-logo"
          src={officialLogo}
          priority
          sizes="(max-width: 640px) 180px, 230px"
        />
      </header>
      {children}
      <div className="archive-orbits" aria-hidden="true">
        <span />
      </div>
      <footer className="archive-version">V0.05</footer>
    </main>
  );
}
