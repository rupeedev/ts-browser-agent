"""Run: uv run python examples/history_demo.py (workspace .env supplies TypeSafe)."""

import asyncio
import os
from pathlib import Path

from dotenv import dotenv_values

from ts_browser_agent import build_browser_agent


async def main() -> None:
    config = dotenv_values(Path(__file__).resolve().parents[2] / ".env")
    key = os.getenv("TYPESAFE_API_KEY") or config.get("TYPESAFE_API_KEY") or config.get("typesafe_api_key")
    if not key:
        raise SystemExit("Set TYPESAFE_API_KEY in the workspace .env.")
    os.environ["TYPESAFE_API_KEY"] = key
    agent = build_browser_agent(headless=False, max_steps=8)
    result = await agent.ainvoke({"messages": [("user",
        "Open the History section of the LangChain article. "
        "Stop when the URL ends in #History.\n\n"
        "Start at https://en.wikipedia.org/wiki/LangChain"
    )]})
    for message in result["messages"]:
        if message.type == "ai":
            print(message.content)
    snapshots = [m.artifact for m in result["messages"] if getattr(m, "artifact", None)]
    if snapshots:
        print("Final URL:", snapshots[-1].url)


if __name__ == "__main__":
    asyncio.run(main())
