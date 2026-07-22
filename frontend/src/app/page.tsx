type HealthResponse = {
  status: string;
  service: string;
  database: string;
};

async function getBackendHealth(): Promise<HealthResponse | null> {
  const apiUrl = process.env.INTERNAL_API_URL;

  if (!apiUrl) {
    return null;
  }

  try {
    const response = await fetch(`${apiUrl}/api/health/`, {
      cache: "no-store",
    });

    if (!response.ok) {
      return null;
    }

    return response.json();
  } catch {
    return null;
  }
}

export default async function Home() {
  const health = await getBackendHealth();

  return (
    <main>
      <h1>DEUS ARCHIVE</h1>

      {health ? (
        <div>
          <p>Backend : {health.status}</p>
          <p>Service : {health.service}</p>
          <p>Database : {health.database}</p>
        </div>
      ) : (
        <p>Backend indisponible</p>
      )}
    </main>
  );
}