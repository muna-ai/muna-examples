import gdot from "@stdlib/blas-base-gdot"
import type { Embedding } from "muna"

export interface SplitDocumentInput {
  document: string;
  separators?: string[];
}

export interface FindClosestEmbeddingInput {
  query: Embedding;
  database: Embedding[];
}

export function splitDocument({
  document,
  separators = [".", "?"]
}: SplitDocumentInput): string[] {
  const separatorPattern = new RegExp(`[${separators.join("")}]`, "g");
  const documentLines = document.split("\n");
  const documentWithoutNewlines = documentLines.join(" ");
  const documents = documentWithoutNewlines
    .split(separatorPattern)
    .map(p => p.trim())
    .filter(p => p);
  return documents;
}

export function findClosestEmbedding({ // topk with k=1
  query,
  database
}: FindClosestEmbeddingInput): Embedding {
  const scores = database.map(({ embedding }) => gdot(query.embedding.length, query.embedding, 1, embedding, 1));
  const bestIdx = scores.reduce(
    (maxIdx, currentValue, currentIndex, array) => currentValue > array[maxIdx] ? currentIndex : maxIdx,
    0
  );
  return database[bestIdx];
}