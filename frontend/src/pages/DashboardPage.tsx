import {
  Container,
  Title,
  SimpleGrid,
  Card,
  Text,
  Group,
  Badge,
  Loader,
  Alert,
  Tooltip,
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
import MetricCard from "../components/MetricCard";
import ConfusionMatrixCard from "../components/ConfusionMatrixCard";
import { useDashboard } from "../hooks/useDashboard";

ChartJS.register(CategoryScale, LinearScale, BarElement, ChartTooltip, Legend);

export default function DashboardPage() {
  const { data, error, loading } = useDashboard();

  if (error)
    return (
      <Alert color="red" title="Errore">
        {error}
      </Alert>
    );
  if (loading || !data) return <Loader m="xl" />;

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
            Miglior Reparto: {data.model_info.best_department_model}
          </Badge>
          <Badge color="yellow" variant="light" size="lg">
            Miglior Sentiment: {data.model_info.best_sentiment_model}
          </Badge>
        </Group>
      </Group>

      <SimpleGrid cols={{ base: 2, sm: 2, md: 4 }} mb="xl">
        <MetricCard
          label="Accuratezza Reparto"
          value={data.metrics.department_accuracy}
          color="#ff922b"
          tooltip="Percentuale di recensioni il cui reparto è stato classificato correttamente dal modello migliore"
        />
        <MetricCard
          label="Accuratezza Sentiment"
          value={data.metrics.sentiment_accuracy}
          color="#fcc419"
          tooltip="Percentuale di recensioni il cui sentiment è stato classificato correttamente dal modello migliore"
        />
        <MetricCard
          label="F1 Reparto"
          value={data.metrics.department_f1}
          color="#ff922b"
          tooltip="Media armonica di precisione e recall per la classificazione del reparto (bilancia falsi positivi e falsi negativi)"
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
            Classificazione Reparto
          </Title>
          <Text size="sm" c="dimmed" mb="md">
            Confronto tra i modelli addestrati per la classificazione del
            reparto
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
          title="Matrice di Confusione — Reparto"
          tooltip={`Matrice calcolata sul modello ${data.model_info.best_department_model}. Le righe indicano la classe reale, le colonne la classe predetta. I valori sulla diagonale (verde) sono le predizioni corrette.`}
          matrix={data.confusion_matrix.department}
          labels={data.confusion_matrix.labels_dept}
          modelName={data.model_info.best_department_model}
        />
        <ConfusionMatrixCard
          title="Matrice di Confusione — Sentiment"
          tooltip={`Matrice calcolata sul modello ${data.model_info.best_sentiment_model}. Le righe indicano la classe reale, le colonne la classe predetta. I valori sulla diagonale (verde) sono le predizioni corrette.`}
          matrix={data.confusion_matrix.sentiment}
          labels={data.confusion_matrix.labels_sent}
          modelName={data.model_info.best_sentiment_model}
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
