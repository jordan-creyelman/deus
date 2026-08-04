import RetryButton from "@/components/retry-button";

export default function UnavailablePage() {
  return (
    <main className="unavailable-screen">
      <section>
        <h1>SYSTÈME INDISPONIBLE.</h1>
        <p>
          Aucun accès valide détecté.
          <br />
          Veuillez réessayer ultérieurement.
        </p>
        <RetryButton />
        <span>[État de connexion]</span>
      </section>
    </main>
  );
}
