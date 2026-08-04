"use client";

export default function RetryButton() {
  return (
    <button className="retry-button" type="button" onClick={() => window.location.reload()}>
      ACTUALISER
    </button>
  );
}
