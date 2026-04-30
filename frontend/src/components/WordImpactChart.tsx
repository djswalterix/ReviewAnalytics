import { Badge, Card, Group, Title, Tooltip } from "@mantine/core";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip as ChartTooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(CategoryScale, LinearScale, BarElement, ChartTooltip, Legend);

interface WordImpactChartProps {
  title: string;
  tooltip: string;
  badgeLabel?: string;
  labels: string[];
  data: number[];
  backgroundColor: string[];
  xAxisTitle?: string;
  legend?: React.ReactNode;
}

export default function WordImpactChart({
  title,
  tooltip,
  badgeLabel = "Solo Logistic Regression ⓘ",
  labels,
  data,
  backgroundColor,
  xAxisTitle,
  legend,
}: WordImpactChartProps) {
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
            {badgeLabel}
          </Badge>
        </Tooltip>
      </Group>
      {legend}
      <Bar
        data={{
          labels,
          datasets: [
            {
              label: "Impatto",
              data,
              backgroundColor,
            },
          ],
        }}
        options={{
          indexAxis: "y",
          responsive: true,
          plugins: { legend: { display: false } },
          scales: {
            x: {
              ...(xAxisTitle
                ? { title: { display: true, text: xAxisTitle } }
                : {}),
              grid: { color: "rgba(0,0,0,0.04)" },
            },
            y: { grid: { display: false } },
          },
        }}
      />
    </Card>
  );
}
