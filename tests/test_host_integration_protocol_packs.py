from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
PROTOCOLS = {
    "hermes": "https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes",
    "codex": "https://developers.openai.com/codex/mcp",
    "claude-code": "https://code.claude.com/docs/en/mcp-quickstart",
    "cursor": "https://cursor.com/docs/mcp",
    "openclaw": "https://docs.openclaw.ai/cli/mcp",
}


class HostIntegrationProtocolPackTests(unittest.TestCase):
    def test_every_host_has_a_documented_synthetic_non_mutating_protocol(self):
        for host, official_url in PROTOCOLS.items():
            path = ROOT / "docs" / "integrations" / f"{host}-synthetic-mcp-protocol.md"
            text = path.read_text(encoding="utf-8")
            for required in (
                "Status: Documented",
                "examples/demo-vault",
                "cited-vault-recall-mcp --vault",
                "Expected bounded evidence",
                "search",
                "Rollback",
                "Do not use a real vault",
                "No credentials",
                "No host configuration or connection is performed by this document",
                "Integration-tested",
                official_url,
            ):
                self.assertIn(required, text, f"{path}: missing {required!r}")

    def test_protocol_packs_do_not_promote_documentation_to_host_integration_evidence(self):
        for host in PROTOCOLS:
            text = (ROOT / "docs" / "integrations" / f"{host}-synthetic-mcp-protocol.md").read_text(encoding="utf-8")
            self.assertIn("Documentation-only protocol", text)
            self.assertIn("fresh explicit user approval", text)
            self.assertIn("owner-controlled", text)
            self.assertIn("not proof that the host loaded Cited Vault Recall", text)


if __name__ == "__main__":
    unittest.main()
