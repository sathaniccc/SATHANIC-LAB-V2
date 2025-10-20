import os
import logging
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from gtts import gTTS
from io import BytesIO
from PIL import Image
from pyrogram.types import InputMediaPhoto

# ------------- CONFIG ----------------
BOT_TOKEN = os.getenv("8410736835:AAEb8FxjrSN2AmjpiYSfqjg6rBqGLuAqXzI") or "YOUR_BOT_TOKEN"
API_ID = int(os.getenv("93372553") or 123456)
API_HASH = os.getenv("API_HASH") or "YOUR_API_HASH"
YOUTUBE_API = os.getenv("AIzaSyDydoN5jRFL8w-iZAqq--7e3Y2-DmagjYQ") or "YOUR_YOUTUBE_API"
OMDB_API = os.getenv("OMDB_API") or "YOUR_OMDB_API"
ADMIN_ID = int(os.getenv("ADMIN_ID") or 0)

app = Client("SATHANIC_LAB", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ------------- WELCOME & MENU ----------------
MENU = [
    [InlineKeyboardButton("🎵 Songs", callback_data="song") ,
     InlineKeyboardButton("🎬 Movies", callback_data="movie")],
    [InlineKeyboardButton("📱 Apps", callback_data="app"),
     InlineKeyboardButton("🎮 Mod APKs", callback_data="mod")],
    [InlineKeyboardButton("🗣️ TTS", callback_data="tts"),
     InlineKeyboardButton("🖼️ Photo→Sticker", callback_data="sticker")],
    [InlineKeyboardButton("🤖 Fun Chat", callback_data="fun")]
]

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_photo(
        photo="https://i.ibb.co/4gJvZbZ/satanic-lab.jpg",
        caption=f"😈 Welcome to *SATHANIC LAB*\nHey {message.from_user.first_name}, choose below 👇",
        reply_markup=InlineKeyboardMarkup(MENU)
    )

@app.on_callback_query()
async def cb_handler(client, callback):
    data = callback.data
    if data == "song":
        await callback.message.edit_text("🎧 Send me song name to search YouTube")
    elif data == "movie":
        await callback.message.edit_text("🎬 Send movie name to get OMDb info")
    elif data == "app":
        await callback.message.edit_text("📱 Send app name to get Play Store info")
    elif data == "mod":
        await callback.message.edit_text("🎮 Send APK name to get Mod APK links")
    elif data == "tts":
        await callback.message.edit_text("🗣️ Send text to get TTS audio reply")
    elif data == "sticker":
        await callback.message.edit_text("🖼️ Send photo to convert into Telegram sticker")
    elif data == "fun":
        await callback.message.edit_text("🤖 Send message for fun auto-reply")

# ------------- COMMAND HANDLERS ----------------
@app.on_message(filters.text & filters.reply)
async def reply_handler(client, message):
    reply_to = message.reply_to_message.text.lower()
    text = message.text

    # SONG SEARCH
    if "song" in reply_to:
        query = text
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={query}&key={YOUTUBE_API}"
        r = requests.get(url).json()
        if "items" in r:
            vid = r["items"][0]
            title = vid["snippet"]["title"]
            link = f"https://www.youtube.com/watch?v={vid['id']['videoId']}"
            await message.reply_text(f"🎵 {title}\n{link}")
        else:
            await message.reply_text("😕 No results found")

    # MOVIE INFO
    elif "movie" in reply_to:
        query = text
        url = f"http://www.omdbapi.com/?t={query}&apikey={OMDB_API}"
        r = requests.get(url).json()
        if r.get("Response")=="True":
            await message.reply_photo(
                r.get("Poster"),
                caption=f"🎬 {r['Title']} ({r['Year']})\n⭐ {r['imdbRating']}/10\n📄 {r['Plot']}"
            )
        else:
            await message.reply_text("❌ Movie not found")

    # APP INFO
    elif "app" in reply_to:
        q = text.replace(" ","+")
        await message.reply_text(f"📲 Play Store search:\nhttps://play.google.com/store/search?q={q}&c=apps")

    # MOD APK SEARCH (dummy example links)
    elif "apk" in text.lower() or "mod" in reply_to:
        await message.reply_text(f"🎮 Mod APK Links for {text}:\nhttps://moddroid.com/search?q={text}\nhttps://happymod.com/search.html?q={text}")

    # TTS
    elif "tts" in reply_to:
        tts = gTTS(text)
        bio = BytesIO()
        tts.write_to_fp(bio)
        bio.seek(0)
        await message.reply_voice(bio)

    # PHOTO → STICKER
    elif "sticker" in reply_to and message.photo:
        img = await message.download()
        im = Image.open(img)
        bio = BytesIO()
        im.save(bio,"WEBP")
        bio.seek(0)
        await message.reply_sticker(bio)

    # FUN AUTO REPLY
    elif "fun" in reply_to:
        fun_dict = {"hi":"Hello bro 😎","good morning":"Have a great day 🌞","bye":"See ya ✌️"}
        resp = fun_dict.get(text.lower(), "😂 I didn't get that, try again!")
        await message.reply_text(resp)

# ------------- RUN BOT ----------------
print("🔥 SATHANIC LAB v2.0 Running...")
app.run()
