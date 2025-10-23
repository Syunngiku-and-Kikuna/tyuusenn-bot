class Roles():
    rsl1: int = 1
    rsl2: int = 994237636745101342
    rsc1: int = 1011204987365371914
    rsc2: int = 1121958514366087321
    rsc3: int = 1121958514366087321
    rsc4: int = 1263077856867782727
    rsc5: int = 1405855317702606909
    rsc6: int = 1
    rsc7: int = 1
    rsc8: int = 1
    rsc9: int = 1
    rsc10: int = 1
    administrater_role_id: int = 1006568446449958913  # 鯖管理者ロールID


class Channels():
    important_log: int = 1


class Categories():
    announcement: int = 1  


def load_token() -> str:
    with open("TSTK.txt", "r") as f:
        d = f.read()
    return d


class Config:
    token: str = load_token()
    role: Roles = Roles()
    channel: Channels = Channels()
    category: Categories = Categories()


config = Config()
