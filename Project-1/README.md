# 🐳 AI-Assisted Minimal Dockerfile Generator

This project uses **Ollama** (running on port **11435**) to generate **minimal, single-stage Dockerfiles** for different languages (**Python**, **Node.js**, **Shell**, and **Go**).  
Each run generates a Dockerfile **only** in the folder you specify — no other directories are touched.

---

## 🚀 Features
- ✅ Generates **only one** Dockerfile per run
- ✅ Writes into **an existing folder** (will not create a new one)
- ✅ Supports **Python, Node.js, Shell, and Go**
- ✅ Uses **only the file name** in the `COPY` instruction (`COPY app.py .`)
- ✅ Refuses to overwrite unless `--force` is given
- ✅ Runs locally with **Ollama** (offline if the model is downloaded)
- ✅ Works with **Ollama API on port 11435**

---

## 📦 Prerequisites
1. Install **[Ollama](https://ollama.com/download)** and start it on **port 11435**:
   ```bash
   OLLAMA_HOST=127.0.0.1:11435 ollama serve
   ```
2. Pull the required model:
   ```bash
   ollama pull llama3.1
   ```
3. Ensure Python 3.8+ is installed.
4. Folder Structure
├── python/
│   └── app.py
├── node/
│   └── app.js
├── shell/
│   └── script.sh
├── go/
│   └── main.go
├── dockerfile_gen_multi.py
└── README.md
Note: The Dockerfile will be placed in the folder you specify (e.g., ./python/Dockerfile)

🛠 Usage
1️⃣ Python
```bash
python dockerfile_gen_targeted.py \
  --language python \
  --app-dir ./python \
  --version 3.12 \
  --filename python/app.py
```
Example Output (./python/Dockerfile):
FROM python:3.12-slim
WORKDIR /app
COPY app.py .
CMD ["python3", "app.py"]
2️⃣ Node.js
```bash
python dockerfile_gen_targeted.py \
  --language node \
  --app-dir ./node \
  --version 20 \
  --filename node/app.js
```
Example Output (./node/Dockerfile):
FROM node:20-slim
WORKDIR /app
COPY app.js .
CMD ["node", "app.js"]
3️⃣ Shell (Alpine)
```bash
python dockerfile_gen_targeted.py \
  --language shell \
  --app-dir ./shell \
  --version 3.18 \
  --filename shell/script.sh
```
Example Output (./shell/Dockerfile):
FROM alpine:3.18
WORKDIR /app
COPY script.sh .
CMD ["sh", "script.sh"]
4️⃣ Go
```bash
python dockerfile_gen_targeted.py \
  --language go \
  --app-dir ./go \
  --version 1.22 \
  --filename go/main.go
```
Example Output (./go/Dockerfile):
FROM golang:1.22-alpine
WORKDIR /app
COPY main.go .
CMD ["go", "run", "main.go"]

⚠ Overwriting an existing Dockerfile
If a Dockerfile already exists in the target folder, you must pass --force to replace it:
```bash
python dockerfile_gen_targeted.py --language python --app-dir ./python --force
```

