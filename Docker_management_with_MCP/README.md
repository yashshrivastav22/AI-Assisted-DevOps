# 🐳 MCP Server for Docker – Claude Desktop Integration Guide

Easily connect **Claude Desktop** to your **remote Docker environments** through the  
**[MCP Server for Docker](https://pypi.org/project/mcp-server-docker/)** adapter.  
This setup lets you manage Docker containers on AWS EC2 or any SSH-reachable host  
directly through natural-language interaction - powered by **Ask Gordon**, an AI DevOps assistant.

---

## 🧩 1. What is `mcp-server-docker`?

[`mcp-server-docker`](https://pypi.org/project/mcp-server-docker/) is an official **Model Context Protocol (MCP)** adapter that allows Claude (via Claude Desktop) to communicate with the Docker Engine API.

It acts as a **secure middleware layer** between Claude and Docker:
```
Claude Desktop  ⇄  MCP Server for Docker  ⇄  Docker Context  ⇄  Remote AWS Host
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
Install the MCP adapter that connects Claude to Docker:

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
create a **Docker Context** that uses your PEM key:

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

## 🤖 6. Ask Gordon - Your AI Docker Assistant

**Ask Gordon** is an AI DevOps persona that runs through Claude Desktop using the MCP Docker adapter.  
It allows conversational container management — no CLI required.

| Task | Example Prompt |
|------|----------------|
| List containers | “Ask Gordon: show all running containers.” |
| Monitor usage | “Ask Gordon: how much memory is nginx-prod using?” |
| Manage lifecycle | “Ask Gordon: restart the redis-cache container.” |
| Cleanup | “Ask Gordon: remove unused Docker images.” |
| System info | “Ask Gordon: show Docker version and context name.” |

⚡ Ask Gordon converts natural language into authenticated Docker API actions via the MCP bridge.

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

## 📚 9. References

- [Model Context Protocol (GitHub)](https://github.com/modelcontextprotocol)
- [Claude Desktop Documentation](https://docs.anthropic.com/claude)
- [uv (PyPI)](https://pypi.org/project/uv/)
- [mcp-server-docker (PyPI)](https://pypi.org/project/mcp-server-docker/)
- [Docker Context CLI Reference](https://docs.docker.com/engine/context/working-with-contexts/)

---

> 🧩 **Author:** Yash  
> 🔗 *Integrating Claude MCP with Docker Contexts for secure AI-assisted DevOps.*  
> 💬 *“Ask Gordon” — Manage your containers the smart way.*
