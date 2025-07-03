import asyncio
import uvicorn
from discord_bot import bot
from api import app
from dotenv import load_dotenv
import os

load_dotenv()

async def main():
    asyncio.create_task(bot.start(os.getenv("DISCORD_BOT_TOKEN")))

    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

asyncio.run(main())


