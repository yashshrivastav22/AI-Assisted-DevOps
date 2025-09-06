# 📦 Hosted LLM Gemini Dockerfile Generator

This project uses **Google Gemini (hosted LLM)** to generate **minimal, single-stage Dockerfiles** for simple applications written in:

- Python  
- Node.js  
- Shell  
- Go  

The generator script (`dockerfile_gen_multi.py`) takes arguments for language, app directory, version, and entry file. It produces a ready-to-use `Dockerfile` inside the target app folder.

---
## 🚀 Project Structure
```
Dockerfile_generator_with_AI/
└── hosted-llm-gemini/
    ├── dockerfile_gen_multi.py      
    ├── python
    ├── node/
    ├── shell/
    ├── go/
    └── .venv/
```
---

## ⚙️ Setup
1. **Create a virtual environment & install dependencies**

```bash
cd hosted-llm-gemini
python -m venv .venv
source .venv/bin/activate
pip install google-generativeai
```
2. Set your Gemini API Key

Get an API key from 👉 https://aistudio.google.com
Export it:
```bash
export GOOGLE_API_KEY="PASTE_YOUR_KEY"
```
---

## 🛠️ Usage
Run the script with your desired language, version, and entry file:
```bash
./dockerfile_gen_multi.py --language <lang> --app-dir <folder> --version <runtime_version> --filename <entry_file>
```
If you don't want to put app version, it will take default version mentioned in the "dockerfile_gen_multi.py" file
```bash
./dockerfile_gen_multi.py --language python --app-dir ./python
```
---

## 📂 Step-by-Step: Creating Folders, Minimal App Files, Generating Dockerfiles, and Testing

### 0️⃣ Create Project Root and Language Folders
```bash
mkdir -p Dockerfile_generator_with_AI/{python,node,shell,go}
```

📂 Initial Folder Structure:
```
Dockerfile_generator_with_AI/
└── hosted-llm-gemini/
    ├── dockerfile_gen_multi.py      
    ├── python
    ├── node/
    ├── shell/
    ├── go/
    └── .venv/
```
```bash
cd Dockerfile_generator_with_AI/hosted-llm-gemini
```
---

### 1️⃣ Python

#### Create the minimal Python app file
```bash
cat > python/app.py <<'PY'
print("Hello Gemini from Python in Docker!")
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
COPY . .
CMD ["python", "app.py"]
```

#### Build and Run
```bash
cd python/
docker build -t demoapp_gemini_python:v1 .
docker run --rm demoapp_gemini_python:v1
```

#### Output
```
Hello Gemini from Python in Docker!
```

---

### 2️⃣ Node.js

#### Create the minimal Node.js app file
```bash
cat > node/app.js <<'JS'
console.log("Hello Gemini from Node.js in Docker!");
JS
```

#### Generate the Dockerfile
```bash
./dockerfile_gen_multi.py --language nodejs --app-dir ./node --version 22 --filename node/app.js
```

#### Dockerfile Output (`./node/Dockerfile`)
```dockerfile
FROM node:22-alpine
WORKDIR /app
COPY . .
EXPOSE 3000
CMD ["node", "app.js"]
```

#### Build and Run
```bash
cd node/
docker build -t demoapp_gemini_node:v1 .
docker run --rm demoapp_gemini_node:v1
```

#### Output
```
Hello Gemini from Node.js in Docker!
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
./dockerfile_gen_multi.py --language shell --app-dir ./shell --version 3.20 --filename shell/script.sh
```

#### Dockerfile Output (`./shell/Dockerfile`)
```dockerfile
FROM alpine:3.20
WORKDIR /app
COPY script.sh .
RUN chmod +x /app/script.sh
CMD ["/app/script.sh"]
```

#### Build and Run
```bash
cd shell/
docker build -t demoapp_gemini_shell:v1 .
docker run --rm demoapp_gemini-shell:v1
```

#### Output
```
Hello Gemini from Shell in Docker!
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
COPY . .
RUN go build -o app main.go
CMD ["./app"]
```

#### Build and Run
```bash
cd go/
docker build -t demoapp_gemini_go:v1 .
docker run --rm demoapp_gemini_go:v1
```

#### Output
```
Hello Gemini from Go in Docker!
```

---

## 📂 Final Folder Structure

```
Dockerfile_generator_with_AI/
└── hosted-llm-gemini/
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
    └── go/
        ├── main.go
        └── Dockerfile
```

## 🐋 Generated docker images by Gemini:
![Alt text](../images/docker_images_gemini_llm.PNG)

---

## ⚠ Overwriting an Existing Dockerfile
If a Dockerfile already exists in a folder, you must add `--force` to replace it:
```bash
./dockerfile_gen_multi.py --language python --app-dir ./python --force
```

---




