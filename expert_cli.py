# -*- coding: utf-8 -*-
"""

Uso:
  python expert_cli.py ejemplo.py
  @"<código multilínea>"@ | python expert_cli.py
  "if x > 0`n    print('ok')" | python expert_cli.py
  python expert_cli.py --error "TypeError: can't concatenate str and int"
  python expert_cli.py ejemplo.py --debug
"""
import os, sys, re, argparse, ast
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

# --------- CONFIG BD (ajusta a tu base de datos) ----------
DB_HOST = os.getenv("SBC_DB_HOST", "127.0.0.1")
DB_NAME = os.getenv("SBC_DB_NAME", "sbc_python")
DB_USER = os.getenv("SBC_DB_USER", "root")
DB_PASS = os.getenv("SBC_DB_PASS", "1234")

# --------- MODELOS ----------
@dataclass
class ErrorType:
    id: int
    name: str
    category: str
    severity: int
    explanation: str
    suggestion: str

@dataclass
class Rule:
    id: int
    name: str
    kind: str                  # "code" | "message"
    pattern_regex: str
    conclusion_error_type_id: int
    diag_text: str
    priority: int
    pattern: re.Pattern = None # regex compilada

# --------- helpers NUEVOS (post-fix y runtime seguro) ----------
_HEADER_RE = re.compile(r'^\s*(if|for|while|def|class)\b(.*)$')

def progressive_fixes(code: str) -> str:
    """
    Reparaciones mínimas para permitir análisis posterior:
    - Agrega ':' al final de encabezados (if/for/while/def/class) si falta.
    No toca indentación u otras cosas para evitar falsos positivos grandes.
    """
    fixed = []
    for line in code.splitlines():
        if _HEADER_RE.match(line) and not line.rstrip().endswith(':'):
            fixed.append(line.rstrip() + ':')
        else:
            fixed.append(line)
    return '\n'.join(fixed)

def safe_exec_and_capture(code: str, debug: bool=False) -> Optional[str]:
    """
    Ejecuta el código en un entorno vacío y captura el PRIMER error de runtime.
     Úsalo solo con código educativo/confiable.
    """
    try:
        exec(code, {})
        return None
    except Exception as e:
        msg = f"{type(e).__name__}: {e}"
        if debug:
            print(f"[DEBUG] Excepción en ejecución: {msg}")
        return msg

# --------- CARGA DE CONOCIMIENTO DESDE MYSQL ----------
def load_kb_from_mysql(debug: bool=False):
    import mysql.connector as mc
    conn = mc.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT id, name, category, severity, explanation, suggestion FROM error_type")
    ets = [ErrorType(**row) for row in cur.fetchall()]

    cur.execute("""
        SELECT id, name, kind, pattern_regex, conclusion_error_type_id, diag_text, priority
        FROM rule
        ORDER BY priority ASC, id ASC
    """)
    rrows = cur.fetchall()
    rules: List[Rule] = []
    for row in rrows:
        try:
            pat = re.compile(row["pattern_regex"], re.MULTILINE | re.IGNORECASE)
        except re.error as e:
            if debug:
                print(f"[DEBUG] Regex inválida en regla '{row['name']}': {e}  -> {row['pattern_regex']}", file=sys.stderr)
            continue
        rules.append(Rule(pattern=pat, **row))

    cur.close(); conn.close()

    if debug:
        print(f"[DEBUG] Cargados {len(ets)} tipos de error y {len(rules)} reglas desde MySQL ({DB_NAME}).")
        for r in rules:
            print(f"[DEBUG] Regla {r.id} {r.name} [{r.kind}] / {r.pattern_regex}")

    return {et.id: et for et in ets}, rules

