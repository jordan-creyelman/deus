"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

export default function LogoutButton() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  async function logout() {
    setIsLoading(true);
    try {
      await fetch("/api/auth/logout/", {
        method: "POST",
        credentials: "include",
      });
    } finally {
      router.replace("/");
      router.refresh();
    }
  }

  return (
    <button className="logout-button" disabled={isLoading} onClick={logout} type="button">
      {isLoading ? "DÉCONNEXION…" : "SE DÉCONNECTER"}
    </button>
  );
}
