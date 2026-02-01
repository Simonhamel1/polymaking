import discord
from discord.ext import commands, tasks
import ccxt
import os
import asyncio
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
ALERTS_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ALERTS_ID", 0))
STATUS_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_STATUS_ID", 0))

# Configuration
EXCHANGES = ["binance", "kraken", "bybit"]
TOKENS = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
PRICE_HISTORY = {}

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def get_exchange_instance(exchange_name):
    """Crée une instance d'exchange."""
    try:
        loop = asyncio.get_event_loop()
        exchange_class = getattr(ccxt, exchange_name)
        return await loop.run_in_executor(None, exchange_class)
    except Exception as e:
        print(f"Erreur création {exchange_name}: {e}")
        return None

async def get_price(exchange_name, symbol):
    """Récupère le prix d'un token sur un exchange."""
    try:
        exchange = await get_exchange_instance(exchange_name)
        if not exchange:
            return None
        loop = asyncio.get_event_loop()
        ticker = await loop.run_in_executor(None, exchange.fetch_ticker, symbol)
        return ticker['last']
    except Exception as e:
        print(f"Erreur prix {symbol} sur {exchange_name}: {e}")
        return None

async def get_funding_rate(exchange_name, symbol):
    """Récupère le funding rate (Binance uniquement)."""
    if exchange_name != "binance":
        return None
    try:
        exchange = await get_exchange_instance(exchange_name)
        loop = asyncio.get_event_loop()
        # Format pour futures: BTC/USDT:USDT
        futures_symbol = f"{symbol.split('/')[0]}/USDT:USDT"
        funding = await loop.run_in_executor(None, exchange.fetch_funding_rate, futures_symbol)
        return funding['fundingRate'] * 100
    except Exception as e:
        print(f"Erreur funding rate: {e}")
        return None

def calculate_change(current, previous):
    """Calcule la variation en pourcentage."""
    if previous is None or previous == 0:
        return 0
    return ((current - previous) / previous) * 100

@bot.event
async def on_ready():
    """Bot prêt."""
    print(f"✅ Connecté en tant que {bot.user.name}")
    if STATUS_CHANNEL_ID:
        channel = bot.get_channel(STATUS_CHANNEL_ID)
        if channel:
            await channel.send("🤖 Bot en ligne - Monitoring BTC, ETH, SOL sur multiple exchanges!")
            hourly_alerts.start()
    else:
        print("⚠️ ID du canal non défini")

@tasks.loop(hours=1)
async def hourly_alerts():
    """Alertes toutes les heures."""
    channel = bot.get_channel(ALERTS_CHANNEL_ID)
    if not channel:
        return

    embed = discord.Embed(title="📊 Rapport Horaire", color=discord.Color.blue())

    for token in TOKENS:
        token_name = token.split('/')[0]
        prices = {}

        for exchange in EXCHANGES:
            price = await get_price(exchange, token)
            if price:
                prices[exchange] = price

        if prices:
            avg_price = sum(prices.values()) / len(prices)
            
            # Récupère le prix précédent
            prev_key = f"{token_name}_prev"
            prev_price = PRICE_HISTORY.get(prev_key)
            change = calculate_change(avg_price, prev_price)
            PRICE_HISTORY[prev_key] = avg_price

            emoji = "📈" if change > 0 else "📉"
            field_value = f"Prix moyen: ${avg_price:,.2f}\n{emoji} Variation: {change:+.2f}%\n"
            
            # Funding rate (Binance)
            funding = await get_funding_rate("binance", token)
            if funding is not None:
                field_value += f"💰 Funding: {funding:+.3f}%"

            embed.add_field(name=f"{token_name}", value=field_value, inline=False)

    await channel.send(embed=embed)




# commandes utilisateur
@bot.command(name="price")
async def price_command(ctx, token="BTC"):
    """Commande: !price [BTC|ETH|SOL]"""
    token = token.upper()
    symbol = f"{token}/USDT"

    if symbol not in TOKENS:
        await ctx.send(f"❌ Token non supporté. Disponibles: {', '.join([t.split('/')[0] for t in TOKENS])}")
        return

    embed = discord.Embed(title=f"💹 Prix {token}", color=discord.Color.green())

    for exchange in EXCHANGES:
        price = await get_price(exchange, symbol)
        if price:
            embed.add_field(name=exchange.capitalize(), value=f"${price:,.2f}", inline=True)

    await ctx.send(embed=embed)

@bot.command(name="funding")
async def funding_command(ctx, token="BTC"):
    """Commande: !funding [BTC|ETH|SOL]"""
    token = token.upper()
    symbol = f"{token}/USDT"
    
    funding = await get_funding_rate("binance", symbol)
    if funding is not None:
        await ctx.send(f"💰 Funding rate {token} (Binance): {funding:+.4f}%")
    else:
        await ctx.send("❌ Impossible de récupérer le funding rate")

@bot.command(name="compare")
async def compare_command(ctx):
    """Commande: !compare - Compare tous les tokens"""
    embed = discord.Embed(title="📊 Comparaison tous les tokens", color=discord.Color.gold())

    for token in TOKENS:
        token_name = token.split('/')[0]
        price = await get_price("binance", token)
        if price:
            embed.add_field(name=token_name, value=f"${price:,.2f}", inline=True)

    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
