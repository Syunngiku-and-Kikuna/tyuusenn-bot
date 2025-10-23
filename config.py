class Roles():
    rsl1: int = 1
    rsl2: int = 1392060380561408052
    rsc1: int = 1397899288553717770
    rsc2: int = 1
    rsc3: int = 1
    rsc4: int = 1
    rsc5: int = 1
    rsc6: int = 1
    rsc7: int = 1
    rsc8: int = 1
    rsc9: int = 1
    rsc10: int = 1
    administrater_role_id: int = 1  # 鯖管理者ロールID


class Channels():
    important_log: int = 1399287484621262979  # 重要ログチャンネル#//Now：テスト鯖の重要logチャンネル
    log: int = 1399287447753588848  # ログチャンネル#//Now：テスト鯖のlogチャンネル


class Categories():
    announcement: int = 1  # 「重要項目」カテゴリー
    poll: int = 1  # 「投票用カテゴリー」
    server_management: int = 1  # 「鯖運営について」カテゴリー
    freechat: int = 1  # 「お話しするチャット」カテゴリー
    developer: int = 1397904744227278918  # 「開発カテゴリー」#//Now：テスト鯖の春菊の調理場
    information: int = 1  # 「情報チャット」カテゴリー
    showcase: int = 1  # 「掲示するところ」カテゴリー
    public_meeting: int = 1  # 「公開会議」カテゴリー


def load_token() -> str:
    with open("SybotTK.txt", "r") as f:
        d = f.read()
    return d


class Config:
    token: str = load_token()
    role: Roles = Roles()
    channel: Channels = Channels()
    category: Categories = Categories()


config = Config()
