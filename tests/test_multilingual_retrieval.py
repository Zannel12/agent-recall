from __future__ import annotations

import json
import unittest
from pathlib import Path

from cited_vault_recall.core import search_vault


ROOT = Path(__file__).parents[1] / "benchmarks" / "retrieval"


def metrics(*, russian_lexical_expansion: bool) -> dict[str, float]:
    judgments = json.loads((ROOT / "multilingual-judgments.json").read_text(encoding="utf-8"))["queries"]
    recall = reciprocal_rank = 0.0
    for judgment in judgments:
        paths = [
            hit.relative_path
            for hit in search_vault(
                ROOT / "corpus",
                judgment["query"],
                judgment["k"],
                russian_lexical_expansion=russian_lexical_expansion,
            )
        ]
        relevant = set(judgment["relevant_paths"])
        recall += len(relevant.intersection(paths)) / len(relevant)
        for rank, path in enumerate(paths, 1):
            if path in relevant:
                reciprocal_rank += 1 / rank
                break
    count = len(judgments)
    return {"recall_at_k": round(recall / count, 3), "mrr": round(reciprocal_rank / count, 3)}


class MultilingualRetrievalTests(unittest.TestCase):
    def test_opt_in_russian_lexical_expansion_improves_the_recorded_synthetic_baseline(self):
        baseline = json.loads((ROOT / "multilingual-baseline.json").read_text(encoding="utf-8"))

        default = metrics(russian_lexical_expansion=False)
        expanded = metrics(russian_lexical_expansion=True)

        self.assertEqual(baseline["default_metrics"], default)
        self.assertEqual(baseline["expanded_metrics"], expanded)
        self.assertGreater(expanded["recall_at_k"], default["recall_at_k"])
        self.assertGreater(expanded["mrr"], default["mrr"])


if __name__ == "__main__":
    unittest.main()
