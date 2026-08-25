## Summary

## Contract and boundary check

- [ ] Keeps selected-vault, local-first, read-only behavior by default.
- [ ] Adds no network access, telemetry, LLM/API call, credential handling, or automatic vault write.
- [ ] Does not expose absolute vault paths or private data.
- [ ] Documents copied/adapted code in `UPSTREAMS.md` and `ADAPTATIONS.md`, if applicable.

## Verification

- [ ] Added/updated a behavior test before production behavior.
- [ ] `PYTHONPATH=src python3 -m unittest discover -s tests -v` passes.
- [ ] `git diff --check` passes.

## Evidence

<!-- Include synthetic reproduction/evaluation evidence. Do not paste real vault data, credentials, machine paths, or agent configuration. -->
