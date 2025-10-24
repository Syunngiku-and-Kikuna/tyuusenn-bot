from discord.ext import commands
from datetime import datetime, timedelta
from discord import ButtonStyle, app_commands
from database import User, session
import discord
from config import config
import asyncio


class Lottery(discord.ui.View):  # 抽選コマンド
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="応募", style=ButtonStyle.green, emoji="✅", custom_id="present")
    async def pressedLotteryButton(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.defer(thinking=True, ephemeral=True)
        oubouser = session.query(User).filter_by(userid=interaction.user.id).first()
        rsl2 = interaction.guild.get_role(config.role.rsl2)
        rsc1 = interaction.guild.get_role(config.role.rsc1)
        rsc2 = interaction.guild.get_role(config.role.rsc2)
        rsc3 = interaction.guild.get_role(config.role.rsc3)
        rsc4 = interaction.guild.get_role(config.role.rsc4)
        rsc5 = interaction.guild.get_role(config.role.rsc5)
        point = 0
        if oubouser is None:
            userdb = User(userid=interaction.user.id, username=interaction.user.name)
            session.add(userdb)
            session.commit()
            await interaction.followup.send("データベースが作成されました。もう一度[応募ボタン]を押してください\n-# 1回で応募まで完了させたかったんだけど多分仕様的に無理っぽい(笑)", ephemeral=True)
            return
        if oubouser.oubo is True:
            await interaction.followup.send("すでに応募済みです。抽選開始までお待ちください。", ephemeral=True)
            oubouser.pushbutton += 1
            session.commit()
            return
        if rsl2 in interaction.user.roles:
            oubouser.rsl2 = True
            point += 1
            await asyncio.sleep(1)  # 少し待機してから再取得
        if rsc1 in interaction.user.roles:
            oubouser.rsc1 = True
            point += 1
            await asyncio.sleep(1)  # 少し待機してから再取得
        if rsc2 in interaction.user.roles:
            oubouser.rsc2 = True
            point += 1
            await asyncio.sleep(1)  # 少し待機してから再取得
        if rsc3 in interaction.user.roles:
            oubouser.rsc3 = True
            point += 1
            await asyncio.sleep(1)  # 少し待機してから再取得
        if rsc4 in interaction.user.roles:
            oubouser.rsc4 = True
            point += 1
            await asyncio.sleep(1)  # 少し待機してから再取得
        if rsc5 in interaction.user.roles:
            oubouser.rsc5 = True
            point += 1
            await asyncio.sleep(1)  # 少し待機してから再取得
        if point == 0:
            await interaction.followup.send("応募資格がありません\n応募条件を読んできてください", ephemeral=True)
            oubouser.pushbutton += 1
            session.commit()
            return
        else:
            oubouser.oubo = True  # 応募済み
            oubouser.pushbutton += 1
            session.commit()
            await interaction.followup.send(f"{point}口応募されました。抽選開始までお待ちください。", ephemeral=True)

    @discord.ui.button(label="応募状況確認", style=ButtonStyle.blurple, custom_id="check")
    async def pressedCheckButton(self, interaction: discord.Interaction, button: discord.ui.button):
        oubouser = session.query(User).filter_by(userid=interaction.user.id).first()
        if oubouser is None:
            await interaction.response.send_message("まだ応募されていません。応募ボタンを押して応募してください。", ephemeral=True)
            return
        if oubouser.oubo is True:
            rsl2status = "取得済み(応募権)" if oubouser.rsl2 else "なし"
            rsc1status = "取得済み(応募権)" if oubouser.rsc1 else "なし"
            rsc2status = "取得済み(応募権)" if oubouser.rsc2 else "なし"
            rsc3status = "取得済み(応募権)" if oubouser.rsc3 else "なし"
            rsc4status = "取得済み(応募権)" if oubouser.rsc4 else "なし"
            rsc5status = "取得済み(応募権)" if oubouser.rsc5 else "なし"
            CHDESC = f"""
<@{interaction.user.id}> さんの応募状況は以下の通りです。
応募権1つにつき1口応募されます。

> <@&{config.role.rsl2}> : {rsl2status}
> <@&{config.role.rsc1}> : {rsc1status}
> <@&{config.role.rsc2}> : {rsc2status}
> <@&{config.role.rsc3}> : {rsc3status}
> <@&{config.role.rsc4}> : {rsc4status}
> <@&{config.role.rsc5}> : {rsc5status}

合計応募口数 : {sum([oubouser.rsl2, oubouser.rsc1, oubouser.rsc2, oubouser.rsc3, oubouser.rsc4, oubouser.rsc5])}口
"""
            chembed = discord.Embed(
                title="応募状況確認",
                description=CHDESC,
                color=0x00ff00
            )
            await interaction.response.send_message("応募済みです。抽選開始までお待ちください。", embed=chembed, ephemeral=True)
        else:
            await interaction.response.send_message("まだ応募されていません。応募ボタンを押して応募してください。", ephemeral=True)

    @discord.ui.button(label="企画終了", style=ButtonStyle.red, custom_id="delevent")
    async def pressedDeleventButton(self, interaction: discord.Interaction, button: discord.ui.button):
        role = interaction.guild.get_role(config.role.administrater_role_id)
        if role in interaction.user.roles:
            await interaction.message.delete()
        else:
            await interaction.response.send_message("権限ないで", ephemeral=True)
            oubouser = session.query(User).filter_by(userid=interaction.user.id).first()
            oubouser.pushbutton += 1
            session.commit()


class Present(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

# !--------------------------------------------------------------------

    @app_commands.command(name="present", description="【運営】present企画")
    @app_commands.describe(
        serveruser="サーバー人数(100の倍数で入力)",
        kikann="応募期間(日数入力)"
    )
    @app_commands.checks.has_role(config.role.administrater_role_id)
    @app_commands.guild_only()
    async def cpresent_user(self, interaction: discord.Interaction, serveruser: int, kikann: int):

        syuuryoubi = datetime.now() + timedelta(days=kikann)
        fsyuuryoubi = syuuryoubi.strftime(" %Y/%m/%d ")
        tyuusennbi = syuuryoubi + timedelta(days=1)
        ftyuusennbi = tyuusennbi.strftime(" %Y/%m/%d ")

        PRESENT_DESCRIPTION = f"""
【応募条件】
1: このサーバーに抽選時に参加していること
2: 過去にれぞらんど/緑黄色クラフトに参加していること
(Resoland2参加者,Ryokuousyoku1,2,3,4,5参加者ロールのいずれかを持っていること)
3: 下のボタンを押すこと

【景品内容】
1名 : Discord Nitro 1ヶ月分

【その他】
・2アカウント以上の応募・ボタンの連打は禁止です
→発覚次第その回の全アカウントでの応募権はく奪します
・参加者ロールが多いほど当選確率が上がります
(Ryokuousyoku1～5参加者ロール持ってたら5口応募になります)
・鯖主は参加権ないです(笑)

【締め切り】{fsyuuryoubi} 23:59
【当選発表】{ftyuusennbi} 18:00
"""
        present_embed = discord.Embed(
            title=f"{serveruser}人突破記念プチプレゼント企画!",
            description=PRESENT_DESCRIPTION,
            color=0x87ea00,
            timestamp=datetime.now()
        )
        await interaction.response.send_message("送信しました", ephemeral=True)
        await interaction.channel.send(embed=present_embed)
        await interaction.channel.send(view=Lottery(self.bot))

    @app_commands.command(name="present-reset", description="【運営】present企画-リセットコマンド")
    @app_commands.checks.has_role(config.role.administrater_role_id)
    @app_commands.guild_only()
    async def cpresentreset(self, interaction: discord.Interaction):
        results = session.query(User).all()
        for i in results:
            i.oubo = False  # 応募済みをリセット
        session.commit()
        print("リセット完了")
        await interaction.response.send_message("リセットしました", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Present(bot))
    bot.add_view(Lottery(bot))
