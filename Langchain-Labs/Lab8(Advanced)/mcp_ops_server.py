"""A self-hosted MCP server for Lab 8: "Market Ops" internal service.

This is the *hosted* half of the lab. Unlike Lab 7's stdio server, this server
exposes its tools over Streamable HTTP, so a client on any machine can reach it
by URL — the same shape as a third-party hosted MCP server (e.g. Coinfuty on
mcp.so). The data is synthetic and deterministic on purpose: the lab is about
the MCP + context mechanics, not about real market data.

Context engineering is about what the *server* chooses to hand back, too. The
three tools below differ in how much context they produce:
  - digest_snapshot   : compact, fixed size.
  - digest_logs       : the full firehose (as big as you ask for).
  - digest_highlights : a server-side *digest* — the same events, compressed.

Run it:  python mcp_ops_server.py [port]
"""

import logging
import random
import sys
import warnings

from mcp.server.fastmcp import FastMCP

logging.getLogger("mcp").setLevel(logging.WARNING)
warnings.filterwarnings("ignore", module="pydantic_settings")

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8788

mcp = FastMCP("market-ops")
mcp.settings.host = "127.0.0.1"
mcp.settings.port = PORT


def _log_lines(coin: str, n: int) -> str:
    rng = random.Random(7)  # deterministic "logs" so every run matches Section 5
    kinds = ["INFO request ok", "WARN slow response", "ERROR upstream timeout"]
    return "\n".join(
        f"{rng.randint(0, 23):02d}:{rng.randint(0, 59):02d}:{rng.randint(0, 59):02d} "
        f"{coin.upper()} {rng.choice(kinds)} latency={rng.randint(20, 950)}ms"
        for _ in range(n)
    )


def _build_logs(coins: str, lines: int) -> str:
    return "\n".join(_log_lines(c.strip(), max(1, lines // max(1, len(coins.split(",")))))
                     for c in coins.split(","))


@mcp.tool()
def digest_snapshot(coins: str = "BTC,ETH,SOL") -> str:
    """Return a compact one-line digest per coin: price, 24h change, funding
    rate and open interest. All fields are synthetic sample data generated
    deterministically on every call."""
    rows = {
        "BTC": ("68241.5", "-0.5%", "0.0101%", "$32.4B"),
        "ETH": ("3521.8", "+1.2%", "0.0092%", "$18.1B"),
        "SOL": ("142.7", "-2.1%", "0.0124%", "$6.8B"),
    }
    return "\n".join(
        f"{c}: price={rows.get(c.upper(), ('?', '?', '?', '?'))[0]} "
        f"24h={rows.get(c.upper(), ('?', '?', '?', '?'))[1]} "
        f"funding={rows.get(c.upper(), ('?', '?', '?', '?'))[2]} "
        f"OI={rows.get(c.upper(), ('?', '?', '?', '?'))[3]}"
        for c in coins.split(",")
    )


@mcp.tool()
def digest_logs(coins: str, lines: int = 300) -> str:
    """Return the raw log stream for the given coins, up to `lines` entries.
    This is the unshaped context: the full firehose, returned verbatim.
    A multi-thousand-token result is common — and paid for on every request."""
    return _build_logs(coins, lines)


@mcp.tool()
def digest_highlights(coins: str) -> str:
    """Return a short server-side digest of recent logs for the given coins:
    one line with error/warn/info counts plus the five most recent events.
    Same underlying events as digest_logs, but shaped server-side so only a
    few hundred characters reach the model."""
    parts = []
    for c in coins.split(","):
        events = _log_lines(c.strip(), 20).split("\n")
        errors = sum(1 for e in events if "ERROR" in e)
        warns = sum(1 for e in events if "WARN" in e)
        parts.append(f"{c.upper()}: {errors} errors, {warns} warns, "
                     f"{20 - errors - warns} infos; last: {events[-1]}")
    return "\n".join(parts)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
