"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

type TokenResponse = {
  access: string;
  refresh: string;
};

export default function LoginForm() {
  const router = useRouter();
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage("");
    setIsLoading(true);

    const form = new FormData(event.currentTarget);

    try {
      const response = await fetch("/api/auth/token/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: form.get("username"),
          password: form.get("password"),
        }),
      });

      if (!response.ok) {
        setMessage("Connexion impossible. Vérifiez vos informations.");
        return;
      }

      const tokens = (await response.json()) as TokenResponse;
      localStorage.setItem("access_token", tokens.access);
      localStorage.setItem("refresh_token", tokens.refresh);
      router.push("/synchronisation");
    } catch {
      router.push("/indisponible");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <form className="archive-panel login-panel" onSubmit={handleSubmit}>
      <h1>CONNEXION</h1>
      <label htmlFor="username">Identifiant</label>
      <input id="username" name="username" placeholder="Votre identifiant" required />
      <label htmlFor="password">Mot de passe</label>
      <input
        id="password"
        name="password"
        type="password"
        placeholder="Votre mot de passe"
        required
      />
      <button className="archive-button" disabled={isLoading} type="submit">
        {isLoading ? "CONNEXION…" : "CONNEXION"}
      </button>
      <p className="form-message" role="status">
        {message}
      </p>
    </form>
  );
}
