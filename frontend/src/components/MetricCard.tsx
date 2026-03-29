import { Card, Group, RingProgress, Stack, Text, Tooltip } from "@mantine/core";

interface MetricCardProps {
  label: string;
  value: number;
  color: string;
  tooltip: string;
}

export default function MetricCard({
  label,
  value,
  color,
  tooltip,
}: MetricCardProps) {
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
