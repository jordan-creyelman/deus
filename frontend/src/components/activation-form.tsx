"use client";

import { FormEvent, useState } from "react";

export default function ActivationForm() {
  const [status, setStatus] = useState("En attente d’activation");

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const character = String(form.get("character") ?? "").trim();
    setStatus(character ? `Compte activé pour ${character}.` : "Indiquez un personnage.");
  }

  return (
    <form className="archive-panel activation-panel" onSubmit={handleSubmit}>
      <h1>ACTIVATION JOUEUR</h1>
      <label htmlFor="character">Joueur en attente</label>
      <input id="character" name="character" placeholder="Nom du personnage" required />
      <div className="account-state">
        <strong>État</strong>
        <span>{status}</span>
      </div>
      <button className="archive-button" type="submit">
        ACTIVER LE COMPTE
      </button>
    </form>
  );
}
