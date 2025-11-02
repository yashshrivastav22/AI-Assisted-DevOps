# 🐳 MCP Server for Docker - Claude Desktop & Ask Gordon Integration Guide

Easily connect **Claude Desktop** and **Docker Desktop** to your **remote Docker environments** through the  
**[MCP Server for Docker](https://pypi.org/project/mcp-server-docker/)** adapter.  

This setup lets you manage Docker containers on AWS EC2 or any SSH-reachable host  
directly through natural-language interaction — powered by **Claude Desktop** and **Ask Gordon**, Docker’s built-in AI assistant.

---

## 🧩 1. What is `mcp-server-docker`?

[`mcp-server-docker`](https://pypi.org/project/mcp-server-docker/) is an official **Model Context Protocol (MCP)** adapter that allows **Claude Desktop** and **Docker Desktop’s Ask Gordon** to communicate securely with the Docker Engine API.

It acts as a **middleware bridge** between AI tools and Docker:

```
Claude Desktop / Docker Desktop (Ask Gordon) ⇄ MCP Server for Docker ⇄ Docker Context ⇄ Remote AWS Host
```

Through this bridge, you can query, monitor, and control containers conversationally —  
for example:
> “List all containers.”  
> “Restart the nginx container.”  
> “Show image disk usage.”

---

## ⚙️ 2. Installation

### Step 1 - Install [uv](https://pypi.org/project/uv/)
[`uv`](https://pypi.org/project/uv/) is a lightweight Python package runner used to launch MCP servers.

```bash
pip install uv
```

Verify installation:

```bash
uv --version
```

---

### Step 2 - Install [mcp-server-docker](https://pypi.org/project/mcp-server-docker/)
Install the MCP adapter that connects Claude or Docker Desktop’s Ask Gordon to Docker:

```bash
pip install mcp-server-docker
```

Verify installation:

```bash
mcp-server-docker --help
```

You should see command-line options like `--server`, `--token`, and `--read-only`.

---

## 🔐 3. Configure a Docker Context (SSH + PEM)

To securely manage a remote Docker Engine (e.g., AWS EC2) without exposing ports,
create a **Docker Context** using your PEM key:

```bash
docker context create my-remote-docker-host   --description "Remote Docker host using PEM key"   --docker "host=ssh://<remote_user>@<remote_ip>,key=<path of .pem file>"
```

List contexts to confirm:

```bash
docker context ls
```

Example output:

```
NAME                       DESCRIPTION                          DOCKER ENDPOINT
default                    Current DOCKER_HOST based configuration
my-remote-docker-host *     Remote Docker host using PEM key     ssh://ubuntu@44.211.224.248
```

Optionally activate the context:

```bash
docker context use my-remote-docker-host
```

✅ Contexts store connection details securely — no need to expose Docker API TCP ports or embed keys in environment variables.

---

## 🧠 4. Configure Claude Desktop

Claude Desktop reads its integrations from a configuration file  
(on Windows → `%APPDATA%\Claude\claude_desktop_config.json`).

Add this entry:

```json
{
  "mcpServers": {
    "docker-aws": {
      "command": "uvx",
      "args": ["mcp-server-docker"],
      "env": {
        "DOCKER_HOST": "ssh://remote_user@remote_ip"
      }
    }
  }
}
```

### Explanation
| Key | Description |
|-----|--------------|
| `docker-aws` | Logical name for your Docker MCP integration |
| `command` | Uses `uvx` to run the Python adapter |
| `args` | Invokes the `mcp-server-docker` binary |
| `DOCKER_HOST` | Secure SSH connection to your remote Docker Host |
| `remote_user@remote_ip` | EC2 username and IP address |

> 💡 Ensure your SSH private key is accessible through your system’s SSH agent or configured in `~/.ssh/config`.  
> Restart Claude Desktop after saving the file.

---

## 🚀 5. Test the Connection

1. Launch **Claude Desktop**
2. Run a natural-language test, for example:
   ```
   List Docker containers
   ```
   or
   ```
   Show Docker system info
   ```
3. Claude will use the **MCP Server for Docker** to execute real commands on your remote context.

---

## 🎬 Claude Desktop MCP Integration Demo

The following video shows how **Claude Desktop** uses the MCP Server for Docker  
to connect to a remote Docker context and perform live container operations.

https://github.com/yashshrivastav22/Images/tree/main/AI-Assisted-DevOps/Docker_management_with_MCP/assets/mcp_docker_Claude_Desktop_demo.mp4

<video src="https://github.com/yashshrivastav22/Images/tree/main/AI-Assisted-DevOps/Docker_management_with_MCP/assets/mcp_docker_Claude_Desktop_demo.mp4" controls width="600">
  Your browser does not support the video tag.
</video>

### 🧭 What’s Demonstrated
1. Launching **Claude Desktop**
2. Running `List Docker containers`
3. Executing real-time container queries via `mcp-server-docker`
4. Restarting and inspecting containers from conversation

> 💡 *Claude Desktop communicates directly with the Docker Engine through MCP for real-time DevOps automation.*

---

## 🤖 6. Ask Gordon - AI Assistant in Docker Desktop

**Ask Gordon** is a built-in AI assistant within **Docker Desktop** that uses the same  
**MCP Server for Docker** backend to manage your Docker environments conversationally.

| Task | Example Prompt |
|------|----------------|
| List containers | “Show all running containers.” |
| Monitor usage | “How much memory is nginx-prod using?” |
| Manage lifecycle | “Restart the redis-cache container.” |
| Cleanup | “Remove unused Docker images.” |
| System info | “Which Docker context am I connected to?” |

⚡ Ask Gordon translates natural language into Docker API actions using MCP —  
enabling quick insights and automation directly within Docker Desktop.

---

## 🎥 Ask Gordon (Docker Desktop) Demo

Watch this short demo to see **Ask Gordon** in action inside **Docker Desktop**.  
It showcases how you can interact with containers, monitor resources, and perform operations in real time.

<p align="center">
  <video src="assets/ask-gordon-demo.mp4" width="800" controls poster="assets/ask-gordon-thumbnail.png">
    Your browser does not support the video tag.
  </video>
</p>

### 🧭 What’s Demonstrated
1. Opening **Docker Desktop**
2. Launching **Ask Gordon**
3. Asking “List Docker containers”
4. Viewing live container metrics
5. Restarting containers and performing cleanup

> 💡 *Ask Gordon provides an intuitive chat-driven DevOps experience inside Docker Desktop.*

---

## 🧰 7. Troubleshooting

| Issue | Fix |
|-------|-----|
| **SSH authentication failed** | Check `.pem` path and permissions (`chmod 400` on Linux/macOS). |
| **MCP not detected** | Restart Claude Desktop; confirm JSON syntax. |
| **No containers listed** | Run `docker context use my-remote-docker-host` to ensure correct context. |
| **Permission denied** | Add your SSH user to the `docker` group on EC2. |
| **Timeout / no response** | Verify EC2 security group allows SSH from your IP. |

---

## 📚 8. References

- [Model Context Protocol (GitHub)](https://github.com/modelcontextprotocol)
- [Claude Desktop Documentation](https://docs.anthropic.com/claude)
- [Docker Desktop - Ask Gordon Overview](https://docs.docker.com/desktop/ai-assistant/)
- [uv (PyPI)](https://pypi.org/project/uv/)
- [mcp-server-docker (PyPI)](https://pypi.org/project/mcp-server-docker/)
- [Docker Context CLI Reference](https://docs.docker.com/engine/context/working-with-contexts/)

---

> 🧩 **Author:** Yash  
> 🔗 *Integrating Claude MCP and Ask Gordon for AI-assisted Docker management.*  
> 💬 *“Claude + Gordon” — Unified, intelligent DevOps automation.*
