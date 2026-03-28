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
    scales: { y: { beginAtZero: true, max: 100 } },
  };

  const featureWords = [
    ...data.feature_importance.positive,
    ...data.feature_importance.negative,
  ].sort((a, b) => a.coefficient - b.coefficient);

  return (
    <Container size="lg" py={{ base: "md", md: "xl" }}>
      <Title order={1} mb="lg" size="h2">
        Dashboard Modelli
      </Title>

      <SimpleGrid cols={{ base: 2, sm: 2, md: 4 }} mb="xl">
        <MetricCard
          label="Accuratezza Department"
          value={data.metrics.department_accuracy}
          tooltip="Percentuale di recensioni il cui department è stato classificato correttamente dal modello migliore"
        />
        <MetricCard
          label="Accuratezza Sentiment"
          value={data.metrics.sentiment_accuracy}
          tooltip="Percentuale di recensioni il cui sentiment è stato classificato correttamente dal modello migliore"
        />
        <MetricCard
          label="F1 Department"
          value={data.metrics.department_f1}
          tooltip="Media armonica di precisione e recall per la classificazione del department (bilancia falsi positivi e falsi negativi)"
        />
        <MetricCard
          label="F1 Sentiment"
          value={data.metrics.sentiment_f1}
          tooltip="Media armonica di precisione e recall per la classificazione del sentiment"
        />
      </SimpleGrid>

      <Group mb="xs">
        <Badge color="blue">
          Miglior Department: {data.model_info.best_department_model}
        </Badge>
        <Badge color="teal">
          Miglior Sentiment: {data.model_info.best_sentiment_model}
        </Badge>
        <Badge color="gray">Addestrato: {data.model_info.training_date}</Badge>
      </Group>

      <SimpleGrid cols={{ base: 1, md: 2 }} mt="xl">
        <Card shadow="sm" padding="md" radius="md" withBorder>
          <Title order={3} mb="md" size="h4">
            Classificazione Department
          </Title>
          <Text size="sm" c="dimmed" mb="sm">
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
                  backgroundColor: "rgba(34,139,230,0.7)",
                },
                {
                  label: "F1 %",
                  data: deptF1s,
                  backgroundColor: "rgba(34,139,230,0.3)",
                },
              ],
            }}
            options={chartOptions}
          />
        </Card>

        <Card shadow="sm" padding="md" radius="md" withBorder>
          <Title order={3} mb="md" size="h4">
            Classificazione Sentiment
          </Title>
          <Text size="sm" c="dimmed" mb="sm">
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
                  backgroundColor: "rgba(18,184,134,0.7)",
                },
                {
                  label: "F1 %",
                  data: sentF1s,
                  backgroundColor: "rgba(18,184,134,0.3)",
                },
              ],
            }}
            options={chartOptions}
          />
        </Card>
      </SimpleGrid>

      <SimpleGrid cols={{ base: 1, sm: 2 }} mt="xl">
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

      <Card shadow="sm" padding="md" radius="md" withBorder mt="xl">
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
          }}
        />
      </Card>
    </Container>
  );
}

function MetricCard({
  label,
  value,
  tooltip,
}: {
  label: string;
  value: number;
  tooltip: string;
}) {
  return (
    <Tooltip label={tooltip} multiline w={260} withArrow>
      <Card
        shadow="sm"
        padding="md"
        radius="md"
        withBorder
        style={{ cursor: "help" }}
      >
        <Stack gap={4}>
          <Text size="xs" c="dimmed">
            {label}
          </Text>
          <Text size="lg" fw={700}>
            {(value * 100).toFixed(1)}%
          </Text>
        </Stack>
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
    <Card shadow="sm" padding="md" radius="md" withBorder>
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
      <div style={{ overflowX: "auto" }}>
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            textAlign: "center",
            minWidth: 200,
          }}
        >
          <thead>
            <tr>
              <th style={{ padding: 8 }}></th>
              {labels.map((l) => (
                <th key={l} style={{ padding: 8, fontSize: 12 }}>
                  {l}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {matrix.map((row, i) => (
              <tr key={i}>
                <td style={{ padding: 8, fontWeight: 600, fontSize: 12 }}>
                  {labels[i]}
                </td>
                {row.map((cell, j) => (
                  <td
                    key={j}
                    style={{
                      padding: 8,
                      background:
                        i === j
                          ? `rgba(18,184,134,${Math.min(cell / 60, 1)})`
                          : cell > 0
                            ? `rgba(255,77,77,${Math.min(cell / 60, 1)})`
                            : "transparent",
                      borderRadius: 4,
                      fontWeight: i === j ? 700 : 400,
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
