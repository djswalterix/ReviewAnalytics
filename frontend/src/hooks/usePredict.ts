import { useState } from "react";
import type { PredictResponse } from "../api";
import { predict } from "../api";

export function usePredict() {
  const [result, setResult] = useState<PredictResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const run = async (body: string, title?: string) => {
    if (!body.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await predict(body, title);
      setResult(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Errore sconosciuto");
    } finally {
      setLoading(false);
    }
  };

  return { result, error, loading, run };
}
