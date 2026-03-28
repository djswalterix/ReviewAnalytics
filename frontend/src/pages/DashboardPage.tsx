import { useEffect, useState } from "react";
import {
  Container,
  Title,
  SimpleGrid,
  Card,
  Text,
  Group,
  Badge,
  Stack,
  Loader,
  Alert,
  Tooltip,
  RingProgress,
  Divider,
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
import type { DashboardData } from "../api";
import { fetchDashboard } from "../api";

ChartJS.register(CategoryScale, LinearScale, BarElement, ChartTooltip, Legend);

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboard()
      .then(setData)
      .catch((e) => setError(e.message));
  }, []);

  if (error)
    return (
      <Alert color="red" title="Errore">
        {error}
      </Alert>
    );
  if (!data) return <Loader m="xl" />;

  const modelNames = Object.keys(data.model_comparison.department);
  const deptAccuracies = modelNames.map(
    (n) => data.model_comparison.department[n].accuracy * 100,
  );
  const deptF1s = modelNames.map(
    (n) => data.model_comparison.department[n].f1 * 100,
  );
  const sentAccuracies = modelNames.map(
    (n) => data.model_comparison.sentiment[n].accuracy * 100,
  );
  const sentF1s = modelNames.map(
    (n) => data.model_comparison.sentiment[n].f1 * 100,
  );

  const chartOptions = {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        grid: { color: "rgba(0,0,0,0.04)" },
      },
      x: { grid: { display: false } },
    },
    plugins: {
      legend: {
        labels: { usePointStyle: true, pointStyle: "circle", padding: 16 },
      },
    },
    barPercentage: 0.7,
  };

  const featureWords = [
    ...data.feature_importance.positive,
    ...data.feature_importance.negative,
  ].sort((a, b) => a.coefficient - b.coefficient);

  return (
    <Container size="lg" py={{ base: "md", md: "xl" }}>
      <Group justify="space-between" align="flex-end" mb="xl">
        <div>
          <Title order={1} size="h2" style={{ letterSpacing: -0.5 }}>
            Dashboard Modelli
          </Title>
          <Text size="sm" c="dimmed" mt={4}>
            Panoramica delle performance dei modelli di classificazione
          </Text>
        </div>
        <Group gap="xs">
          <Badge color="orange" variant="light" size="lg">
            Miglior Department: {data.model_info.best_department_model}
          </Badge>
          <Badge color="yellow" variant="light" size="lg">
            Miglior Sentiment: {data.model_info.best_sentiment_model}
          </Badge>
        </Group>
      </Group>

      <SimpleGrid cols={{ base: 2, sm: 2, md: 4 }} mb="xl">
        <MetricCard
          label="Accuratezza Department"
          value={data.metrics.department_accuracy}
          color="#ff922b"
          tooltip="Percentuale di recensioni il cui department è stato classificato correttamente dal modello migliore"
        />
        <MetricCard
          label="Accuratezza Sentiment"
          value={data.metrics.sentiment_accuracy}
          color="#fcc419"
          tooltip="Percentuale di recensioni il cui sentiment è stato classificato correttamente dal modello migliore"
        />
        <MetricCard
          label="F1 Department"
          value={data.metrics.department_f1}
          color="#ff922b"
          tooltip="Media armonica di precisione e recall per la classificazione del department (bilancia falsi positivi e falsi negativi)"
        />
        <MetricCard
          label="F1 Sentiment"
          value={data.metrics.sentiment_f1}
          color="#fcc419"
          tooltip="Media armonica di precisione e recall per la classificazione del sentiment"
        />
      </SimpleGrid>

      <Badge color="gray" variant="light" size="sm" mb="xl">
        Addestrato: {data.model_info.training_date}
      </Badge>

      <Divider
        my="lg"
        label="Confronto Modelli"
        labelPosition="left"
        styles={{ label: { fontWeight: 600, fontSize: 13 } }}
      />

      <SimpleGrid cols={{ base: 1, md: 2 }} mt="md">
        <Card shadow="sm" padding="lg" radius="md" withBorder>
          <Title order={3} mb={4} size="h4">
            Classificazione Department
          </Title>
          <Text size="sm" c="dimmed" mb="md">
            Confronto tra i modelli addestrati per la classificazione del
            department
          </Text>
          <Bar
            data={{
              labels: modelNames,
              datasets: [
                {
                  label: "Accuratezza %",
                  data: deptAccuracies,
                  backgroundColor: "rgba(255,146,43,0.8)",
                  borderRadius: 6,
                },
                {
                  label: "F1 %",
                  data: deptF1s,
                  backgroundColor: "rgba(255,146,43,0.3)",
                  borderRadius: 6,
                },
              ],
            }}
            options={chartOptions}
          />
        </Card>

        <Card shadow="sm" padding="lg" radius="md" withBorder>
          <Title order={3} mb={4} size="h4">
            Classificazione Sentiment
          </Title>
          <Text size="sm" c="dimmed" mb="md">
            Confronto tra i modelli addestrati per la classificazione del
            sentiment
          </Text>
          <Bar
            data={{
              labels: modelNames,
              datasets: [
                {
                  label: "Accuratezza %",
                  data: sentAccuracies,
                  backgroundColor: "rgba(252,196,25,0.8)",
                  borderRadius: 6,
                },
                {
                  label: "F1 %",
                  data: sentF1s,
                  backgroundColor: "rgba(252,196,25,0.35)",
                  borderRadius: 6,
                },
              ],
            }}
            options={chartOptions}
          />
        </Card>
      </SimpleGrid>

      <Divider
        my="xl"
        label="Matrici di Confusione"
        labelPosition="left"
        styles={{ label: { fontWeight: 600, fontSize: 13 } }}
      />

      <SimpleGrid cols={{ base: 1, sm: 2 }} mt="md">
        <ConfusionMatrixCard
          title="Matrice di Confusione — Department"
          tooltip="Matrice calcolata sul modello Logistic Regression. Le righe indicano la classe reale, le colonne la classe predetta. I valori sulla diagonale (verde) sono le predizioni corrette."
          matrix={data.confusion_matrix.department}
          labels={data.confusion_matrix.labels_dept}
        />
        <ConfusionMatrixCard
          title="Matrice di Confusione — Sentiment"
          tooltip="Matrice calcolata sul modello Logistic Regression. Le righe indicano la classe reale, le colonne la classe predetta. I valori sulla diagonale (verde) sono le predizioni corrette."
          matrix={data.confusion_matrix.sentiment}
          labels={data.confusion_matrix.labels_sent}
        />
      </SimpleGrid>

      <Divider
        my="xl"
        label="Importanza delle Parole"
        labelPosition="left"
        styles={{ label: { fontWeight: 600, fontSize: 13 } }}
      />

      <Card shadow="sm" padding="lg" radius="md" withBorder mt="md">
        <Group gap="xs" mb="md" align="center">
          <Title order={3} size="h4">
            Importanza delle Parole — Sentiment
          </Title>
          <Tooltip
            label="Coefficienti estratti dal modello Logistic Regression per il sentiment. Valori positivi indicano parole associate a recensioni positive, valori negativi a recensioni negative."
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
            labels: featureWords.map((w) => w.word),
            datasets: [
              {
                label: "Coefficiente",
                data: featureWords.map((w) => w.coefficient),
                backgroundColor: featureWords.map((w) =>
                  w.coefficient >= 0
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
              x: { grid: { color: "rgba(0,0,0,0.04)" } },
              y: { grid: { display: false } },
            },
          }}
        />
      </Card>
    </Container>
  );
}

