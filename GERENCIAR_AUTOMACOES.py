from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import unicodedata
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

TEMPLATE_REPO = "fabio-ara/VBA"
APP_DIR = Path(os.environ.get("APPDATA", Path.home())) / "VBA-Automacoes"
CONFIG_PATH = APP_DIR / "config.json"

LABELS = [
    ("type:feature", "1D76DB", "Nova funcionalidade ou alteração funcional"),
    ("type:bug", "D73A4A", "Defeito ou regressão"),
    ("type:tooling", "5319E7", "Infraestrutura de desenvolvimento e automação"),
    ("type:plan", "0E8A16", "Plano coordenador de implementação"),
    ("status:discussion", "FBCA04", "Ainda em discussão; não implementar"),
    ("status:ready", "0E8A16", "Pronta para implementação"),
    ("status:blocked", "B60205", "Bloqueada por dependência ou informação"),
    ("status:validation", "006B75", "Implementada e aguardando validação"),
]


def executar(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def exigir_ambiente() -> None:
    ausentes = [nome for nome in ("git", "gh") if shutil.which(nome) is None]
    if ausentes:
        raise RuntimeError("Não encontrado no PATH: " + ", ".join(ausentes))
    auth = executar(["gh", "auth", "status"])
    if auth.returncode != 0:
        raise RuntimeError("O GitHub CLI não está autenticado. Autentique-o uma vez e abra novamente o gerenciador.")


def login_atual() -> str:
    resultado = executar(["gh", "api", "user", "--jq", ".login"])
    if resultado.returncode != 0:
        raise RuntimeError(resultado.stderr.strip() or "Não foi possível identificar a conta GitHub.")
    return resultado.stdout.strip()


def normalizar_nome(valor: str) -> str:
    texto = unicodedata.normalize("NFKD", valor)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = texto.strip().replace(" ", "-")
    texto = re.sub(r"[^A-Za-z0-9._-]+", "-", texto)
    texto = re.sub(r"-{2,}", "-", texto).strip("-._")
    return texto[:100]


def carregar_config() -> dict:
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def salvar_config(dados: dict) -> None:
    APP_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")


def garantir_template() -> None:
    consulta = executar(["gh", "api", f"repos/{TEMPLATE_REPO}", "--jq", ".is_template"])
    if consulta.returncode != 0:
        raise RuntimeError(consulta.stderr.strip() or "Não foi possível consultar o template.")
    if consulta.stdout.strip().lower() == "true":
        return
    if not messagebox.askyesno(
        "Preparar template",
        f"{TEMPLATE_REPO} ainda não está marcado como Template repository.\n\nConfigurar automaticamente agora?",
    ):
        raise RuntimeError("O repositório-base precisa estar marcado como template.")
    ajuste = executar([
        "gh", "api", f"repos/{TEMPLATE_REPO}", "-X", "PATCH",
        "-F", "is_template=true", "-F", "has_issues=true", "-F", "has_wiki=false",
    ])
    if ajuste.returncode != 0:
        raise RuntimeError(ajuste.stderr.strip() or "Falha ao configurar o template.")


def criar_labels(repo: str) -> None:
    for nome, cor, descricao in LABELS:
        resultado = executar([
            "gh", "label", "create", nome, "--repo", repo,
            "--color", cor, "--description", descricao, "--force",
        ])
        if resultado.returncode != 0:
            raise RuntimeError(resultado.stderr.strip() or f"Falha ao criar label {nome}.")


def escrever_readme(pasta: Path, nome: str, descricao: str) -> None:
    linhas = [f"# {nome}", ""]
    if descricao.strip():
        linhas += [descricao.strip(), ""]
    linhas += [
        "Automação VBA com GitHub como fonte de verdade do código e da documentação.", "",
        "## Continuidade", "",
        "- `AGENTS.md`: protocolo obrigatório para agentes.",
        "- `docs/SPEC.md`: regras de negócio e comportamento normativo.",
        "- `docs/WORKBOOK.md`: estrutura confirmada da pasta de trabalho.",
        "- `docs/ARCHITECTURE.md`: arquitetura e contratos técnicos.",
        "- GitHub Issues: backlog executável, bugs e histórico das unidades de trabalho.", "",
        "O XLSM permanece local e não é versionado.", "",
    ]
    (pasta / "README.md").write_text("\n".join(linhas), encoding="utf-8")


def inicializar_projeto(repo: str, pasta: Path, nome: str, descricao: str, manter_mit: bool) -> None:
    gerenciador = pasta / "GERENCIAR_AUTOMACOES.py"
    if gerenciador.exists():
        gerenciador.unlink()
    if not manter_mit:
        licenca = pasta / "LICENSE"
        if licenca.exists():
            licenca.unlink()
    escrever_readme(pasta, nome, descricao)
    executar(["git", "add", "-A"], pasta)
    diferencas = executar(["git", "diff", "--cached", "--quiet"], pasta)
    if diferencas.returncode != 0:
        commit = executar(["git", "commit", "-m", "chore: initialize project from VBA template"], pasta)
        if commit.returncode != 0:
            raise RuntimeError(commit.stderr.strip() or "Falha no commit de inicialização.")
        push = executar(["git", "push", "origin", "main"], pasta)
        if push.returncode != 0:
            raise RuntimeError(push.stderr.strip() or "Falha no push da inicialização.")


def escolher_pasta(variavel: tk.StringVar) -> None:
    pasta = filedialog.askdirectory(initialdir=variavel.get() or str(Path.home()))
    if pasta:
        variavel.set(pasta)
        cfg = carregar_config()
        cfg["base_dir"] = pasta
        salvar_config(cfg)


def criar(parent: tk.Misc, nome_var: tk.StringVar, desc_var: tk.StringVar, vis_var: tk.StringVar,
          pasta_var: tk.StringVar, mit_var: tk.BooleanVar) -> None:
    try:
        exigir_ambiente()
        garantir_template()
        owner = login_atual()
        original = nome_var.get().strip()
        nome = normalizar_nome(original)
        if not nome:
            raise RuntimeError("Informe um nome válido.")
        if original != nome and not messagebox.askyesno(
            "Normalizar nome", f"O nome no GitHub será:\n\n{nome}\n\nContinuar?", parent=parent
        ):
            return
        base = Path(pasta_var.get()).expanduser()
        if not base.is_dir():
            raise RuntimeError("Escolha uma pasta local existente.")
        repo = f"{owner}/{nome}"
        if executar(["gh", "repo", "view", repo]).returncode == 0:
            raise RuntimeError(f"O repositório {repo} já existe.")
        visibilidade = "--private" if vis_var.get() == "private" else "--public"
        criado = executar([
            "gh", "repo", "create", repo, visibilidade,
            "--template", TEMPLATE_REPO, "--description", desc_var.get().strip(),
        ])
        if criado.returncode != 0:
            raise RuntimeError(criado.stderr.strip() or "Falha ao criar o repositório.")
        ajuste = executar([
            "gh", "api", f"repos/{repo}", "-X", "PATCH",
            "-F", "has_issues=true", "-F", "has_wiki=false",
        ])
        if ajuste.returncode != 0:
            raise RuntimeError(ajuste.stderr.strip() or "Falha ao ajustar o repositório.")
        criar_labels(repo)
        destino = base / nome
        if destino.exists():
            raise RuntimeError(f"O remoto foi criado, mas a pasta local já existe:\n{destino}")
        clone = executar(["gh", "repo", "clone", repo, str(destino)])
        if clone.returncode != 0:
            raise RuntimeError("O remoto foi criado, mas o clone falhou.\n\n" + clone.stderr.strip())
        inicializar_projeto(repo, destino, nome, desc_var.get(), bool(mit_var.get()))
        cfg = carregar_config()
        cfg["base_dir"] = str(base)
        salvar_config(cfg)
        messagebox.showinfo("Automação criada", f"{repo}\n\nCópia local:\n{destino}", parent=parent)
        nome_var.set("")
        desc_var.set("")
    except Exception as exc:
        messagebox.showerror("Erro", str(exc), parent=parent)


def listar_repos(owner: str) -> list[str]:
    resultado = executar([
        "gh", "repo", "list", owner, "--limit", "500",
        "--json", "nameWithOwner,isArchived",
        "--jq", ".[] | select(.isArchived == false) | .nameWithOwner",
    ])
    if resultado.returncode != 0:
        raise RuntimeError(resultado.stderr.strip() or "Falha ao listar repositórios.")
    return sorted((x.strip() for x in resultado.stdout.splitlines() if x.strip()), key=str.lower)


def atualizar_lista(combo: ttk.Combobox) -> None:
    try:
        exigir_ambiente()
        repos = [r for r in listar_repos(login_atual()) if r != TEMPLATE_REPO]
        combo["values"] = repos
        if repos:
            combo.set(repos[0])
    except Exception as exc:
        messagebox.showerror("Erro", str(exc))


def autorizar_exclusao() -> bool:
    flags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
    resultado = subprocess.run(
        ["gh", "auth", "refresh", "-h", "github.com", "-s", "delete_repo"],
        creationflags=flags,
        check=False,
    )
    return resultado.returncode == 0


def excluir(parent: tk.Misc, combo: ttk.Combobox, local_var: tk.BooleanVar, pasta_var: tk.StringVar) -> None:
    try:
        exigir_ambiente()
        repo = combo.get().strip()
        if not repo:
            raise RuntimeError("Selecione um repositório.")
        if repo == TEMPLATE_REPO:
            raise RuntimeError("O repositório-modelo é protegido por esta ferramenta.")
        nome = repo.split("/", 1)[1]
        digitado = simpledialog.askstring(
            "Confirmação destrutiva",
            f"Excluir permanentemente:\n\n{repo}\n\nDigite exatamente {nome} para confirmar:",
            parent=parent,
        )
        if digitado != nome:
            messagebox.showinfo("Cancelado", "Exclusão cancelada.", parent=parent)
            return
        resultado = executar(["gh", "repo", "delete", repo, "--yes"])
        if resultado.returncode != 0 and ("delete_repo" in resultado.stderr or "scope" in resultado.stderr.lower()):
            messagebox.showinfo(
                "Autorizar exclusão",
                "Será aberta a autenticação do GitHub para conceder a permissão de exclusão. Conclua o fluxo e retorne.",
                parent=parent,
            )
            if not autorizar_exclusao():
                raise RuntimeError("A autorização de exclusão não foi concluída.")
            resultado = executar(["gh", "repo", "delete", repo, "--yes"])
        if resultado.returncode != 0:
            raise RuntimeError(resultado.stderr.strip() or "Falha ao excluir o repositório.")
        nota = ""
        if local_var.get():
            local = Path(pasta_var.get()).expanduser() / nome
            if local.is_dir() and (local / ".git").exists():
                shutil.rmtree(local)
                nota = f"\n\nPasta local removida:\n{local}"
        messagebox.showinfo("Excluído", f"Repositório remoto excluído:\n{repo}{nota}", parent=parent)
        atualizar_lista(combo)
    except Exception as exc:
        messagebox.showerror("Erro", str(exc), parent=parent)


def main() -> None:
    root = tk.Tk()
    root.title("VBA - Gerenciador de automações")
    root.minsize(650, 470)
    cfg = carregar_config()
    base_padrao = cfg.get("base_dir", str(Path.home() / "Documents"))
    nome = tk.StringVar()
    descricao = tk.StringVar()
    visibilidade = tk.StringVar(value="private")
    pasta = tk.StringVar(value=base_padrao)
    manter_mit = tk.BooleanVar(value=False)
    apagar_local = tk.BooleanVar(value=False)

    frame = ttk.Frame(root, padding=16)
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text="Automações VBA", font=("Segoe UI", 16, "bold")).pack(anchor="w")
    ttk.Label(frame, text=f"Template: {TEMPLATE_REPO}").pack(anchor="w", pady=(0, 12))
    abas = ttk.Notebook(frame)
    abas.pack(fill="both", expand=True)

    nova = ttk.Frame(abas, padding=16)
    remover = ttk.Frame(abas, padding=16)
    abas.add(nova, text="Criar automação")
    abas.add(remover, text="Excluir automação")

    ttk.Label(nova, text="Nome").grid(row=0, column=0, sticky="w")
    ttk.Entry(nova, textvariable=nome).grid(row=1, column=0, columnspan=3, sticky="ew", pady=(2, 10))
    ttk.Label(nova, text="Descrição (opcional)").grid(row=2, column=0, sticky="w")
    ttk.Entry(nova, textvariable=descricao).grid(row=3, column=0, columnspan=3, sticky="ew", pady=(2, 10))
    ttk.Radiobutton(nova, text="Privado", variable=visibilidade, value="private").grid(row=4, column=0, sticky="w")
    ttk.Radiobutton(nova, text="Público", variable=visibilidade, value="public").grid(row=4, column=1, sticky="w")
    ttk.Checkbutton(nova, text="Manter licença MIT", variable=manter_mit).grid(row=5, column=0, columnspan=3, sticky="w", pady=(4, 10))
    ttk.Label(nova, text="Pasta local dos repositórios").grid(row=6, column=0, sticky="w")
    ttk.Entry(nova, textvariable=pasta).grid(row=7, column=0, columnspan=2, sticky="ew")
    ttk.Button(nova, text="Escolher...", command=lambda: escolher_pasta(pasta)).grid(row=7, column=2, padx=(8, 0))
    ttk.Button(
        nova, text="Criar repositório e clone local",
        command=lambda: criar(root, nome, descricao, visibilidade, pasta, manter_mit),
    ).grid(row=8, column=0, columnspan=3, sticky="ew", pady=(18, 0))
    nova.columnconfigure(0, weight=1)
    nova.columnconfigure(1, weight=1)

    ttk.Label(remover, text="Repositório").grid(row=0, column=0, sticky="w")
    combo = ttk.Combobox(remover, state="readonly")
    combo.grid(row=1, column=0, sticky="ew", pady=(2, 10))
    ttk.Button(remover, text="Atualizar lista", command=lambda: atualizar_lista(combo)).grid(row=1, column=1, padx=(8, 0))
    ttk.Checkbutton(
        remover, text="Também remover o clone local correspondente", variable=apagar_local
    ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(4, 14))
    ttk.Button(
        remover, text="Excluir repositório selecionado",
        command=lambda: excluir(root, combo, apagar_local, pasta),
    ).grid(row=3, column=0, columnspan=2, sticky="ew")
    ttk.Label(
        remover,
        text="O template fabio-ara/VBA é protegido contra exclusão por esta ferramenta.",
        wraplength=540,
    ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(14, 0))
    remover.columnconfigure(0, weight=1)

    root.after(250, lambda: atualizar_lista(combo))
    root.mainloop()


if __name__ == "__main__":
    main()
