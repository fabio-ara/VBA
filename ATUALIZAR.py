from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def executar(repo: Path, *args: str, capturar: bool = False) -> subprocess.CompletedProcess[str]:
    kwargs: dict[str, object] = {
        "cwd": str(repo),
        "text": True,
        "encoding": "utf-8",
        "errors": "replace",
        "check": False,
    }
    if capturar:
        kwargs["stdout"] = subprocess.PIPE
        kwargs["stderr"] = subprocess.PIPE
    return subprocess.run(["git", *args], **kwargs)


def branch_remoto(repo: Path) -> str:
    resultado = executar(repo, "ls-remote", "--symref", "origin", "HEAD", capturar=True)
    if resultado.returncode == 0:
        for linha in resultado.stdout.splitlines():
            if linha.startswith("ref: refs/heads/") and linha.endswith("\tHEAD"):
                return linha.split("refs/heads/", 1)[1].split("\t", 1)[0]
    return "main"


def main() -> int:
    repo = Path(__file__).resolve().parent

    if shutil.which("git") is None:
        print("ERRO: o Git não foi encontrado no PATH.")
        return 1
    if not (repo / ".git").exists():
        print(f"ERRO: esta pasta não parece ser um repositório Git: {repo}")
        return 1

    branch = branch_remoto(repo)
    print("=" * 56)
    print("ATUALIZANDO PELO GITHUB")
    print("=" * 56)
    print(f"Repositório: {repo}")
    print(f"Referência: origin/{branch}")
    print()

    fetch = executar(repo, "fetch", "origin", branch)
    if fetch.returncode != 0:
        print("\nERRO: git fetch falhou.")
        return fetch.returncode or 1

    reset = executar(repo, "reset", "--hard", f"origin/{branch}")
    if reset.returncode != 0:
        print("\nERRO: git reset falhou.")
        return reset.returncode or 1

    print()
    print("=" * 56)
    print("ATUALIZAÇÃO CONCLUÍDA")
    print("=" * 56)
    print("Os arquivos versionados locais correspondem ao branch remoto corrente.")
    print("Arquivos ignorados e não rastreados, como o XLSM, não foram removidos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
