# -*- coding: utf-8 -*-
"""
expert_cli.py — Sistema Basado en Reglas (consola)
Entrada: código Python (por archivo o stdin) y/o mensaje de error (--error).
Salida: diagnóstico(s) con explicación y sugerencia.

Ejemplos:
  python expert_cli.py ejemplo.py
  echo "if x > 0\n    print('ok')" | python expert_cli.py
  python expert_cli.py --error "TypeError: can't concatenate str and int"
"""
import sys, re, argparse, ast
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

# ===== Conocimiento del dominio (tipos de error) =====
ERROR_TYPES: Dict[str, Dict[str, str]] = {
    "SyntaxError": {
        "category": "SINTAXIS",
        "explanation": "El código no sigue las reglas del lenguaje.",
        "suggestion": "Revisa ':' al final de if/for/while/def/class, paréntesis y comillas."
    },
    "IndentationError": {
        "category": "SINTAXIS",
        "explanation": "Indentación inválida o inconsistente.",
        "suggestion": "Usa 4 espacios por nivel y no mezcles tabs con espacios."
    },
    "TypeError": {
        "category": "SEMÁNTICO",
        "explanation": "Operación inválida entre tipos (str, int, etc.).",
        "suggestion": "Convierte tipos con int(), float(), str() cuando corresponda."
    },
}

# ===== Reglas (clasificación por patrones) =====
@dataclass
class Rule:
    name: str            # nombre de la regla
    kind: str            # "code" o "message"
    pattern: re.Pattern  # regex a detectar
    conclusion: str      # "SyntaxError" | "IndentationError" | "TypeError"
    diag_text: str       # explicación breve del diagnóstico

RULES: List[Rule] = [
    # Código: línea que empieza con 'if' y no termina con ':'
    Rule(
        name="IfSinDosPuntos",
        kind="code",
        pattern=re.compile(r"^\s*if\b[^\n:]*$", re.MULTILINE),
        conclusion="SyntaxError",
        diag_text="Se detectó una línea 'if' sin ':' al final."
    ),
    # Mensaje: Indentación
    Rule(
        name="MsgIndent",
        kind="message",
        pattern=re.compile(r"\bindent", re.IGNORECASE),
        conclusion="IndentationError",
        diag_text="El mensaje del intérprete indica un problema de indentación."
    ),
    # Mensaje: TypeError por concatenar str + int
    Rule(
        name="MsgTypeCatStrInt",
        kind="message",
        pattern=re.compile(r"can't concatenate str and int", re.IGNORECASE),
        conclusion="TypeError",
        diag_text="Concatenación entre str e int detectada en el mensaje."
    ),
    # Mensaje: CPython típico para colon faltante
    Rule(
        name="MsgExpectedColon",
        kind="message",
        pattern=re.compile(r"expected ':'", re.IGNORECASE),
        conclusion="SyntaxError",
        diag_text="El intérprete indica que falta ':'."
    ),
]

def run_inference(code: str, errmsg: Optional[str]) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []

    # 1) Reglas sobre mensaje externo (si viene)
    if errmsg:
        for r in RULES:
            if r.kind == "message" and r.pattern.search(errmsg):
                info = ERROR_TYPES[r.conclusion]
                findings.append({
                    "regla": r.name,
                    "error": r.conclusion,
                    "categoria": info["category"],
                    "diagnostico": r.diag_text,
                    "explicacion": info["explanation"],
                    "sugerencia": info["suggestion"],
                    "evidencia": errmsg.strip()
                })

    # 2) Intentar parsear para capturar SyntaxError y reusar reglas de mensaje
    syntax_msg = None
    if code.strip():
        try:
            ast.parse(code)
        except SyntaxError as e:
            syntax_msg = str(e)

    if syntax_msg:
        for r in RULES:
            if r.kind == "message" and r.pattern.search(syntax_msg):
                info = ERROR_TYPES[r.conclusion]
                findings.append({
                    "regla": r.name,
                    "error": r.conclusion,
                    "categoria": info["category"],
                    "diagnostico": r.diag_text,
                    "explicacion": info["explanation"],
                    "sugerencia": info["suggestion"],
                    "evidencia": syntax_msg
                })

    # 3) Reglas sobre el código (patrones estáticos)
    if code.strip():
        for r in RULES:
            if r.kind == "code" and r.pattern.search(code):
                info = ERROR_TYPES[r.conclusion]
                findings.append({
                    "regla": r.name,
                    "error": r.conclusion,
                    "categoria": info["category"],
                    "diagnostico": r.diag_text,
                    "explicacion": info["explanation"],
                    "sugerencia": info["suggestion"],
                    "evidencia": "coincidencia de patrón en el código"
                })

    # Orden simple + deduplicación
    findings.sort(key=lambda f: (f["categoria"], f["error"], f["regla"]))
    uniq, seen = [], set()
    for f in findings:
        k = (f["regla"], f["error"], f["evidencia"])
        if k not in seen:
            seen.add(k)
            uniq.append(f)
    return uniq

def read_code_from_stdin_if_any() -> str:
    # Si viene por pipe/redirect, leer todo; si es TTY, devolver vacío
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""

def main():
    ap = argparse.ArgumentParser(description="Diagnóstico de errores Python (educativo) — consola")
    ap.add_argument("file", nargs="?", help="Archivo .py a analizar")
    ap.add_argument("--error", "-e", help="Mensaje de error del intérprete (opcional)")
    args = ap.parse_args()

    code = ""
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            code = f.read()
    else:
        code = read_code_from_stdin_if_any()

    errmsg = (args.error or "").strip()

    if not code and not errmsg:
        print("⚠️ No recibí código ni mensaje de error.\n"
              "Usa alguno de estos modos:\n"
              "  1) python expert_cli.py tu_archivo.py\n"
              "  2) echo \"if x > 0\\n    print('ok')\" | python expert_cli.py\n"
              "  3) python expert_cli.py --error \"TypeError: can't concatenate str and int\"")
        sys.exit(1)

    results = run_inference(code, errmsg)

    if not results:
        print("✅ No se detectaron errores según las reglas actuales.")
        sys.exit(0)

    print("=== Reporte de Diagnóstico ===")
    for i, r in enumerate(results, 1):
        print(f"\n#{i}. [{r['error']}] {r['diagnostico']}")
        print(f" Categoría:  {r['categoria']}")
        print(f" Explicación: {r['explicacion']}")
        print(f" Sugerencia:  {r['sugerencia']}")
        print(f" Evidencia:   {r['evidencia']}")

if __name__ == "__main__":
    main()