function MetricCard({
  label,
  value,
  color,
  tooltip,
}: {
  label: string;
  value: number;
  color: string;
  tooltip: string;
}) {
  const pct = value * 100;
  return (
    <Tooltip label={tooltip} multiline w={260} withArrow>
      <Card
        shadow="sm"
        padding="md"
        radius="md"
        withBorder
        style={{ cursor: "help" }}
      >
        <Group gap="md" wrap="nowrap">
          <RingProgress
            size={56}
            thickness={5}
            roundCaps
            sections={[{ value: pct, color }]}
            label={
              <Text size="xs" ta="center" fw={700} style={{ fontSize: 11 }}>
                {pct.toFixed(0)}
              </Text>
            }
          />
          <Stack gap={2}>
            <Text size="xs" c="dimmed" lineClamp={2}>
              {label}
            </Text>
            <Text size="lg" fw={700}>
              {pct.toFixed(1)}%
            </Text>
          </Stack>
        </Group>
      </Card>
    </Tooltip>
  );
}

function ConfusionMatrixCard({
  title,
  tooltip,
  matrix,
  labels,
}: {
  title: string;
  tooltip: string;
  matrix: number[][];
  labels: string[];
}) {
  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      <Group gap="xs" mb="md" align="center">
        <Title order={3} size="h4">
          {title}
        </Title>
        <Tooltip label={tooltip} multiline w={300} withArrow>
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
      <Text size="xs" c="dimmed" mb="xs">
        Righe = classe reale · Colonne = classe predetta
      </Text>
      <div style={{ overflowX: "auto" }}>
        <table
          style={{
            width: "100%",
            borderCollapse: "separate",
            borderSpacing: 3,
            textAlign: "center",
            minWidth: 200,
          }}
        >
          <thead>
            <tr>
              <th style={{ padding: 8 }}></th>
              {labels.map((l) => (
                <th
                  key={l}
                  style={{
                    padding: "6px 8px",
                    fontSize: 11,
                    fontWeight: 600,
                    color: "#868e96",
                    textTransform: "uppercase",
                    letterSpacing: 0.5,
                  }}
                >
                  {l}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {matrix.map((row, i) => (
              <tr key={i}>
                <td
                  style={{
                    padding: "6px 8px",
                    fontWeight: 600,
                    fontSize: 11,
                    color: "#868e96",
                    textTransform: "uppercase",
                    letterSpacing: 0.5,
                    textAlign: "right",
                  }}
                >
                  {labels[i]}
                </td>
                {row.map((cell, j) => (
                  <td
                    key={j}
                    style={{
                      padding: "10px 8px",
                      background:
                        i === j
                          ? `rgba(252,196,25,${Math.max(Math.min(cell / 60, 1), 0.15)})`
                          : cell > 0
                            ? `rgba(255,146,43,${Math.max(Math.min(cell / 60, 1), 0.1)})`
                            : "rgba(0,0,0,0.02)",
                      borderRadius: 6,
                      fontWeight: i === j ? 700 : 400,
                      fontSize: 14,
                      transition: "transform 0.15s",
                    }}
                  >
                    {cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
