import { Badge, Card, Text, Title, Tooltip } from "@mantine/core";

interface ConfusionMatrixCardProps {
  title: string;
  tooltip: string;
  matrix: number[][];
  labels: string[];
}

export default function ConfusionMatrixCard({
  title,
  tooltip,
  matrix,
  labels,
}: ConfusionMatrixCardProps) {
  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      <Title order={3} size="h4" mb={4}>
        {title}
      </Title>
      <Tooltip label={tooltip} multiline w={300} withArrow>
        <Badge
          variant="light"
          color="gray"
          size="sm"
          mb="md"
          style={{ cursor: "help" }}
        >
          Solo Logistic Regression ⓘ
        </Badge>
      </Tooltip>
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
