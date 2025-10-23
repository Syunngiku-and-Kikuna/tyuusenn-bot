class Roles():
    rsl1: int = 1
    rsl2: int = 1232143915449188482
    rsc1: int = 1232143942590533643
    rsc2: int = 1232143965634170890
    rsc3: int = 1
    rsc4: int = 1
    rsc5: int = 1
    rsc6: int = 1
    rsc7: int = 1
    rsc8: int = 1
    rsc9: int = 1
    rsc10: int = 1
    administrater_role_id: int = 1215981050292080640  # 鯖管理者ロールID


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
