"use client";

import { useEffect } from "react";

export default function PwaRegister() {
  useEffect(() => {
    if (!("serviceWorker" in navigator)) {
      return;
    }

    const registerServiceWorker = () => {
      navigator.serviceWorker.register("/sw.js", {
        scope: "/",
        updateViaCache: "none",
      });
    };

    window.addEventListener("load", registerServiceWorker);

    return () => window.removeEventListener("load", registerServiceWorker);
  }, []);

  return null;
}
