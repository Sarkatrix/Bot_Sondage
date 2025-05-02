import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    try:
        synced = await tree.sync()
        print(f"🌐 {len(synced)} commande(s) slash synchronisée(s).")
    except Exception as e:
        print(f"❌ Erreur de synchronisation : {e}")

@tree.command(name="sondage", description="Crée un sondage avec des réactions")
@app_commands.describe(
    question="La question du sondage",
    max_votes="Nombre maximum de votes par personne",
    reponses="Réponses séparées par des virgules (ex: Oui,Non,Peut-être)"
)
async def sondage(interaction: discord.Interaction, question: str, max_votes: int, reponses: str):
    options = [r.strip() for r in reponses.split(",") if r.strip()]
    if len(options) < 2 or len(options) > 10:
        await interaction.response.send_message("⚠️ Il faut entre 2 et 10 réponses maximum.", ephemeral=True)
        return

    if max_votes < 1 or max_votes > len(options):
        await interaction.response.send_message("⚠️ Le nombre maximum de votes doit être entre 1 et le nombre de réponses.", ephemeral=True)
        return

    emojis = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟']
    description = f"**{question}**\n\n"
    for i, opt in enumerate(options):
        description += f"{emojis[i]} {opt}\n"

    embed = discord.Embed(title="🗳️ Sondage", description=description, color=0x00ff99)
    embed.set_footer(text=f"Max {max_votes} vote(s) par personne.")

    await interaction.response.send_message(embed=embed)
    message = await interaction.original_response()

    for i in range(len(options)):
        await message.add_reaction(emojis[i])

# Démarrage du bot
if __name__ == "__main__":
    bot.run(os.environ["DISCORD_TOKEN"])
