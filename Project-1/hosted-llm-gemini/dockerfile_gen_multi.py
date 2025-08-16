#!/usr/bin/env python3
import os, argparse

# ---------- helpers ----------
def strip_code_fence(s: str) -> str:
    if "```" not in s:
        return s.strip()
    lines, copying = [], False
    for line in s.splitlines():
        if line.strip().startswith("```"):
            copying = not copying
            continue
        if copying:
            lines.append(line)
    return "\n".join(lines).strip() or s.strip()

# Minimal fallback templates (NO requirements.txt, just app)
FALLBACKS = {
    "python": """\
FROM python:{version}-slim
WORKDIR /app
COPY . .
CMD ["python", "{entry}"]
""",
    "nodejs": """\
FROM node:{version}-alpine
WORKDIR /app
COPY . .
EXPOSE 3000
CMD ["node", "{entry}"]
""",
    "shell": """\
FROM alpine:{version}
WORKDIR /app
COPY {entry} .
RUN chmod +x /app/{entry}
CMD ["/app/{entry}"]
""",
    "go": """\
FROM golang:{version}-alpine
WORKDIR /app
COPY . .
RUN go build -o app {entry}
CMD ["./app"]
"""
}

def build_prompt(language: str, version: str, entry: str) -> str:
    entry_base = os.path.basename(entry)

    if language == "python":
        specifics = f"""\
- Base: python:{version}-slim
- WORKDIR /app
- COPY . .
- CMD ["python", "{entry_base}"]"""
    elif language == "nodejs":
        specifics = f"""\
- Base: node:{version}-alpine
- WORKDIR /app
- COPY . .
- EXPOSE 3000
- CMD ["node", "{entry_base}"]"""
    elif language == "shell":
        specifics = f"""\
- Base: alpine:{version}
- WORKDIR /app
- COPY {entry_base} .
- Make it executable
- CMD ["/app/{entry_base}"]"""
    elif language == "go":
        specifics = f"""\
- Base: golang:{version}-alpine
- WORKDIR /app
- COPY . .
- RUN go build -o app {entry_base}
- CMD ["./app"]"""
    else:
        raise SystemExit("Unsupported language")

    system_rules = """\
You are a Dockerfile generator. Output ONLY a valid Dockerfile.
Constraints:
- Single-stage, minimal, production-safe.
- Prefer slim/alpine images.
- No dependency files (requirements.txt, package.json, go.mod).
- Just copy app and run it.
- Avoid comments and explanations.
"""
    return f"{system_rules}\nGenerate a Dockerfile for {language}:\n{specifics}\n"

def call_gemini(prompt: str) -> str:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is not set.")

    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("models/gemini-1.5-pro")
    resp = model.generate_content(prompt)
    text = (resp.text or "").strip()
    if not text:
        raise RuntimeError("Empty response from Gemini.")
    return strip_code_fence(text)

def generate_dockerfile(language: str, version: str, entry: str) -> str:
    prompt = build_prompt(language, version, entry)
    try:
        return call_gemini(prompt)
    except Exception:
        tmpl = FALLBACKS[language]
        return tmpl.format(version=version, entry=os.path.basename(entry))

def write_file(dirpath: str, content: str, force: bool) -> str:
    os.makedirs(dirpath, exist_ok=True)
    path = os.path.join(dirpath, "Dockerfile")
    if os.path.exists(path) and not force:
        raise SystemExit(f"ERROR: {path} already exists. Use --force to overwrite.")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    return path

# ---------- CLI ----------
def main():
    p = argparse.ArgumentParser(description="Generate a minimal Dockerfile via Gemini.")
    p.add_argument("--language", required=True, choices=["python", "nodejs", "shell", "go"])
    p.add_argument("--app-dir", required=True, help="Target folder for Dockerfile")
    p.add_argument("--version", required=True, help="Runtime version (e.g., 3.12, 22, 3.20, 1.22)")
    p.add_argument("--filename", required=True, help="Entry file (e.g., app.py, server.js, script.sh, main.go)")
    p.add_argument("--force", action="store_true", help="Overwrite existing Dockerfile")
    args = p.parse_args()

    dockerfile = generate_dockerfile(args.language, args.version, args.filename)
    path = write_file(args.app_dir, dockerfile, args.force)
    print(f"✅ Wrote {path}")

if __name__ == "__main__":
    main()

