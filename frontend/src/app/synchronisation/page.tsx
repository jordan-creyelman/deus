import ArchiveShell from "@/components/archive-shell";

export default function SynchronisationPage() {
  return (
    <ArchiveShell>
      <section className="archive-panel sync-panel">
        <h1>ACCÈS RECONNU.</h1>
        <h2>SYNCHRONISATION EN COURS.</h2>
        <div className="sync-ring" role="status" aria-label="Synchronisation en cours">
          <span>Synchronisation</span>
        </div>
        <p>Veuillez patienter.</p>
      </section>
    </ArchiveShell>
  );
}
