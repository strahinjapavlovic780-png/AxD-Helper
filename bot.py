import discord
from discord.ext import commands
import os

# ------------------ Bot setup ------------------
intents = discord.Intents.default()
intents.message_content = True  # Neophodno za komande i poruke

bot = commands.Bot(command_prefix="$", intents=intents)

# ------------------ Config ------------------
OWNER_ROLE_ID = 1486458080265896097  # Zameni sa tvojim Owner role ID
SHOP_NAME = "AxD Shop"

# ------------------ $panel command ------------------
@bot.command()
async def panel(ctx):
    if OWNER_ROLE_ID not in [role.id for role in ctx.author.roles]:
        await ctx.send("❌ You don't have permission to use this command!")
        return

    embed = discord.Embed(
        title=f"🛒 Welcome to {SHOP_NAME}!",
        description=(
            "**Explore our products and make your purchase easily!**\n\n"
            "🔥 **Featured Products:**\n"
            "• Product 1 – **High quality & affordable**\n"
            "• Product 2 – **Limited stock, grab it fast!**\n"
            "• Product 3 – **Best seller of the month**\n\n"
            "To purchase or ask questions, click the **Open Shop Ticket** button below. Our staff will assist you personally.\n\n"
            "**Thank you for choosing AxD Shop!** 💙"
        ),
        color=discord.Color.black()
    )

    embed.set_thumbnail(url="https://i.imgur.com/yourShopThumbnail.png")
    embed.set_footer(text=f"{SHOP_NAME} | Your trusted shop")

    # Button to open shop ticket
    view = discord.ui.View()
    button = discord.ui.Button(label="🛒 Open Shop Ticket", style=discord.ButtonStyle.black, custom_id="open_shop_ticket")
    view.add_item(button)

    await ctx.send(embed=embed, view=view)

# ------------------ Button interaction ------------------
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data["custom_id"] == "open_shop_ticket":
            guild = interaction.guild
            category = discord.utils.get(guild.categories, name="Shop Tickets")  # Napravi ovu kategoriju
            ticket_channel = await guild.create_text_channel(
                name=f"shop-{interaction.user.name}",
                category=category,
                reason="New shop ticket opened"
            )

            # Permissions za korisnika
            await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True)

            # Embed u kanalu
            embed = discord.Embed(
                title=f"🛒 {SHOP_NAME} - Shop Ticket",
                description=(
                    "Welcome to your **personal shop ticket**.\n"
                    "Our staff will assist you shortly.\n"
                    "Please write which product you want to buy or ask your questions here."
                ),
                color=discord.Color.black()
            )
            await ticket_channel.send(embed=embed)

            # Mention korisnika van embeda
            await ticket_channel.send(f"{interaction.user.mention} your ticket is ready! ✅")

            await interaction.response.send_message("✅ Your shop ticket has been created!", ephemeral=True)

# ------------------ $close command ------------------
@bot.command()
async def close(ctx):
    if OWNER_ROLE_ID not in [role.id for role in ctx.author.roles]:
        await ctx.send("❌ You don't have permission to close this ticket!")
        return

    if ctx.channel.name.startswith("ticket-") or ctx.channel.name.startswith("shop-"):
        await ctx.send("✅ Closing the ticket...")
        await ctx.channel.delete()
    else:
        await ctx.send("❌ This command can only be used inside a ticket channel.")

# ------------------ Run bot ------------------
token = os.getenv("TOKEN")
if not token:
    raise ValueError("TOKEN environment variable not set")

bot.run(token)