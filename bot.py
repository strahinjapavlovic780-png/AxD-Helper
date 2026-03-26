import discord
from discord.ext import commands
import os  # Obavezno za os.getenv

# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Obavezno za komande i poruke

# Create bot with prefix and intents
bot = commands.Bot(command_prefix="$", intents=intents)

# Owner role ID
OWNER_ROLE_ID = 1486458080265896097
SHOP_NAME = "AxD Shop"

# ------------------ $panel command ------------------
@bot.command()
async def panel(ctx):
    # Check if user has Owner role
    if OWNER_ROLE_ID not in [role.id for role in ctx.author.roles]:
        await ctx.send("❌ You don't have permission to use this command!")
        return

    # Create the shop embed
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
        color=discord.Color.green()
    )

    embed.set_thumbnail(url="https://i.imgur.com/yourShopThumbnail.png")  # optional thumbnail
    embed.set_footer(text=f"{SHOP_NAME} | Your trusted shop")

    # Create a button for opening a shop ticket
    view = discord.ui.View()
    button = discord.ui.Button(label="🛒 Open Shop Ticket", style=discord.ButtonStyle.green, custom_id="open_shop_ticket")
    view.add_item(button)

    await ctx.send(embed=embed, view=view)

# ------------------ Button interaction ------------------
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data["custom_id"] == "open_shop_ticket":
            guild = interaction.guild
            category = discord.utils.get(guild.categories, name="Shop Tickets")  # Make sure this category exists
            ticket_channel = await guild.create_text_channel(
                name=f"shop-{interaction.user.name}",
                category=category,
                reason="New shop ticket opened"
            )
            await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True)
            await ticket_channel.send(
                f"Hello {interaction.user.mention}! 🛒\n"
                "Welcome to your **personal shop ticket**. Our staff will assist you shortly.\n"
                "Please **state which product** you want to buy or ask your questions here."
            )
            await interaction.response.send_message("✅ Your shop ticket has been created!", ephemeral=True)

# ------------------ $close command ------------------
@bot.command()
async def close(ctx):
    # Check if user has the Owner role
    if OWNER_ROLE_ID not in [role.id for role in ctx.author.roles]:
        await ctx.send("❌ You don't have permission to close this ticket!")
        return

    # Check if the channel is a ticket channel
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