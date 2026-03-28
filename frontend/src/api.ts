const BASE_URL = import.meta.env.DEV ? "http://localhost:8080" : "";

export interface DashboardData {
  metrics: {
    department_accuracy: number;
    sentiment_accuracy: number;
    department_f1: number;
    sentiment_f1: number;
  };
  model_comparison: {
    department: Record<string, { accuracy: number; f1: number }>;
    sentiment: Record<string, { accuracy: number; f1: number }>;
  };
  confusion_matrix: {
    department: number[][];
    sentiment: number[][];
    labels_dept: string[];
    labels_sent: string[];
  };
  feature_importance: {
    positive: { word: string; coefficient: number }[];
    negative: { word: string; coefficient: number }[];
  };
  model_info: {
    best_department_model: string;
    best_sentiment_model: string;
    training_date: string;
  };
}

export interface PredictionResult {
  model: string;
  prediction: string;
  confidence: number | null;
}

export interface WordImpact {
  word: string;
  impact: number;
}

export interface DepartmentWordImpact {
  word: string;
  department: string;
  impact: number;
}

export interface PredictResponse {
  review: string;
  department: PredictionResult[];
  sentiment: PredictionResult[];
  sentiment_word_contributions: WordImpact[];
  department_word_contributions: DepartmentWordImpact[];
}

export async function fetchDashboard(): Promise<DashboardData> {
  const res = await fetch(`${BASE_URL}/dashboard`);
  if (!res.ok) throw new Error("Failed to fetch dashboard data");
  return res.json();
}

export async function predict(
  body: string,
  title?: string,
): Promise<PredictResponse> {
  const res = await fetch(`${BASE_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ body, title: title || null }),
  });
  if (!res.ok) throw new Error("Prediction failed");
  return res.json();
}
