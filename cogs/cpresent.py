from discord.ext import commands, tasks
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

    @discord.ui.button(label="参加", style=ButtonStyle.green, emoji="✅", custom_id="present")
    async def pressedLotteryButton(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.defer(thinking=True, ephemeral=True)
        oubouser = session.query(User).filter_by(userid=interaction.user.id).first()

        if oubouser is None:
            userdb = User(userid=interaction.user.id, username=interaction.user.name, displayname=interaction.user.display_name)
            session.add(userdb)
            session.commit()
            await interaction.followup.send("参加が完了しました。当選発表までお待ちください。", ephemeral=True)
            return
        else:
            await interaction.followup.send("すでに参加済みです。当選発表までお待ちください。", ephemeral=True)
            return

    @discord.ui.button(label="参加状況確認", style=ButtonStyle.blurple, custom_id="check")
    async def pressedCheckButton(self, interaction: discord.Interaction, button: discord.ui.button):
        oubouser = session.query(User).filter_by(userid=interaction.user.id).first()
        if oubouser is None:
            await interaction.response.send_message("まだ参加されていません。参加ボタンを押して参加してください。", ephemeral=True)
            return
        else:
            await interaction.response.send_message("参加完了してます。当選発表までお待ちください。", ephemeral=True)

    @discord.ui.button(label="企画終了", style=ButtonStyle.red, custom_id="delevent")
    async def pressedDeleventButton(self, interaction: discord.Interaction, button: discord.ui.button):
        if interaction.user.id == config.syunngiku_id:
            await interaction.message.delete()
        else:
            await interaction.response.send_message("権限ないで", ephemeral=True)


class Present(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.send_task.start()

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
        await interaction.channel.send(embed=present_embed)
        await interaction.channel.send(view=Lottery(self.bot))

    @tasks.loop(seconds=60)
    async def send_task(self):
        now = datetime.now()
        if now.hour == 00 and now.minute == 00:
            ch = await self.bot.fetch_channel(config.channel.nitice)
            oubouser = session.query(User).all()
            if len(oubouser) == 0:
                await ch.send("応募者はいませんでした。")
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
                    await ch.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Present(bot))
    bot.add_view(Lottery(bot))
