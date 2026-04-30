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
  FileInput,
  Table,
  ScrollArea,
  Progress,
} from "@mantine/core";
import type { BatchPredictionRow, PredictionResult } from "../api";
import PredictionCard from "../components/PredictionCard";
import WordImpactChart from "../components/WordImpactChart";
import { usePredict } from "../hooks/usePredict";
import { predictBatch } from "../api";

const BATCH_CHUNK_SIZE = 200;
const BATCH_MAX_CONCURRENCY = 5;

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
  const [batchFile, setBatchFile] = useState<File | null>(null);
  const [batchLoading, setBatchLoading] = useState(false);
  const [batchError, setBatchError] = useState<string | null>(null);
  const [batchRows, setBatchRows] = useState<BatchPredictionRow[]>([]);
  const [batchProgress, setBatchProgress] = useState<number>(0);
  const { result, error, loading, run } = usePredict();

  const handleSubmit = () => run(bodyInput, titleInput || undefined);

  const sentimentContributions = result?.sentiment_word_contributions ?? [];
  const departmentContributions = result?.department_word_contributions ?? [];

  const buildChunkFiles = (fileText: string, chunkSize: number): File[] => {
    const lines = fileText.split(/\r?\n/);
    if (lines.length < 2) {
      throw new Error("CSV vuoto o non valido");
    }

    const header = lines[0];
    const columns = header.split(",").map((c) => c.trim().replace(/^"|"$/g, "").toLowerCase());
    if (!columns.includes("body")) {
      throw new Error(`Colonna 'body' mancante. Colonne trovate: ${columns.join(", ")}`);
    }

    const dataRows = lines.slice(1).filter((line) => line.trim() !== "");
    if (dataRows.length === 0) {
      throw new Error("Nessuna riga dati trovata nel CSV");
    }

    const chunks: File[] = [];
    for (let i = 0; i < dataRows.length; i += chunkSize) {
      const chunkRows = dataRows.slice(i, i + chunkSize);
      const chunkCsv = [header, ...chunkRows].join("\n");
      chunks.push(
        new File(
          [chunkCsv],
          `batch_chunk_${Math.floor(i / chunkSize) + 1}.csv`,
          {
            type: "text/csv",
          },
        ),
      );
    }

    return chunks;
  };

  const handleBatchPredict = async () => {
    if (!batchFile) return;
    setBatchLoading(true);
    setBatchError(null);
    setBatchRows([]);
    setBatchProgress(0);

    try {
      const fileText = await batchFile.text();
      const chunkFiles = buildChunkFiles(fileText, BATCH_CHUNK_SIZE);

      setBatchProgress(0);

      const responses: Array<{
        chunkIndex: number;
        response: Awaited<ReturnType<typeof predictBatch>>;
      }> = [];

      for (
        let batchStart = 0;
        batchStart < chunkFiles.length;
        batchStart += BATCH_MAX_CONCURRENCY
      ) {
        const batch = chunkFiles
          .slice(batchStart, batchStart + BATCH_MAX_CONCURRENCY)
          .map((chunkFile, localIndex) => ({
            chunkFile,
            chunkIndex: batchStart + localIndex,
          }));

        const batchResponses = await Promise.all(
          batch.map(async ({ chunkFile, chunkIndex }) => {
            const response = await predictBatch(chunkFile);
            // Update progress on every completed chunk for smoother UI feedback.
            setBatchProgress((prev) =>
              Math.min(100, prev + 100 / chunkFiles.length),
            );
            return { chunkIndex, response };
          }),
        );

        responses.push(...batchResponses);
      }

      const ordered = responses.sort((a, b) => a.chunkIndex - b.chunkIndex);

      const mergedRows: BatchPredictionRow[] = [];
      let rowOffset = 0;
      for (const { response } of ordered) {
        const normalized = response.results.map((row) => ({
          ...row,
          row: row.row + rowOffset,
        }));
        mergedRows.push(...normalized);
        rowOffset += response.total_rows;
      }

      setBatchRows(mergedRows);
      setBatchProgress(100);
    } catch (e) {
      setBatchError(
        e instanceof Error ? e.message : "Errore batch sconosciuto",
      );
      setBatchProgress(0);
    } finally {
      setBatchLoading(false);
    }
  };

  const exportBatchResults = () => {
    if (batchRows.length === 0) return;

    const escapeCsv = (value: string) => `"${value.replace(/"/g, '""')}"`;
    const header = [
      "row",
      "title",
      "body",
      "reparto_consigliato",
      "modello_reparto",
      "probabilita_reparto",
      "sentiment",
      "modello_sentiment",
      "probabilita_sentiment",
      "predicted_at",
    ].join(",");

    const lines = batchRows.map((r) =>
      [
        r.row,
        escapeCsv(r.title ?? ""),
        escapeCsv(r.body),
        escapeCsv(r.reparto_consigliato),
        escapeCsv(r.modello_reparto),
        r.probabilita_reparto != null
          ? (r.probabilita_reparto * 100).toFixed(1)
          : "",
        escapeCsv(r.sentiment),
        escapeCsv(r.modello_sentiment),
        r.probabilita_sentiment != null
          ? (r.probabilita_sentiment * 100).toFixed(1)
          : "",
        escapeCsv(r.predicted_at),
      ].join(","),
    );

    const csv = [header, ...lines].join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");

    const link = document.createElement("a");
    link.href = url;
    link.download = `batch_predictions_${timestamp}.csv`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const downloadCsvTemplate = () => {
    const templateRows = [
      "title,body",
      '"Camera confortevole","La camera era pulita e il personale molto gentile."',
      '"Esperienza negativa","Reception lenta e colazione scarsa."',
    ];

    const csv = templateRows.join("\n");
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "template_batch_reviews.csv";
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <Container size="lg" py={{ base: "md", md: "xl" }}>
      <div>
        <Title order={1} mb={4} size="h2" style={{ letterSpacing: -0.5 }}>
          Predizione Recensione
        </Title>
        <Text size="sm" c="dimmed" mb="lg">
          Inserisci una recensione per analizzare reparto e sentiment
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
              title="Predizioni Reparto"
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
                title="Contributo Parole — Reparto"
                tooltip="Associazione di ogni parola al reparto, calcolata dai coefficienti del modello Logistic Regression. Ogni parola è assegnata al reparto dove ha l'impatto assoluto più forte."
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

      <Card shadow="sm" padding="lg" radius="md" withBorder mt="xl">
        <Stack gap="md">
          <div>
            <Title order={3} size="h4" mb={4}>
              Predizione Batch da CSV
            </Title>
            <Text size="sm" c="dimmed">
              Carica un CSV per ottenere reparto consigliato, sentiment e
              probabilita. Se non hai un file pronto, scarica il template.
            </Text>
          </div>

          <Group align="flex-end">
            <FileInput
              label="File CSV"
              placeholder="Seleziona file .csv"
              value={batchFile}
              onChange={setBatchFile}
              accept=".csv,text/csv"
              style={{ flex: 1 }}
            />
            <Button variant="default" onClick={downloadCsvTemplate}>
              Download Template CSV
            </Button>
            <Button
              onClick={handleBatchPredict}
              loading={batchLoading}
              color="orange"
            >
              Predici Batch
            </Button>
            <Button
              variant="light"
              color="yellow"
              onClick={exportBatchResults}
              disabled={batchRows.length === 0}
            >
              Export CSV
            </Button>
          </Group>

          {batchError && <Alert color="red">{batchError}</Alert>}
          {batchLoading && (
            <div>
              <Text size="sm" mb={6}>
                Elaborazione in corso...
              </Text>
              <Progress value={batchProgress} color="orange" radius="xl" />
            </div>
          )}

          {batchRows.length > 0 && (
            <>
              <Text size="sm">Righe processate: {batchRows.length}</Text>
              <ScrollArea>
                <Table
                  striped
                  highlightOnHover
                  withTableBorder
                  withColumnBorders
                >
                  <Table.Thead>
                    <Table.Tr>
                      <Table.Th>#</Table.Th>
                      <Table.Th>Testo</Table.Th>
                      <Table.Th>Reparto Consigliato</Table.Th>
                      <Table.Th>Modello Reparto</Table.Th>
                      <Table.Th>Prob. Reparto</Table.Th>
                      <Table.Th>Sentiment</Table.Th>
                      <Table.Th>Modello Sentiment</Table.Th>
                      <Table.Th>Prob. Sentiment</Table.Th>
                      <Table.Th>Timestamp</Table.Th>
                    </Table.Tr>
                  </Table.Thead>
                  <Table.Tbody>
                    {batchRows.map((row) => (
                      <Table.Tr key={`${row.row}-${row.predicted_at}`}>
                        <Table.Td>{row.row}</Table.Td>
                        <Table.Td style={{ maxWidth: 260 }}>
                          <div style={{ maxHeight: 80, overflowY: "auto", wordBreak: "break-word", fontSize: 12 }}>
                            {row.body}
                          </div>
                        </Table.Td>
                        <Table.Td>{row.reparto_consigliato}</Table.Td>
                        <Table.Td>{row.modello_reparto}</Table.Td>
                        <Table.Td>
                          {row.probabilita_reparto != null
                            ? `${(row.probabilita_reparto * 100).toFixed(1)}%`
                            : "-"}
                        </Table.Td>
                        <Table.Td>
                          {row.sentiment === "Positive"
                            ? "Positivo"
                            : "Negativo"}
                        </Table.Td>
                        <Table.Td>{row.modello_sentiment}</Table.Td>
                        <Table.Td>
                          {row.probabilita_sentiment != null
                            ? `${(row.probabilita_sentiment * 100).toFixed(1)}%`
                            : "-"}
                        </Table.Td>
                        <Table.Td>
                          {new Date(row.predicted_at).toLocaleString()}
                        </Table.Td>
                      </Table.Tr>
                    ))}
                  </Table.Tbody>
                </Table>
              </ScrollArea>
            </>
          )}
        </Stack>
      </Card>
    </Container>
  );
}
