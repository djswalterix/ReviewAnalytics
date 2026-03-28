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
  Table,
  Tooltip,
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
      <Title order={1} mb="lg" size="h2">
        Predizione Recensione
      </Title>

      <Card shadow="sm" padding="md" radius="md" withBorder mb="xl">
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
          <Button onClick={handleSubmit} loading={loading}>
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
            <Card shadow="sm" padding="md" radius="md" withBorder>
              <Title order={3} mb="md" size="h4">
                Predizioni Department
              </Title>
              <Table highlightOnHover style={{ minWidth: 280 }}>
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th>Modello</Table.Th>
                    <Table.Th>Predizione</Table.Th>
                    <Table.Th>Confidenza</Table.Th>
                  </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                  {result.department.map((p) => (
                    <Table.Tr key={p.model}>
                      <Table.Td>{p.model}</Table.Td>
                      <Table.Td>
                        <Badge color="blue">{p.prediction}</Badge>
                      </Table.Td>
                      <Table.Td>
                        {p.confidence !== null
                          ? `${(p.confidence * 100).toFixed(1)}%`
                          : "N/D"}
                      </Table.Td>
                    </Table.Tr>
                  ))}
                </Table.Tbody>
              </Table>
            </Card>

            <Card shadow="sm" padding="md" radius="md" withBorder>
              <Title order={3} mb="md" size="h4">
                Predizioni Sentiment
              </Title>
              <Table highlightOnHover style={{ minWidth: 280 }}>
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th>Modello</Table.Th>
                    <Table.Th>Predizione</Table.Th>
                    <Table.Th>Confidenza</Table.Th>
                  </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                  {result.sentiment.map((p) => (
                    <Table.Tr key={p.model}>
                      <Table.Td>{p.model}</Table.Td>
                      <Table.Td>
                        <Badge
                          color={p.prediction === "Positive" ? "green" : "red"}
                        >
                          {p.prediction === "Positive"
                            ? "Positivo"
                            : "Negativo"}
                        </Badge>
                      </Table.Td>
                      <Table.Td>
                        {p.confidence !== null
                          ? `${(p.confidence * 100).toFixed(1)}%`
                          : "N/D"}
                      </Table.Td>
                    </Table.Tr>
                  ))}
                </Table.Tbody>
              </Table>
            </Card>
          </SimpleGrid>

          {sentimentContributions.length > 0 && (
            <Card shadow="sm" padding="md" radius="md" withBorder mb="xl">
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
                          ? "rgba(18,184,134,0.7)"
                          : "rgba(255,77,77,0.7)",
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
                    },
                  },
                }}
              />
            </Card>
          )}

          {departmentContributions.length > 0 && (
            <Card shadow="sm" padding="md" radius="md" withBorder mb="xl">
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
                    },
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
