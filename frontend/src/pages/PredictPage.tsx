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
  Tooltip,
  Text,
  Progress,
} from "@mantine/core";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip as ChartTooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";
import type { PredictResponse } from "../api";
import { predict } from "../api";

ChartJS.register(CategoryScale, LinearScale, BarElement, ChartTooltip, Legend);

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
  const [result, setResult] = useState<PredictResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!bodyInput.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const data = await predict(bodyInput, titleInput || undefined);
      setResult(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Errore sconosciuto");
    } finally {
      setLoading(false);
    }
  };

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
            <Card shadow="sm" padding="lg" radius="md" withBorder>
              <Title order={3} mb="md" size="h4">
                Predizioni Department
              </Title>
              <Stack gap="sm">
                {result.department.map((p) => (
                  <div key={p.model}>
                    <Group justify="space-between" mb={4}>
                      <Text size="sm" fw={500}>
                        {p.model}
                      </Text>
                      <Badge color="orange" variant="light" size="sm">
                        {p.prediction}
                      </Badge>
                    </Group>
                    {p.confidence !== null ? (
                      <Group gap="xs" align="center">
                        <Progress
                          value={p.confidence * 100}
                          color="orange"
                          size="sm"
                          radius="xl"
                          style={{ flex: 1 }}
                        />
                        <Text size="xs" c="dimmed" w={45} ta="right">
                          {(p.confidence * 100).toFixed(1)}%
                        </Text>
                      </Group>
                    ) : (
                      <Text size="xs" c="dimmed">
                        Confidenza N/D
                      </Text>
                    )}
                  </div>
                ))}
              </Stack>
            </Card>

            <Card shadow="sm" padding="lg" radius="md" withBorder>
              <Title order={3} mb="md" size="h4">
                Predizioni Sentiment
              </Title>
              <Stack gap="sm">
                {result.sentiment.map((p) => (
                  <div key={p.model}>
                    <Group justify="space-between" mb={4}>
                      <Text size="sm" fw={500}>
                        {p.model}
                      </Text>
                      <Badge
                        color={
                          p.prediction === "Positive" ? "yellow" : "orange"
                        }
                        variant="light"
                        size="sm"
                      >
                        {p.prediction === "Positive" ? "Positivo" : "Negativo"}
                      </Badge>
                    </Group>
                    {p.confidence !== null ? (
                      <Group gap="xs" align="center">
                        <Progress
                          value={p.confidence * 100}
                          color={
                            p.prediction === "Positive" ? "yellow" : "orange"
                          }
                          size="sm"
                          radius="xl"
                          style={{ flex: 1 }}
                        />
                        <Text size="xs" c="dimmed" w={45} ta="right">
                          {(p.confidence * 100).toFixed(1)}%
                        </Text>
                      </Group>
                    ) : (
                      <Text size="xs" c="dimmed">
                        Confidenza N/D
                      </Text>
                    )}
                  </div>
                ))}
              </Stack>
            </Card>
          </SimpleGrid>

          {sentimentContributions.length > 0 && (
            <Card shadow="sm" padding="lg" radius="md" withBorder mb="xl">
              <Group gap="xs" mb="md" align="center">
                <Title order={3} size="h4">
                  Contributo Parole — Sentiment
                </Title>
                <Tooltip
                  label="Impatto di ogni parola sulla predizione del sentiment, calcolato dai coefficienti del modello Logistic Regression. Valori positivi spingono verso 'Positivo', negativi verso 'Negativo'."
                  multiline
                  w={300}
                  withArrow
                >
                  <Badge
                    variant="light"
                    color="gray"
                    size="sm"
                    style={{ cursor: "help" }}
                  >
                    Solo Logistic Regression ⓘ
                  </Badge>
                </Tooltip>
              </Group>
              <Bar
                data={{
                  labels: sentimentContributions.map((w) => w.word),
                  datasets: [
                    {
                      label: "Impatto",
                      data: sentimentContributions.map((w) => w.impact),
                      backgroundColor: sentimentContributions.map((w) =>
                        w.impact >= 0
                          ? "rgba(252,196,25,0.7)"
                          : "rgba(255,146,43,0.7)",
                      ),
                    },
                  ],
                }}
                options={{
                  indexAxis: "y",
                  responsive: true,
                  plugins: { legend: { display: false } },
                  scales: {
                    x: {
                      title: {
                        display: true,
                        text: "Impatto (Negativo ← → Positivo)",
                      },
                      grid: { color: "rgba(0,0,0,0.04)" },
                    },
                    y: { grid: { display: false } },
                  },
                }}
              />
            </Card>
          )}

          {departmentContributions.length > 0 && (
            <Card shadow="sm" padding="lg" radius="md" withBorder mb="xl">
              <Group gap="xs" mb="md" align="center">
                <Title order={3} size="h4">
                  Contributo Parole — Department
                </Title>
                <Tooltip
                  label="Associazione di ogni parola al department, calcolata dai coefficienti del modello Logistic Regression. Ogni parola è assegnata al department dove ha l'impatto assoluto più forte."
                  multiline
                  w={300}
                  withArrow
                >
                  <Badge
                    variant="light"
                    color="gray"
                    size="sm"
                    style={{ cursor: "help" }}
                  >
                    Solo Logistic Regression ⓘ
                  </Badge>
                </Tooltip>
              </Group>
              <Group gap="xs" mb="md">
                <Badge color="blue">Housekeeping</Badge>
                <Badge color="teal">Reception</Badge>
                <Badge color="orange">F&B</Badge>
              </Group>
              <Bar
                data={{
                  labels: departmentContributions
                    .slice(0, 20)
                    .map((w) => w.word),
                  datasets: [
                    {
                      label: "Impatto",
                      data: departmentContributions
                        .slice(0, 20)
                        .map((w) => w.impact),
                      backgroundColor: departmentContributions
                        .slice(0, 20)
                        .map((w) => {
                          if (w.department === "Housekeeping")
                            return "rgba(34,139,230,0.7)";
                          if (w.department === "Reception")
                            return "rgba(18,184,134,0.7)";
                          return "rgba(255,146,43,0.7)";
                        }),
                    },
                  ],
                }}
                options={{
                  indexAxis: "y",
                  responsive: true,
                  plugins: { legend: { display: false } },
                  scales: {
                    x: {
                      title: { display: true, text: "Impatto (assoluto)" },
                      grid: { color: "rgba(0,0,0,0.04)" },
                    },
                    y: { grid: { display: false } },
                  },
                }}
              />
            </Card>
          )}
        </>
      )}
    </Container>
  );
}
