import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils import process_image
import os

# โหลด ENV
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# ตั้งค่า Intents
intents = discord.Intents.default()
intents.message_content = True  # ต้องเปิดเพื่อให้บอทอ่านข้อความได้

bot = commands.Bot(command_prefix="!", intents=intents)


# บอทเริ่มทำงาน
@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

# คำสั่ง check
@bot.command()
async def check(ctx):
    await ctx.send("📥 โปรดแนบรูปขวดน้ำเพื่อตรวจสอบ QC")

# จัดการรูปที่แนบมา
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                await attachment.save(attachment.filename)

                output_path, summary = process_image(attachment.filename)
                summary_text = ', '.join([f'{k}: {v}' for k, v in summary.items()])

                await message.channel.send(content=summary_text, file=discord.File(output_path))

    await bot.process_commands(message)

# รันบอท
bot.run(DISCORD_BOT_TOKEN)
