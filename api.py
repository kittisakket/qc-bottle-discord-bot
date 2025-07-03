from fastapi import FastAPI
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, ImageMessage, TextSendMessage, ImageSendMessage
from utils import process_image
import os

app = FastAPI()

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.get("/")
async def root():
    return {"message": "QC Bottle Bot is running"}

@app.get("/send_discord")
async def send_to_discord(message: str):
    from discord_bot import bot
    channel = bot.get_channel(YOUR_CHANNEL_ID)
    await channel.send(message)
    return {"status": "sent"}

# เพิ่ม Webhook ของ LINE ได้ในนี้เหมือนกัน
