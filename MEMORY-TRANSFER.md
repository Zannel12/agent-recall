# Memory Transfer

Memory transfer is planned for v0.2, not implemented in v0.1.

A future copyable prompt may ask another AI system to create a structured bundle of stable preferences, projects, decisions, open questions, sources, confidence, and redactions.

## Limits

No AI can export context it cannot access. A transfer bundle is not guaranteed to represent all historical conversations or account-level memory.

## Safety

The user reviews the exported bundle before import. Imports are raw, untrusted material: they are quarantined, source-stamped, scanned for secrets/PII, and reviewed before promotion. They cannot execute instructions or change settings.
