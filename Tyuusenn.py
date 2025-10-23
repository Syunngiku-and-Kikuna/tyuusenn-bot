import discord
from discord.ext import commands
import csv
import asyncio

client = commands.Bot(intents=discord.Intents.all(), command_prefix="cm!")
txt = discord.Embed


# ステータス変更
async def change_status(statuses: dict, interval: int):
    while True:
        key = list(statuses.keys())[0]
        value = statuses.pop(key)
        statuses[key] = value

        if value == "playing":  # ~をプレイ中
            status = discord.Activity(type=discord.ActivityType.playing, name=key)
        elif value == "streaming":  # ~を配信中
            status = discord.Activity(type=discord.ActivityType.streaming, name=key)
        elif value == "listening":  # ~を再生中
            status = discord.Activity(type=discord.ActivityType.listening, name=key)
        elif value == "watching":  # ~を視聴中
            status = discord.Activity(type=discord.ActivityType.watching, name=key)
        elif value == "competing":  # ~に参戦中
            status = discord.Activity(type=discord.ActivityType.competing, name=key)
        else:  # その他
            status = discord.Activity(type=discord.ActivityType.custom, name=key)

        await client.change_presence(activity=status)

        await asyncio.sleep(interval)  # インターバル(秒)


# ステータス定義 ({key}を{value}中)
statuses = {
    "緑黄色クラフト": "playing",
    "Discord.pyを勉強中": "playing",
    "Javaを勉強中": "playing",
    "れぞるの動画": "watching",
    "春菊の動画": "watching",
    "れぞるの配信": "watching",
    "春菊の配信": "watching",
    "春菊の17Live配信": "watching"
}


@client.event
async def on_ready():
    print("ログインしました")
    await client.load_extension("jishaku")
    await client.tree.sync()
    await change_status(statuses, 60)


class tyuusennButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="抽選参加", style=discord.ButtonStyle.green)
    async def pressedT(self, interaction: discord.Interaction, button: discord.ui.Button):
        with open('oubosya.csv', newline='', encoding='utf-8') as f:
            data = csv.reader(f)
            user_exist = False
            for row in data:
                if str(interaction.user) in row[0]:
                    user_exist = True
        if user_exist:
            await interaction.response.send_message("すでに参加済です", ephemeral=True)
        else:
            with open('oubosya.csv', mode='a', newline='', encoding='utf-8') as fw:
                writer = csv.writer(fw)
                writer.writerow([str(interaction.user), interaction.user.id])
            await interaction.response.send_message("参加しました", ephemeral=True)


@client.tree.command(name="tyuusenn", description="抽選開始用コマンド")
async def tyuusenn(interaction: discord.Interaction):
    role = interaction.guild.get_role(1215981050292080640)
    if role in interaction.user.roles:
        tyuusen_embed = discord.Embed(
            title="抽選参加ボタン",
            description="抽選に参加する方はボタンを押して参加してください",
            color=0x3aff11
        )
        await interaction.channel.send(embed=tyuusen_embed)
        # await interaction.channel.send(view=tyuusennButton())
    else:
        await interaction.response.send_message("権限ないよ", ephemeral=True)


@client.tree.command(name="test", description="抽選開始用コマンド")
async def tyuusenn2(interaction: discord.Interaction):
    tyuusen_embed = discord.Embed(
        title="抽選参加ボタン",
        description="test",
        color=0x3aff11
    )
    await interaction.channel.send(embed=tyuusen_embed)


with open("TSTK.txt") as file:
    client.run(file.read())

# 画面上：表示⇒ターミナル、押すと実行するための画面出てくる
# 実行コマンド1：cd Desktop\Discord-Bot\DiscordBot_tyuusennyoubot
# 実行コマンド2：python .\Tyuusenn.py
# Botを止めるときは「Ctrl+C」を押す
