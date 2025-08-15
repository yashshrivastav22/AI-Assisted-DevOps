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
