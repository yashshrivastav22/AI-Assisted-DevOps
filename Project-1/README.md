# 🐳 AI-Assisted Minimal Dockerfile Generator

This project uses **Ollama** (running on port **11435**) to generate **minimal, single-stage Dockerfiles** for different languages (**Python**, **Node.js**, **Shell**, and **Go**).  
Each run generates a Dockerfile **only** in the folder you specify, no other directories are touched.

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
3. Ensure **Python 3.8+** is installed.

---

## 📂 Step-by-Step: Creating Folders, Minimal App Files, Generating Dockerfiles, and Testing

### 0️⃣ Create Project Root and Language Folders
```bash
mkdir -p Project-1/{python,node,shell,go}
```

📂 Initial Folder Structure:
```
Project-1/
├── dockerfile_gen_targeted.py
├── python/
├── node/
├── shell/
├── go/
```
```bash
cd Project-1/
```
---

### 1️⃣ Python

#### Create the minimal Python app file
```bash
cat > python/app.py <<'PY'
print("Hello from Python in Docker!")
PY
```

#### Generate the Dockerfile
```bash
./dockerfile_gen_multi.py --language python --app-dir ./python --version 3.12 --filename python/app.py
```

#### Dockerfile Output (`./python/Dockerfile`)
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY app.py .
CMD ["python3", "app.py"]
```

#### Build and Run
```bash
cd python/
docker build -t demoapp_python:v1 .
docker run --rm demoapp_python:v1
```

#### Output
```
Hello from Python in Docker!
```

---

### 2️⃣ Node.js

#### Create the minimal Node.js app file
```bash
cat > node/app.js <<'JS'
console.log("Hello from Node.js in Docker!");
JS
```

#### Generate the Dockerfile
```bash
./dockerfile_gen_multi.py --language node --app-dir ./node --version 20 --filename node/app.js
```

#### Dockerfile Output (`./node/Dockerfile`)
```dockerfile
FROM node:20-slim
WORKDIR /app
COPY app.js .
CMD ["node", "app.js"]
```

#### Build and Run
```bash
cd node/
docker build -t demoapp_node:v1 .
docker run --rm demoapp_node:v1
```

#### Output
```
Hello from Node.js in Docker!
```

---

### 3️⃣ Shell

#### Create the minimal Shell script
```bash
cat > shell/script.sh <<'SH'
#!/bin/sh
echo "Hello from Shell in Docker!"
SH
```

#### Generate the Dockerfile
```bash
./dockerfile_gen_multi.py --language shell --app-dir ./shell --version 3.18 --filename shell/script.sh
```

#### Dockerfile Output (`./shell/Dockerfile`)
```dockerfile
FROM alpine:3.18
WORKDIR /app
COPY script.sh .
CMD ["sh", "script.sh"]
```

#### Build and Run
```bash
cd shell/
docker build -t demoapp_shell:v1 .
docker run --rm demoapp_shell:v1
```

#### Output
```
Hello from Shell in Docker!
```

---

### 4️⃣ Go

#### Create the minimal Go app
```bash
cat > go/main.go <<'GO'
package main
import "fmt"
func main() { fmt.Println("Hello from Go in Docker!") }
GO
```

#### Generate the Dockerfile
```bash
./dockerfile_gen_multi.py --language go --app-dir ./go --version 1.22 --filename go/main.go
```

#### Dockerfile Output (`./go/Dockerfile`)
```dockerfile
FROM golang:1.22-alpine
WORKDIR /app
COPY main.go .
CMD ["go", "run", "main.go"]
```

#### Build and Run
```bash
cd go/
docker build -t demoapp_go:v1 .
docker run --rm demoapp_go:v1
```

#### Output
```
Hello from Go in Docker!
```

---

## 📂 Final Folder Structure

```
Project-1/
├── dockerfile_gen_multi.py
├── python/
│   ├── app.py
│   └── Dockerfile
├── node/
│   ├── app.js
│   └── Dockerfile
├── shell/
│   ├── script.sh
│   └── Dockerfile
├── go/
│   ├── main.go
│   └── Dockerfile
└── README.md
```

---

## ⚠ Overwriting an Existing Dockerfile
If a Dockerfile already exists in a folder, you must add `--force` to replace it:
```bash
./dockerfile_gen_multi.py --language python --app-dir ./python --force
```

If you don't want to put app version, it will take default version mentioned in the "dockerfile_gen_multi.py" file
```bash
./dockerfile_gen_multi.py --language python --app-dir ./python
```

---
