import {
  Badge,
  Card,
  Group,
  Progress,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import type { PredictionResult } from "../api";

interface PredictionCardProps {
  title: string;
  predictions: PredictionResult[];
  colorFn: (prediction: PredictionResult) => string;
  labelFn?: (prediction: string) => string;
}

export default function PredictionCard({
  title,
  predictions,
  colorFn,
  labelFn,
}: PredictionCardProps) {
  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      <Title order={3} mb="md" size="h4">
        {title}
      </Title>
      <Stack gap="sm">
        {predictions.map((p) => {
          const color = colorFn(p);
          const displayLabel = labelFn ? labelFn(p.prediction) : p.prediction;
          return (
            <div key={p.model}>
              <Group justify="space-between" mb={4}>
                <Text size="sm" fw={500}>
                  {p.model}
                </Text>
                <Badge color={color} variant="light" size="sm">
                  {displayLabel}
                </Badge>
              </Group>
              {p.confidence !== null ? (
                <Group gap="xs" align="center">
                  <Progress
                    value={p.confidence * 100}
                    color={color}
                    size="sm"
                    radius="xl"
                    style={{ flex: 1 }}
                  />
                  <Text
                    size="xs"
                    c="dimmed"
                    ta="right"
                    style={{ minWidth: 120 }}
                  >
                    {(p.confidence * 100).toFixed(1)}% (confidenza)
                  </Text>
                </Group>
              ) : (
                <Text size="xs" c="dimmed">
                  Confidenza N/D
                </Text>
              )}
            </div>
          );
        })}
      </Stack>
    </Card>
  );
}
