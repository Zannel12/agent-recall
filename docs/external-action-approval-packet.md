# Пакет одобрения внешних действий

Это воспроизводимый формат финальной русской safety card. **No action is authorized by this document.**

## Правило актуальности снимка

Перед показом живой карточки факты **must be refreshed** новым B1 audit для точного candidate commit. В карточке обязаны быть:

```text
candidate commit
candidate version
artifact checksums
exact successful CI run
clean-tree / tracked-scope audit result
known limits and blockers
```

Даже документационное изменение может сделать старый снимок устаревшим. Если candidate изменился после B1, нужно повторить B1 audit до принятия любого одобрения.

## Default и валидность

```text
Default: DENY / no action
```

Каждое решение требует fresh explicit user approval непосредственно перед выполнением, действует для **exactly one** named action и истекает после завершения, ошибки или изменения scope. Одобрение одного пункта не переносится на другой.

Агент не запрашивает, не принимает, не сохраняет и не логирует credentials, tokens, passwords, recovery codes, browser state или 2FA. Если это требуется, owner completes authentication, account-role checks, legal acceptance, host configuration и подтверждение напрямую.

## Одноразовая safety card

Живая карточка показывает один из независимых пунктов ниже. `APPROVE <id>` допустимо только с приложенным актуальным снимком; `DENY <id>` отменяет пункт. Совмещённого одобрения намеренно нет.

| ID и независимое действие | Риск / обязательные условия | Явный ответ |
|---|---|---|
| C1 — dependency/action SHA pinning | Меняет supply-chain trust anchors; official upstream commit facts должны быть проверены независимо. | `APPROVE C1` / `DENY C1` |
| C2 — semantic/vector/LLM retrieval | Может приобрести dependencies/weights и изменить cost, storage и retrieval behavior; нужны A5 gate, model revision/hash, resource budget и opt-in границы. | `APPROVE C2` / `DENY C2` |
| C3 — real Hermes integration | Owner-controlled host configuration только на synthetic vault; нужен approved rollback. | `APPROVE C3` / `DENY C3` |
| C4 — one named Codex, Claude Code, Cursor, or OpenClaw integration | Только один host, только synthetic vault, owner-controlled configuration и host-specific rollback. | `APPROVE C4: <one host>` / `DENY C4` |
| C5 — production deployment evidence | Нужны defined operator, target, support boundary, privacy/retention plan, observability и rollback по A7 policy. | `APPROVE C5` / `DENY C5` |
| C6a — SBOM generation | Создаёт release evidence asset для exact reviewed artifacts; tag/release/upload этим не одобряются. | `APPROVE C6a` / `DENY C6a` |
| C6b — provenance attestation | Может требовать verified OIDC/workflow permissions и создаёт public claim; нужны exact artifacts. | `APPROVE C6b` / `DENY C6b` |
| C7a — Git tag | User-visible и трудно обратимое publication event; нужны exact commit/version. | `APPROVE C7a` / `DENY C7a` |
| C7b — GitHub Release | Нужен отдельно approved tag и reviewed assets; обязателен read-back URL/assets. | `APPROVE C7b` / `DENY C7b` |
| C8 — PyPI publication | Необратимое public registry event; обязательны immediate registry check и owner namespace/authentication confirmation. | `APPROVE C8` / `DENY C8` |

## Stop conditions

Остановиться, а не расширять scope, если нельзя проверить official reference, checksum, model revision, rollback path, target, host configuration, account/namespace ownership, OIDC permission, artifact identity или evidence read-back. Deny либо отсутствие ответа сохраняет repository unreleased и local-first.
