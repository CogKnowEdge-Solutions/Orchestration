# Lab 7 Assignment: Local MCP — Connect to a Locally-Run MCP Server

## Exercises

**1. (Concept)** MCP has two variants. Which one does this lab use, what transport does it run over, and what are the two processes that actually talk to each other? *(See Section 7.)*

**2. (Concept)** In one sentence, what does the MCP `ListTools` request do, and which line of the notebook's code triggers it? *(See Section 10, Step 5.)*

**3. (Concept)** A tool crosses the protocol as a *name*, a *description*, and a *schema*. In `mcp_notes_server.py`, where does each of the three come from? *(See Section 10, Step 4.)*

**4. (Applied)** Step 7 calls `add_note` directly with `.ainvoke()` and it works — no model, no agent, no API key anywhere in the call. What does that prove about MCP tools? And in Step 5, why is `command` set to `sys.executable`? *(See Section 10, Steps 5 and 7.)*

**5. (Code)** Write the connection-dict entry that would attach a server named `"reminders"` running `reminders_server.py` with the current Python interpreter over stdio. *(See Section 10, Step 5.)*

**6. (Applied)** In Step 13, two servers are connected and both expose a tool named `add_note`. Why don't the tools collide, and how would the agent refer to the `work` server's `add_note`? *(See Section 10, Step 13.)*

**7. (Concept)** The lab says the agent's toolset is *discovered, not compiled in*. What single change to `mcp_notes_server.py` (from Section 11) gives the notebook's agent a brand-new capability with zero changes to the agent code, and which MCP message carries the new tool to the client? *(See Section 11 and Section 7.)*

**8. (Applied)** Step 10's question ("In one sentence, what is MCP?") produced an `ai:` message with no `tool:` lines. Using the agent loop from Lab 2, explain why the loop didn't call a tool. *(See Section 10, Step 10.)*

## Answer Key

**1.** The **local** variant, over **stdio** (a pipe of JSON-RPC messages between two processes on the same machine). The two processes are the **client** (your notebook / `MultiServerMCPClient`) and the **server** (`mcp_notes_server.py`, spawned as a subprocess).

**2.** It asks the server "what tools do you expose?" and the answer — each tool's name, description, and schema — comes back over the pipe. The notebook triggers it on the line `tools = await client.get_tools()`.

**3.** From the decorated function in `mcp_notes_server.py`: the **name** is the function name (`add_note`), the **description** is the docstring (the model reads it to decide when to call), and the **schema** is derived from the typed signature (`title: str, content: str`).

**4.** MCP tools are plain functions over a protocol — they run with zero LLM involvement. The model is only the thing that *decides* to call them, never the thing that *executes* them. `sys.executable` is the Python interpreter currently running the notebook; the client uses it to spawn the server subprocess so the server runs with the same interpreter (and installed packages) as the notebook.

**5.**
```python
"reminders": {
    "transport": "stdio",
    "command": sys.executable,
    "args": ["reminders_server.py"],
}
```

**6.** `tool_name_prefix=True` prefixes every tool with its server name, so the client sees `notes_add_note` and `work_add_note` — distinct names, no collision. The agent would call `work_add_note`.

**7.** Add the `search_notes` tool with `@mcp.tool()` in `mcp_notes_server.py` and restart the notebook's connection. On the next `ListTools`, the new descriptor comes back, the adapter converts it into a LangChain tool, and the agent can call it — the agent code never changes. This is dynamic capability discovery.

**8.** The agent loop only calls tools when the model emits a `tool_calls` message. For a general-knowledge question, the model responds with a plain answer and no tool calls, so the loop skips the tool node and returns the answer directly. Tools are something the model *may* use, not something it *must* use.
