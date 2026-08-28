# ADR-0003: Freeze layered architecture and authority boundaries

- **Status:** accepted
- **Date:** 2026-08-24
- **Decision point:** B10.1

## Context

The shipped product is a local, read-only Markdown retriever: it parses selected Markdown, creates heading-aware chunks, ranks them with deterministic sparse scoring, and emits cited packets. It currently has no managed-memory store, persistent index, adapter server, or semantic layer.

Future roadmap points introduce those capabilities. Without explicit authority boundaries, a derived index, an agent adapter, or a future managed store could incorrectly become a second source of truth or bypass the local read-safe core.

## Decision

Cited Vault Recall uses six ordered layers. A lower layer may not silently acquire authority or wider access from a higher layer.

```text
curated source vault (canonical evidence)
        ↓ read-only
trusted retrieval core (parse → chunk → rank → cite)
        ↓ optional, rebuildable derivatives
managed store | derived index | optional semantic layer
        ↓ bounded interfaces only
adapters / CLI / MCP / host integrations
```

### 1. Curated source vault — canonical authority

- Human-controlled Markdown is the only canonical evidence source.
- It is selected explicitly by the caller; no discovery, network sync, or automatic mutation belongs here.
- A citation ultimately resolves to a source path and chunk/line anchor inside this layer.

### 2. Trusted retrieval core — current shipped core

- Reads selected source material, normalizes text, chunks Markdown, ranks sparse lexical results, and returns citations.
- Does not write curated material, call a network, execute source text, or treat retrieved text as instructions.
- Its output is evidence with scores and citations, not asserted durable fact.

### 3. Managed store — future, non-canonical lifecycle layer

- Holds only staged/approved derived-memory records after B06 governance controls exist.
- Each record requires immutable evidence back-links, explicit lifecycle state, and human-visible correction/deletion semantics.
- It never writes directly into curated Markdown and cannot replace a cited source as authority.

### 4. Derived index — future, disposable acceleration layer

- May cache metadata/chunks/search structures only when B07 benchmarks justify it.
- Is fully rebuildable from canonical inputs; it is never an authority for facts, provenance, or deletion.
- Index corruption or version mismatch must fail recoverably to direct sparse retrieval or rebuild.

### 5. Optional semantic layer — future, ranking-only layer

- Remains deferred under ADR-0001.
- If later accepted, it may rank candidates but must preserve chunk citations, operate locally/offline, be explicitly enabled, and fall back visibly to deterministic sparse retrieval.
- It may not create facts, alter sources, or hide degradation.

### 6. Adapters — bounded integration edge

- CLI, MCP, and host-specific adapters receive explicit user-requested scope and call the trusted core through versioned contracts.
- Adapters cannot perform arbitrary filesystem reads, bypass containment/policy checks, mutate curated sources, or promote memory without the governed lifecycle layer.

## Cross-layer invariants

1. **Authority flows upward only from cited canonical evidence.** Derived memory, indexes, semantic scores, and adapters are not source-of-truth replacements.
2. **Writes are separated from retrieval.** The current core stays read-only; any future write is staged, reviewable, and reversible.
3. **No hidden widening.** A layer cannot add network transfer, discovery, broader filesystem access, or an agent runtime dependency by implication.
4. **Provenance survives transformations.** Any future result or derived record must retain stable source/chunk citation identifiers defined by B10.2.
5. **Fallback is explicit.** Missing optional layers produce documented degraded behavior, never silent semantic or authority changes.

## Consequences

- B03 implements containment, limits, diagnostics, untrusted-content and sensitivity policy around the trusted core.
- B10.2 defines the canonical schemas that make the evidence/provenance invariant machine-readable.
- B05 adapters and B06 lifecycle work must conform to these boundaries.
- B07 indexing and any reopened semantic proposal must remain optional and rebuildable/non-authoritative.
