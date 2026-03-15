from discord.ext import commands
from datetime import datetime, timedelta
from discord import ButtonStyle, app_commands
from database import User, session
import discord
from config import config
import random


class Lottery(discord.ui.View):  # 抽選コマンド
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="参加", style=ButtonStyle.green, emoji="✅", custom_id="present-a")
    async def pressedLotteryButton(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.defer(thinking=True, ephemeral=True)
        oubouser = session.query(User).filter_by(userid=interaction.user.id).first()

        if not oubouser:
            userdb = User(userid=interaction.user.id, username=interaction.user.name, displayname=interaction.user.display_name)
            session.add(userdb)
            session.commit()
            await interaction.followup.send("参加が完了しました。当選発表までお待ちください。", ephemeral=True)
            return
        else:
            await interaction.followup.send("すでに参加済みです。当選発表までお待ちください。", ephemeral=True)
            return

    @discord.ui.button(label="参加状況確認", style=ButtonStyle.blurple, custom_id="check-b")
    async def pressedCheckButton(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.defer(thinking=True, ephemeral=True)
        oubouser = session.query(User).filter_by(userid=interaction.user.id).first()
        if not oubouser:
            await interaction.followup.send("まだ参加されていません。参加ボタンを押して参加してください。", ephemeral=True)
            return
        else:
            await interaction.followup.send("参加完了してます。当選発表までお待ちください。", ephemeral=True)

    @discord.ui.button(label="企画終了", style=ButtonStyle.red, custom_id="delevent-c")
    async def pressedDeleventButton(self, interaction: discord.Interaction, button: discord.ui.button):
        if interaction.user.id == config.syunngiku_id:
            await interaction.message.delete()
        else:
            await interaction.response.send_message("権限ないで", ephemeral=True)


class Present(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

# !--------------------------------------------------------------------

    @app_commands.command(name="present", description="【運営】present企画")
    @app_commands.checks.has_role(config.role.administrater_role_id)
    @app_commands.guild_only()
    async def cpresent_user(self, interaction: discord.Interaction):

        PRESENT_DESCRIPTION = f"""
【応募条件】
1: このサーバーに抽選時に参加していること
2: 下のボタンを押すこと
([Twitter](https://x.com/Kikuna0402)をフォローしてくれると主が喜びます)

【景品内容】
1名 : 星街すいせいバンドル(3000V-BUCKSのやつ) or 1000V-BUCKS(ギフトカードのやつ)

【その他】
・2アカウント以上の応募・ボタンの連打は禁止です
→発覚次第応募権はく奪します
・当選確率アップはありません
・景品はどちらか選べます

【締め切り】{datetime.now().strftime('%Y/%m/%d')} 23:59
【当選発表】{(datetime.now() + timedelta(days=1)).strftime('%Y/%m/%d')} 00:00
"""
        present_embed = discord.Embed(
            title="すいちゃんスキンプレゼント企画!",
            description=PRESENT_DESCRIPTION,
            color=0x87ea00,
            timestamp=datetime.now()
        )
        present_embed.set_footer(text="Bot開発・主催:菊菜(きくな)")
        await interaction.response.send_message("送信しました", ephemeral=True)
        await interaction.channel.send("突如始まる運のみで決まるプレゼント企画(笑)", embed=present_embed)
        await interaction.channel.send(view=Lottery(self.bot))

    @app_commands.command(name="happyou", description="buttonのみ送信")
    @app_commands.checks.has_role(config.role.administrater_role_id)
    @app_commands.guild_only()
    async def tousennsya(self, interaction: discord.Interaction):
        oubouser = session.query(User).all()
        if len(oubouser) == 0:
            await interaction.channel.send("応募者はいませんでした。")
            return
        winner_num = random.randint(1, len(oubouser))
        for user in oubouser:
            if user.no == winner_num:
                embed = discord.Embed(
                    title="当選発表",
                    description=f"# 当選者発表\n## <@{user.userid}>さん\nおめでとうございます!!!\n景品は星街すいせいバンドルか1000V-BUCKSのどちらかになります。\nご希望の景品をDMにてお知らせください。",
                    color=0x87ea00,
                    timestamp=datetime.now()
                )
                await interaction.channel.send(f"<@{user.userid}>", embed=embed)
    
    @app_commands.command(name="button", description="buttonのみ送信")
    @app_commands.checks.has_role(config.role.administrater_role_id)
    @app_commands.guild_only()
    async def send_button(self, interaction: discord.Interaction):
        await interaction.channel.send(view=Lottery(self.bot))


async def setup(bot: commands.Bot):
    await bot.add_cog(Present(bot))
    bot.add_view(Lottery(bot))
