from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REQUIRED = {
    "AGENTS.md",
    "docs/SPEC.md",
    "docs/WORKBOOK.md",
    "docs/ARCHITECTURE.md",
    "docs/DEVELOPMENT.md",
    "ATUALIZAR.py",
}
FORBIDDEN_TRACKED = {".xls", ".xlsx", ".xlsm", ".xlsb", ".xlam", ".frx"}
EXPORT_HEADERS = ("attribute vb_", "version ", "begin ")


def tracked_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=root,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git ls-files falhou")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def first_code_line(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig", errors="strict")
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []

    for required in sorted(REQUIRED):
        if not (root / required).exists():
            errors.append(f"arquivo obrigatório ausente: {required}")

    try:
        tracked = tracked_files(root)
    except Exception as exc:
        print(f"ERRO: {exc}")
        return 2

    for rel in tracked:
        path = root / rel
        if path.suffix.lower() in FORBIDDEN_TRACKED:
            errors.append(f"binário Excel versionado indevidamente: {rel}")

        if path.suffix.lower() in {".bas", ".cls"} and path.is_file():
            try:
                first = first_code_line(path)
                lower = first.lower()
                if lower.startswith(EXPORT_HEADERS):
                    errors.append(f"cabeçalho de exportação VBE detectado: {rel}: {first}")
                if lower != "option explicit":
                    errors.append(f"primeira linha de código não é Option Explicit: {rel}: {first or '<vazio>'}")
            except UnicodeError:
                errors.append(f"fonte VBA não pôde ser lido como UTF-8: {rel}")

    if errors:
        print("VALIDAÇÃO: FALHOU")
        for error in errors:
            print(f"- {error}")
        return 1

    print("VALIDAÇÃO: OK")
    print(f"Arquivos rastreados verificados: {len(tracked)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
