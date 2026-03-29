import { useState } from "react";
import {
  Container,
  Title,
  TextInput,
  Textarea,
  Button,
  Card,
  SimpleGrid,
  Stack,
  Badge,
  Group,
  Alert,
  Text,
} from "@mantine/core";
import type { PredictionResult } from "../api";
import PredictionCard from "../components/PredictionCard";
import WordImpactChart from "../components/WordImpactChart";
import { usePredict } from "../hooks/usePredict";

export default function PredictPage() {
  const [titleInput, setTitleInput] = useState(
    "Soggiorno complessivamente negativo",
  );
  const [bodyInput, setBodyInput] = useState(
    "La camera era sporca e il bagno aveva problemi con l'acqua calda. " +
      "Il personale della reception è stato scortese al momento del check-in e non ha saputo risolvere i problemi segnalati. " +
      "Il ristorante dell'hotel offriva poca scelta e la qualità del cibo era mediocre. " +
      "Unico punto positivo: la posizione centrale dell'hotel, comoda per visitare la città.",
  );
  const { result, error, loading, run } = usePredict();

  const handleSubmit = () => run(bodyInput, titleInput || undefined);

  const sentimentContributions = result?.sentiment_word_contributions ?? [];
  const departmentContributions = result?.department_word_contributions ?? [];

  return (
    <Container size="lg" py={{ base: "md", md: "xl" }}>
      <div>
        <Title order={1} mb={4} size="h2" style={{ letterSpacing: -0.5 }}>
          Predizione Recensione
        </Title>
        <Text size="sm" c="dimmed" mb="lg">
          Inserisci una recensione per analizzare department e sentiment
        </Text>
      </div>

      <Card shadow="sm" padding="lg" radius="md" withBorder mb="xl">
        <Stack gap="md">
          <TextInput
            label="Titolo (opzionale)"
            placeholder="es. Camera deludente"
            value={titleInput}
            onChange={(e) => setTitleInput(e.currentTarget.value)}
          />
          <Textarea
            label="Testo della recensione"
            placeholder="Scrivi o incolla una recensione di un hotel in italiano..."
            minRows={4}
            value={bodyInput}
            onChange={(e) => setBodyInput(e.currentTarget.value)}
          />
          <Button
            onClick={handleSubmit}
            loading={loading}
            size="md"
            color="orange"
            style={{ alignSelf: "flex-start" }}
          >
            Analizza
          </Button>
        </Stack>
      </Card>

      {error && (
        <Alert color="red" title="Errore" mb="xl">
          {error}
        </Alert>
      )}

      {result && (
        <>
          <SimpleGrid cols={{ base: 1, md: 2 }} mb="xl">
            <PredictionCard
              title="Predizioni Department"
              predictions={result.department}
              colorFn={() => "orange"}
            />
            <PredictionCard
              title="Predizioni Sentiment"
              predictions={result.sentiment}
              colorFn={(p: PredictionResult) =>
                p.prediction === "Positive" ? "yellow" : "orange"
              }
              labelFn={(prediction: string) =>
                prediction === "Positive" ? "Positivo" : "Negativo"
              }
            />
          </SimpleGrid>

          {sentimentContributions.length > 0 && (
            <div style={{ marginBottom: "var(--mantine-spacing-xl)" }}>
              <WordImpactChart
                title="Contributo Parole — Sentiment"
                tooltip="Impatto di ogni parola sulla predizione del sentiment, calcolato dai coefficienti del modello Logistic Regression. Valori positivi spingono verso 'Positivo', negativi verso 'Negativo'."
                labels={sentimentContributions.map((w) => w.word)}
                data={sentimentContributions.map((w) => w.impact)}
                backgroundColor={sentimentContributions.map((w) =>
                  w.impact >= 0
                    ? "rgba(252,196,25,0.7)"
                    : "rgba(255,146,43,0.7)",
                )}
                xAxisTitle="Impatto (Negativo ← → Positivo)"
              />
            </div>
          )}

          {departmentContributions.length > 0 && (
            <div style={{ marginBottom: "var(--mantine-spacing-xl)" }}>
              <WordImpactChart
                title="Contributo Parole — Department"
                tooltip="Associazione di ogni parola al department, calcolata dai coefficienti del modello Logistic Regression. Ogni parola è assegnata al department dove ha l'impatto assoluto più forte."
                labels={departmentContributions.slice(0, 20).map((w) => w.word)}
                data={departmentContributions.slice(0, 20).map((w) => w.impact)}
                backgroundColor={departmentContributions
                  .slice(0, 20)
                  .map((w) => {
                    if (w.department === "Housekeeping")
                      return "rgba(34,139,230,0.7)";
                    if (w.department === "Reception")
                      return "rgba(18,184,134,0.7)";
                    return "rgba(255,146,43,0.7)";
                  })}
                xAxisTitle="Impatto (assoluto)"
                legend={
                  <Group gap="xs" mb="md">
                    <Badge color="blue">Housekeeping</Badge>
                    <Badge color="teal">Reception</Badge>
                    <Badge color="orange">F&B</Badge>
                  </Group>
                }
              />
            </div>
          )}
        </>
      )}
    </Container>
  );
}
