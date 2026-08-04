export default function OfflinePage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[#020b1f] px-6 text-center text-white">
      <div className="max-w-md">
        <p className="mb-3 text-sm font-semibold uppercase tracking-[0.3em] text-amber-400">
          DEUS ARCHIVE
        </p>
        <h1 className="text-3xl font-bold">Vous êtes hors ligne</h1>
        <p className="mt-4 text-slate-300">
          Vérifiez votre connexion, puis rechargez la page pour retrouver vos
          archives.
        </p>
      </div>
    </main>
  );
}
