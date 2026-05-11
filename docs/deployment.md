# Deployment

## 1. Smithery.ai (Recommended)

The easiest way to make Rental Agent available to any MCP client:

1. Go to [smithery.ai](https://smithery.ai)
2. Import `github.com/Rumblingb/rental-agent-mcp`
3. Smithery handles hosting and discovery

## 2. Docker

```bash
docker run -it --rm -p 8000:8000 python:3.12-slim bash -c "
  pip install mcp httpx
  git clone https://github.com/Rumblingb/rental-agent-mcp.git
  cd rental-agent-mcp
  python server.py
"
```

## 3. Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "rental-agent": {
      "command": "python3",
      "args": ["/path/to/rental-agent-mcp/server.py"]
    }
  }
}
```

## 4. VS Code (Cline/Continue)

```json
{
  "mcpServers": {
    "rental-agent": {
      "command": "python3",
      "args": ["/path/to/rental-agent-mcp/server.py"]
    }
  }
}
```

## 5. Cursor

In Cursor settings → MCP Servers → Add:

```
Name: rental-agent
Type: stdio
Command: python3 /path/to/rental-agent-mcp/server.py
```
