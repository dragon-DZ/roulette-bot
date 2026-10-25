import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# قاموس بسيط لتخزين رصيد اللاعبين الوهمي
balances = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command(name="balance", help="للتحقق من رصيدك الوهمي")
async def balance(ctx):
    user_id = ctx.author.id
    if user_id not in balances:
        balances[user_id] = 1000  # رصيد ابتدائي مجاني 1000 عملة
    
    embed = discord.Embed(
        title="💰 رصيدك الحالي",
        description=f"لديك **{balances[user_id]}** عملة في حسابك.",
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed)

@bot.command(name="roulette", help="لعبة الروليت: !roulette <المبلغ> <red/black/green>")
async def roulette(ctx, amount: int, color: str):
    user_id = ctx.author.id
    
    if user_id not in balances:
        balances[user_id] = 1000

    if amount <= 0:
        await ctx.send("❌ يرجى إدخال مبلغ صحيح للمراهنة!")
        return

    if balances[user_id] < amount:
        await ctx.send("❌ ليس لديك رصيد كافٍ لإتمام هذه المراهنة! استخدم أمر `!balance` للتحقق.")
        return

    color = color.lower()
    if color not in ["red", "black", "green"]:
        await ctx.send("❌ اللون غير صحيح! اختر إما `red` أو `black` أو `green`.")
        return

    # سحب المبلغ مؤقتاً
    balances[user_id] -= amount

    # تحديد نتيجة الروليت (نسبة الحظ)
    roll = random.choices(["red", "black", "green"], weights=[48, 48, 4])[0]

    embed = discord.Embed(
        title="🎰 نتيجة طاولة الروليت",
        color=discord.Color.red() if roll == "red" else (discord.Color.dark_theme() if roll == "black" else discord.Color.green())
    )

    if color == roll:
        if roll == "green":
            win_amount = amount * 14  # فوز كبير للأخضر
        else:
            win_amount = amount * 2   # فوز عادي للأحمر أو الأسود
            
        balances[user_id] += win_amount
        embed.description = f"🎉 مبروك! استقرت الكرة على اللون **{roll.upper()}**.\n لقد ربحت **{win_amount}** عملة!"
        embed.color = discord.Color.green()
    else:
        embed.description = f"😢 حظ أوفر المرة القادمة! استقرت الكرة على اللون **{roll.upper()}**.\n لقد خسرت مراهنتك."
        embed.color = discord.Color.red()

    embed.set_footer(text=f"رصيدك الجديد: {balances[user_id]} عملة")
    await ctx.send(embed=embed)

# تشغيل البوت بالتوكن الخاص بك
bot.run("MTU2Mzk3MzA5OTgxOTUwNzgxMw.G1nYm8.gxlmGPunCcHZUI-Rr4_-RNB7X-WbuSVMel1GFU")
