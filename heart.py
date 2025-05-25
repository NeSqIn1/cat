import asyncio
import logging
import os
import random

from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ENV config
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TARGET_USER_ID = os.getenv("TARGET_USER_ID")
OWNER_ID = os.getenv("OWNER_ID")

if not TOKEN or not TARGET_USER_ID or not OWNER_ID:
    raise ValueError("Set TELEGRAM_BOT_TOKEN, TARGET_USER_ID, OWNER_ID in environment")

TARGET_USER_ID = int(TARGET_USER_ID)
OWNER_ID = int(OWNER_ID)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Love messages
MESSAGES = [
    "Ты согрреваешь моё сердце, котик!",
    "Каждый раз, когда я вижу тебя, я таю, котик!",
    "Твоё присутствие — мой самый дорогой подарок, котик!",
    "С тобой мир становится ярче, котик!",
    "Ты — лучик солнца в моём дне, котик!",
    "Я не устаю любоваться тобой, котенок!",
    "Твоя улыбка — моя слабость, котик!",
    "Моё сердце бьётся чаще рядом с тобой, котик!",
    "Ты делаешь мою жизнь волшебной, котик!",
    "Я люблю каждое мгновение с тобой, котик!",
    "С тобой я забываю обо всём на свете, котик!",
    "Ты красива, котеночек, как рассвет!",
    "Каждое твоё слово — музыка для моей души, котик!",
    "С тобой я чувствую себя дома, котик!",
    "Ты — мой самый заветный сон, котик!",
    "Каждый день с тобой — праздник, котик!",
    "Я дорожу каждой секундой рядом с тобой, котик!",
    "Ты — моя главная мысль утром и вечером, котик!",
    "В твоих объятиях я нахожу покой!!!!!",
    "Ты — моё вдохновение, котик!",
    "Мои чувства к тебе безграничны, котик!",
    "Я счастлив, что ты у меня есть, котик!",
    "С каждым днём люблю тебя сильнее, котик!",
    "Ты наполняешь мою жизнь смыслом, котик!",
    "Я хочу делать тебя счастливой, котик!!!!!",
    "Ты — моя нежность, котик!!!!!!!!!",
    "В твоих глазах я вижу своё будущее, котик!",
    "Люблю твой смех, котик!",
    "Ты — моя радость, котик!",
    "Моё сердце принадлежит только тебе, котик!",
    "Ты — самая красивая часть моего каждого дня, котик!",
    "С тобой я летаю от счастья, котик!",
    "Ты делаешь меня лучше, котик!",
    "Я скучаю по тебе каждую секунду, котик!",
    "Ты — моя сказка, котик!",
    "Моё счастье — это ты, котик!",
    "Ты — моя нежная мелодия, котик!",
    "Я храню тепло твоих прикосновений, котик!",
    "Ты — свет в моём сердце, котик!",
    "Моё сердце поёт для тебя, котик!",
    "Ты — моё всё, котик!",
    "Я люблю твой голос, котик!",
    "С тобой я забываю обо всех проблемах, котик!",
    "Ты делаешь каждый день особенным, котик!",
    "Я хочу быть рядом вечно, котик!",
    "Ты — моя нежная грёза, котик!",
    "Моё сердце бьётся только для тебя, котик!",
    "Ты — моя гармония, котик!",
    "Я наполняюсь счастьем рядом с тобой, котик!",
    "Ты вдохновляешь меня мечтать, котик!",
    "Моё сердце тает от твоих поцелуев, котик!",
    "Ты — моя звезда, котик!",
    "С тобой любое место становится домом, котик!",
    "Я хочу смотреть в твои глаза вечно, котик!",
    "Ты — моё солнце в пасмурный день, котик!",
    "Я люблю, когда ты смеёшься, котик!",
    "Ты — моя самая красивая мысль, котик!",
    "Моё сердце поёт, когда ты рядом, котик!",
    "Ты делаешь мою жизнь полной, котик!",
    "Я в восторге от твоей доброты, котик!",
    "Ты — моя радость и покой, котик!",
    "Я хочу дарить тебе счастье, котик!",
    "Ты делаешь моё сердце мягким, котик!",
    "Моя любовь к тебе — бесконечность, котик!",
    "Ты — мой самый дорогой человек, котик!",
    "С тобой я чувствую себя особенным, котик! (ну прям оченьььь)",
    "Я люблю твои глазки, котик!",
    "Ты — моя нежная весна, котик!",
    "Моё сердце переполнено тобой, котик!",
    "Ты — моя радужная мечта, котик!",
    "Я счастлив, когда ты счастлива, котик!",
    "Ты — мой ангел, котик!",
    "Моя душа светится от твоей любви, котик!",
    "Ты — моя энергия, котик!",
    "Я влюблён в каждую черточку твоего лица, котик!(ну правда)",
    "Ты — моё безмятежное счастье, котик!",
    "Я люблю тебя до луны и обратно, котик!",
    "Ты — моя тихая гавань, котик!",
    "Моё сердце принадлежит только тебе, котик!",
    "Ты — моя бесконечная сказка, котик!",
    "Я дышу тобой, котик!",
    "Ты — моя радуга после дождя, котик!",
    "Моё сердце радуется, когда ты рядом, котик!",
    "Ты — моя вечная песня, котик!",
    "Я люблю твои теплые ладони, котик!",
    "Ты — моя самая нежная мысль, котик!",
    "Моё счастье начинается с тебя, котик!",
    "Ты — моя главная ценность, котик!",
    "Я в восторге от твоей улыбки, котик!",
    "Ты — моё вдохновение и покой, котик!",
    "Моё сердце поет от твоей любви, котик!",
    "Ты самый шикарный котик в галактике!",
    "мрр~"
]


# Background task
async def love_task(bot: Bot, chat_id: int) -> None:
    await asyncio.sleep(5)  # delay before first message
    while True:
        try:
            message = random.choice(MESSAGES)
            await bot.send_message(chat_id=chat_id, text=message)
            logger.info(f"Sent: {message}")
        except Exception as e:
            logger.error(f"Error sending love: {e}")
        await asyncio.sleep(1800)  # 1 hour


# /start command
async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("йооо, каждые полчаса ты будешь чувствовать мою любовь <3")


# Forwarding messages
async def forward_to_owner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await context.bot.forward_message(
            chat_id=OWNER_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
    except Exception as e:
        logger.error(f"Forward error: {e}")


# Post-start hook
async def on_startup(application: Application) -> None:
    asyncio.create_task(love_task(application.bot, TARGET_USER_ID))


# Main launcher
async def main() -> None:
    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .post_init(on_startup)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_owner))

    await application.run_polling()


import asyncio

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()

    from telegram.ext import ApplicationBuilder
    # Импортируй свою функцию `main()` если она отдельно

    asyncio.get_event_loop().run_until_complete(main())
