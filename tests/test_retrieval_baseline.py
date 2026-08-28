import json
import unittest
from pathlib import Path

from cited_vault_recall.core import search_vault


BENCHMARK_ROOT = Path(__file__).resolve().parents[1] / "benchmarks" / "retrieval"


def _metrics(judgments: list[dict[str, object]]) -> dict[str, float]:
    recall_total = 0.0
    reciprocal_rank_total = 0.0

    for judgment in judgments:
        hits = search_vault(
            BENCHMARK_ROOT / "corpus",
            str(judgment["query"]),
            limit=int(judgment["k"]),
        )
        paths = [hit.relative_path for hit in hits]
        expected = set(judgment["relevant_paths"])
        recall_total += len(expected.intersection(paths)) / len(expected)
        for rank, path in enumerate(paths, 1):
            if path in expected:
                reciprocal_rank_total += 1 / rank
                break

    count = len(judgments)
    return {
        "recall_at_k": round(recall_total / count, 3),
        "mrr": round(reciprocal_rank_total / count, 3),
    }


class RetrievalBaselineTests(unittest.TestCase):
    def test_current_retriever_matches_recorded_multilingual_baseline(self):
        judgments = json.loads((BENCHMARK_ROOT / "judgments.json").read_text(encoding="utf-8"))
        expected = json.loads((BENCHMARK_ROOT / "baseline.json").read_text(encoding="utf-8"))

        self.assertEqual(expected["metrics"], _metrics(judgments["queries"]))
        self.assertEqual("synthetic", judgments["dataset"])
        self.assertEqual("lexical-v0.1.0", expected["retriever"])


if __name__ == "__main__":
    unittest.main()
