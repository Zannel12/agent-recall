from __future__ import annotations

import unittest

from cited_vault_recall.capabilities import (
    RetrievalMode,
    TransportMode,
    choose_retrieval_mode,
    choose_transport_mode,
)


class CapabilityNegotiationTests(unittest.TestCase):
    def test_transport_prefers_native_provider_without_degradation(self):
        choice = choose_transport_mode(
            {TransportMode.NATIVE_PROVIDER, TransportMode.MCP, TransportMode.CLI}
        )

        self.assertEqual(choice.selected, TransportMode.NATIVE_PROVIDER)
        self.assertTrue(choice.available)
        self.assertFalse(choice.degraded)
        self.assertIsNone(choice.reason)

    def test_transport_reports_explicit_fallback_to_cli(self):
        choice = choose_transport_mode({TransportMode.CLI})

        self.assertEqual(choice.selected, TransportMode.CLI)
        self.assertTrue(choice.available)
        self.assertTrue(choice.degraded)
        self.assertEqual(choice.reason, "native_provider_unavailable,mcp_unavailable")

    def test_transport_reports_unavailable_without_substitution(self):
        choice = choose_transport_mode(set())

        self.assertIsNone(choice.selected)
        self.assertFalse(choice.available)
        self.assertFalse(choice.degraded)
        self.assertEqual(choice.reason, "no_transport_available")

    def test_retrieval_reports_explicit_fallback_to_deterministic_lexical(self):
        choice = choose_retrieval_mode({RetrievalMode.LEXICAL})

        self.assertEqual(choice.selected, RetrievalMode.LEXICAL)
        self.assertTrue(choice.available)
        self.assertTrue(choice.degraded)
        self.assertEqual(choice.reason, "hybrid_unavailable,sparse_unavailable")


if __name__ == "__main__":
    unittest.main()
