#!/usr/bin/env python3
import argparse, json, re, sys
from pathlib import Path
import urllib.request

# Ollama API (your custom port)
OLLAMA_URL = "http://localhost:11435/api/generate"

LANG_DEFAULTS = {
    "python": {"version": "3.12", "filename": "app.py"},
    "node":   {"version": "20",   "filename": "app.js"},
    "shell":  {"version": "3.18", "filename": "script.sh"},  # Alpine version
    "go":     {"version": "1.22", "filename": "main.go"},
}

def build_prompt(language, version, workdir, filename):
    if language == "python":
        base = f"python:{version}-slim"; cmd = f"python3 {filename}"
    elif language == "node":
        base = f"node:{version}-slim";   cmd = f"node {filename}"
    elif language == "shell":
        base = f"alpine:{version}";      cmd = f"sh {filename}"
    elif language == "go":
        base = f"golang:{version}-alpine"; cmd = f"go run {filename}"
    else:
        raise ValueError("Unsupported language")

    return f"""You are a DevOps assistant.
Output ONLY the Dockerfile content (no comments, no explanations, no backticks).
Constraints:
- Single-stage
- Minimal
- Base: {base}
- WORKDIR {workdir}
- COPY {filename} .
- Default command: {cmd}
"""

def call_ollama(model, prompt):
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps({"model": model, "prompt": prompt, "stream": False}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read().decode())
    return (data.get("response") or "").strip()

def clean_to_dockerfile(text: str) -> str:
    # Strip markdown code fences if present
    text = re.sub(r"^```[a-zA-Z0-9]*\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s*```$", "", text, flags=re.MULTILINE)
    # Keep from the first FROM line onward
    m = re.search(r"(?mi)^FROM\s+\S+.*$", text)
    if m:
        text = text[m.start():]
    return text.strip()

def main():
    ap = argparse.ArgumentParser(description="Generate a Dockerfile for ONE language into an existing folder.")
    ap.add_argument("--language", choices=["python", "node", "shell", "go"], required=True,
                    help="Language for this run (exactly one).")
    ap.add_argument("--app-dir", required=True,
                    help="Existing directory where Dockerfile will be created.")
    ap.add_argument("--version", help="Language version (defaults per language).")
    ap.add_argument("--filename", help="Entry file name (defaults per language).")
    ap.add_argument("--workdir", default="/app", help="Workdir inside container (default: /app).")
    ap.add_argument("--model", default="llama3.1", help="Ollama model to use (default: llama3.1).")
    ap.add_argument("--out", default="Dockerfile", help="Output file name (default: Dockerfile).")
    ap.add_argument("--force", action="store_true", help="Overwrite existing Dockerfile if present.")
    args = ap.parse_args()

    # Validate existing folder (do NOT create new)
    app_dir = Path(args.app_dir).resolve()
    if not app_dir.is_dir():
        print(f"Error: directory {app_dir} does not exist.", file=sys.stderr)
        sys.exit(4)

    # Defaults per language
    defaults = LANG_DEFAULTS[args.language]
    version = args.version or defaults["version"]

    # Always send only the basename to the model so COPY is like 'COPY app.py .'
    filename = Path(args.filename or defaults["filename"]).name

    out_path = app_dir / args.out
    if out_path.exists() and not args.force:
        print(f"Error: {out_path} already exists. Use --force to overwrite.", file=sys.stderr)
        sys.exit(3)

    prompt = build_prompt(args.language, version, args.workdir, filename)

    try:
        raw = call_ollama(args.model, prompt)
        dockerfile = clean_to_dockerfile(raw)
    except Exception as e:
        print(f"Error calling Ollama on {OLLAMA_URL}: {e}", file=sys.stderr)
        sys.exit(1)

    if not re.search(r"(?mi)^FROM\s+\S+", dockerfile):
        print("Error: Ollama output did not contain a valid Dockerfile.", file=sys.stderr)
        sys.exit(2)

    # Write Dockerfile into the specified existing folder
    out_path.write_text(dockerfile + ("" if dockerfile.endswith("\n") else "\n"), encoding="utf-8")
    print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()

