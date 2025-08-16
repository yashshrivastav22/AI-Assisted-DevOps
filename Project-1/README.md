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

## Step-by-Step: Creating Folders, minimal app files & create the Dockerfile for every application with building the respective image and testing.
```bash
mkdir -p Project-1/{python,node,shell,go}
```
### 1️ Python
#### Create the minimal Python app file
```bash
cat > python/app.py <<'PY'
print("Hello from Python in Docker!")
PY
```
#### Generate the Dockerfile for python application
```bash
./dockerfile_gen_targeted.py --language python --app-dir ./python --version 3.12 --filename python/app.py
```
#### Output(./python/Dockerfile):
```
FROM python:3.12-slim
WORKDIR /app
COPY app.py .
CMD ["python3", "app.py"]
```
#### Build and run the python based application for testing
```bash
cd python/
docker build -t demoapp_python:v1 .
docker run --rm demoapp_python:v1
```
#### Output
```bash
Hello from Python in Docker!
```
### 2️⃣ Node
#### Create the minimal Node app file
```bash
cat > node/app.js <<'JS'
console.log("Hello from Node.js in Docker!");
JS
```
#### Generate the Dockerfile for node application
```bash
./dockerfile_gen_targeted.py --language node --app-dir ./node --version 20 --filename node/app.py
```
#### Output(./node/Dockerfile):
```
FROM node:20-slim
WORKDIR /app
COPY app.js .
CMD ["node", "app.js"]
```
#### Build and run the node based application for testing
```bash
cd node/
docker build -t demoapp_node:v1 .
docker run --rm demoapp_node:v1
```
#### Output
```bash
Hello from Node.js in Docker!
```
### 3️⃣ Shell
#### Create the minimal Shell app file
```bash
cat > shell/script.sh <<'SH'
#!/bin/sh
echo "Hello from Shell in Docker!"
SH
```
#### Generate the Dockerfile for shell application
```bash
./dockerfile_gen_multi.py --language node --app-dir ./shell --version 3.18 --filename shell/app.py
```
#### Output(./shell/Dockerfile):
```
FROM alpine:3.18
WORKDIR /app
COPY script.sh .
CMD ["sh", "script.sh"]
```
#### Build and run the shell based application for testing
```bash
./dockerfile_gen_multi.py --language shell --app-dir ./shell --version 3.18 --filename shell/script.sh
```
#### Output (./shell/Dockerfile):
```
FROM alpine:3.18
WORKDIR /app
COPY script.sh .
CMD ["sh", "script.sh"]
```
#### Build and run the node based application for testing
```bash
cd shell/
docker build -t demoapp_shell:v1 .
docker run --rm demoapp_shell:v1
```
#### Output
```bash
Hello from Shell in Docker!
```
4️⃣ Go
#### Create the minimal Go app file
```bash
cat > go/main.go <<'GO'
package main
import "fmt"
func main() { fmt.Println("Hello from Go in Docker!") }
GO
```
#### Generate the Dockerfile for shell application
```bash
./dockerfile_gen_multi.py --language go --app-dir ./go --version 1.22 --filename go/app.py
```
#### Output(./go/Dockerfile):
```
FROM golang:1.22-alpine
WORKDIR /app
COPY main.go .
CMD ["go", "run", "main.go"]
```
#### Build and run the node based application for testing
```bash
cd go/
docker build -t demoapp_go:v1 .
docker run --rm demoapp_go:v1
```
#### Output
```csharp
Hello from Go in Docker!
📂 Folder Structure
```

```
Project-1/
├── dockerfile_gen_targeted.py
├── python/
│   └── app.py
├── node/
│   └── app.js
├── shell/
│   └── script.sh
├── go/
│   └── main.go
└── README.md
```


