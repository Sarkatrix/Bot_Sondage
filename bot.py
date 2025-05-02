import discord
from discord.ext import commands
from discord import app_commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree  # ✅ correction ici

@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Connecté en tant que {bot.user} - Slash commands synchronisées.")

@tree.command(name="sondage", description="Créer un sondage avec des réactions.")
@app_commands.describe(
    question="La question du sondage",
    choix="Les choix séparés par des virgules (ex: Oui,Non,Peut-être)",
    max_votes="Nombre maximum de réponses qu’un membre peut choisir"
)
async def sondage(interaction: discord.Interaction, question: str, choix: str, max_votes: int):
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    options = [opt.strip() for opt in choix.split(",")]

    if not (2 <= len(options) <= len(emojis)):
        await interaction.response.send_message(
            "❌ Vous devez entrer entre 2 et 10 options séparées par des virgules.",
            ephemeral=True
        )
        return

    if max_votes < 1 or max_votes > len(options):
        await interaction.response.send_message(
            f"❌ Le nombre de votes doit être entre 1 et {len(options)}.",
            ephemeral=True
        )
        return

    description = ""
    for i, option in enumerate(options):
        description += f"{emojis[i]} {option}\n"

    embed = discord.Embed(
        title=f"📊 {question}",
        description=description,
        color=discord.Color.blurple()
    )
    embed.set_footer(text=f"Vous pouvez voter pour {max_votes} option(s).")

    await interaction.response.send_message(embed=embed)
    message = await interaction.original_response()

    for i in range(len(options)):
        await message.add_reaction(emojis[i])

bot.run(os.environ["DISCORD_TOKEN"])