# --------- INFERENCIA ----------


    # 1) Reglas sobre mensaje (externo)
    if errmsg:
        for r in rules:
            if r.kind == "message" and r.pattern.search(errmsg):
                et = error_types[r.conclusion_error_type_id]
                findings.append(build_finding(r, et, errmsg.strip()))

    # 2) Intentar parsear para capturar mensaje de SyntaxError del parser
    syntax_msg = None
    if code.strip():
        try:
            ast.parse(code)
        except SyntaxError as e:
            syntax_msg = str(e)
            if debug:
                print(f"[DEBUG] SyntaxError del parser: {syntax_msg}")

    # Reusar reglas de 'message' contra syntax_msg
    if syntax_msg:
        for r in rules:
            if r.kind == "message" and r.pattern.search(syntax_msg):
                et = error_types[r.conclusion_error_type_id]
                findings.append(build_finding(r, et, syntax_msg))

    # 3) Reglas estáticas sobre el código (texto)
    if code.strip():
        for r in rules:
            if r.kind == "code" and r.pattern.search(code):
                et = error_types[r.conclusion_error_type_id]
                findings.append(build_finding(r, et, "coincidencia de patrón en el código"))

    # === 4) PASADA PROGRESIVA + RUNTIME (para descubrir más errores) ===
    # Activada si:
    #   - está permitido enable_runtime
    #   - y detectamos indicios de ":" faltante (por regla de código o por mensaje del parser)
    if enable_runtime and code.strip():
        hubo_faltantes = any(
            (f["regla"] in {"IfSinDosPuntos","ForSinDosPuntos","WhileSinDosPuntos","DefSinDosPuntos","ClassSinDosPuntos"}
             or ("expected ':'" in f.get("evidencia","")))
            for f in findings
        )

        # Intento 1: si ya compila, ejecutemos tal cual
        if syntax_msg is None:
            runtime_msg = safe_exec_and_capture(code, debug=debug)
            if runtime_msg:
                for r in rules:
                    if r.kind == "message" and r.pattern.search(runtime_msg):
                        et = error_types[r.conclusion_error_type_id]
                        findings.append(build_finding(r, et, runtime_msg))

        # Intento 2: si hubo ":" faltantes, reparamos mínimamente y reintentamos
        if hubo_faltantes:
            code_fixed = progressive_fixes(code)
            try:
                ast.parse(code_fixed)
                runtime_msg2 = safe_exec_and_capture(code_fixed, debug=debug)
                if runtime_msg2:
                    for r in rules:
                        if r.kind == "message" and r.pattern.search(runtime_msg2):
                            et = error_types[r.conclusion_error_type_id]
                            f = build_finding(r, et, runtime_msg2)
                            # marcar que vino tras una reparación mínima
                            f["diagnostico"] = f["diagnostico"] + " (post-fix)"
                            findings.append(f)
            except SyntaxError as e2:
                if debug:
                    print(f"[DEBUG] Aún no compila tras post-fix: {e2}")

    # Orden + dedup
    findings.sort(key=lambda f: (f["categoria"], f["error"], f["regla"]))
    uniq, seen = [], set()
    for f in findings:
        k = (f["regla"], f["error"], f["evidencia"])
        if k not in seen:
            seen.add(k); uniq.append(f)

    if debug:
        print(f"[DEBUG] findings={len(uniq)}")
    return uniq

def build_finding(rule: Rule, et: ErrorType, evidence: str) -> Dict[str, Any]:
    return {
        "regla": rule.name,
        "error": et.name,
        "categoria": et.category,
        "diagnostico": rule.diag_text,
        "explicacion": et.explanation,
        "sugerencia": et.suggestion,
        "evidencia": evidence
    }

# --------- IO/CLI ----------
def read_code_from_stdin_if_any() -> str:
    return "" if sys.stdin.isatty() else sys.stdin.read()

def main():
    ap = argparse.ArgumentParser(description="Diagnóstico de errores Python (educativo) — MySQL")
    ap.add_argument("file", nargs="?", help="Archivo .py a analizar")
    ap.add_argument("--error", "-e", help="Mensaje de error del intérprete (opcional)")
    ap.add_argument("--debug", action="store_true", help="Mostrar info de depuración")
    ap.add_argument("--no-runtime", action="store_true",
                    help="Desactiva la ejecución segura (no captura errores de runtime).")
    args = ap.parse_args()

    code = ""
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            code = f.read()
    else:
        code = read_code_from_stdin_if_any()

    errmsg = (args.error or "").strip()

    if not code and not errmsg:
        print(" No recibí código ni mensaje de error.\n"
              "Modos de uso:\n"
              "  1) python expert_cli.py tu_archivo.py\n"
              "  2) @\"<código>\"@ | python expert_cli.py   (here-string de PowerShell)\n"
              "  3) \"if x > 0`n    print('ok')\" | python expert_cli.py\n"
              "  4) python expert_cli.py --error \"TypeError: can't concatenate str and int\"")
        sys.exit(1)

    error_types, rules = load_kb_from_mysql(debug=args.debug)
    results = infer(code, errmsg, error_types, rules,
                    debug=args.debug, enable_runtime=not args.no_runtime)

    if not results:
        print("No se detectaron errores según las reglas actuales.")
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
