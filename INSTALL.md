# Installation contract

## Supported: POSIX shell (verified)

Requires Python 3.10+ and a POSIX-compatible shell.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
cited-vault-recall doctor --vault /absolute/path/to/vault --json
```

The doctor command must report `status: "READY"`, `install.code: "READY"`, `vault.code: "READY"`, `search.code: "READY"`, and `local_state.discovered: false`. It reports aggregate readiness only and never prints the supplied absolute vault path.

## Windows PowerShell (documented, not executed in this Linux CI)

Requires Python 3.10+ and PowerShell 5.1+ or PowerShell 7+.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install .
cited-vault-recall doctor --vault C:\absolute\path\to\vault --json
```

This repository's CI does not execute PowerShell. The command sequence is documented as a manual verification contract, not a claim of automated Windows validation.

## Unsupported / intentionally absent

- Python older than 3.10.
- Automatic discovery of a vault, home directory, or agent state.
- Network installation claims, hosted service, telemetry, or automatic vault writes.
