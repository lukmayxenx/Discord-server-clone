# Xenx Developer
# ห้ามนำไปหายหรือใช้ในเชิงพาณิชย์น่ะอีสัส

import requests
import time

TOKEN = ""                 # Bot token หรือ User token
IS_BOT = False  		   # True = bot token, False = user token
SOURCE_GUILD_ID = 123456   # เซิร์ฟเวอร์ต้นทางที่จะก็อป
TARGET_GUILD_ID = 123456   # เซิร์ฟเวอร์ปลายทางที่จะสร้างใหม่
DELETE_EXISTING = True     # ลบ role/channel เดิมในเป้าหมายก่อน (ยกเว้น @everyone)

BASE = "https://discord.com/api/v10"

def headers():
    h = {"Authorization": f"Bot {TOKEN}" if IS_BOT else TOKEN}
    return h

def req(method, path, **kw):
    r = requests.request(method, BASE + path, headers=headers(), **kw)
    if r.status_code == 429:  # ratelimit
        retry = r.json().get("retry_after", 1)
        print(f"  [ratelimit] รอ {retry}s ...")
        time.sleep(retry + 0.5)
        return req(method, path, **kw)
    if not r.ok:
        print(f"  [ERR {r.status_code}] {path}: {r.text[:200]}")
    return r

def get(path):
    return req("GET", path).json()

def post(path, json_data):
    return req("POST", path, json=json_data)

def patch(path, json_data):
    return req("PATCH", path, json=json_data)

def delete(path):
    return req("DELETE", path)


def wipe_target(guild_id, everyone_id):
    print("[*] เคลียร์เซิร์ฟเวอร์ปลายทาง ...")
    roles = get(f"/guilds/{guild_id}/roles")
    for role in roles:
        if role["id"] == everyone_id or role.get("managed"):
            continue
        delete(f"/guilds/{guild_id}/roles/{role['id']}")

    channels = get(f"/guilds/{guild_id}/channels")
    for ch in channels:
        delete(f"/channels/{ch['id']}")
    print("[+] เคลียร์เสร็จ")


def clone():
    src = SOURCE_GUILD_ID
    dst = TARGET_GUILD_ID

    src_roles = get(f"/guilds/{src}/roles")
    src_channels = get(f"/guilds/{src}/channels")

    print("[*] กำลังก็อป Roles ...")
    src_roles_sorted = sorted(src_roles, key=lambda r: r["position"])
    everyone_id = next(r["id"] for r in src_roles_sorted if r["name"] == "@everyone")

    if DELETE_EXISTING:
        tgt_roles = get(f"/guilds/{dst}/roles")
        tgt_everyone = next(r["id"] for r in tgt_roles if r["name"] == "@everyone")
        src_everyone = next(r for r in src_roles if r["name"] == "@everyone")
        patch(f"/guilds/{dst}/roles/{tgt_everyone}",
              {"permissions": src_everyone["permissions"]})
        for r in tgt_roles:
            if r["id"] != tgt_everyone and not r.get("managed"):
                delete(f"/guilds/{dst}/roles/{r['id']}")

    role_map = {}   
    for role in sorted(src_roles, key=lambda r: r["position"], reverse=True):
        if role["name"] == "@everyone" or role.get("managed"):
            continue
        data = {
            "name": role["name"],
            "permissions": role["permissions"],
            "color": role["color"],
            "hoist": role["hoist"],
            "mentionable": role["mentionable"],
        }
        r = post(f"/guilds/{dst}/roles", data)
        if r.ok:
            role_map[role["id"]] = r.json()["id"]
            print(f"    + role: {role['name']}")
        time.sleep(0.3)
        
    print("[*] กำลังก็อป Channels ...")
    categories = [c for c in src_channels if c["type"] == 4]
    normal = [c for c in src_channels if c["type"] != 4]

    def convert_overwrites(overwrites):
        out = []
        for ow in overwrites:
            oid = ow["id"]
            if oid in role_map:
                oid = role_map[oid]
            elif oid == everyone_id:
                tgt_roles = get(f"/guilds/{dst}/roles")
                oid = next(r["id"] for r in tgt_roles if r["name"] == "@everyone")
            elif ow["type"] == 1: 
                continue
            else:
                continue
            out.append({
                "id": str(oid),
                "type": ow["type"],
                "allow": ow["allow"],
                "deny": ow["deny"],
            })
        return out

    cat_map = {}
    for cat in sorted(categories, key=lambda c: c["position"]):
        data = {
            "name": cat["name"],
            "type": 4,
            "position": cat["position"],
            "permission_overwrites": convert_overwrites(cat.get("permission_overwrites", [])),
        }
        r = post(f"/guilds/{dst}/channels", data)
        if r.ok:
            cat_map[cat["id"]] = r.json()["id"]
            print(f"    + category: {cat['name']}")
        time.sleep(0.3)

    for ch in sorted(normal, key=lambda c: c["position"]):
        data = {
            "name": ch["name"],
            "type": ch["type"],
            "topic": ch.get("topic"),
            "nsfw": ch.get("nsfw", False),
            "bitrate": ch.get("bitrate"),
            "user_limit": ch.get("user_limit"),
            "rate_limit_per_user": ch.get("rate_limit_per_user", 0),
            "position": ch.get("position", 0),
            "permission_overwrites": convert_overwrites(ch.get("permission_overwrites", [])),
        }
        if ch.get("parent_id") and ch["parent_id"] in cat_map:
            data["parent_id"] = cat_map[ch["parent_id"]]
        r = post(f"/guilds/{dst}/channels", data)
        if r.ok:
            print(f"    + channel: {ch['name']}")
        time.sleep(0.3)

    print("\n[✓] ก็อปเสร็จสิ้น! Roles + Channels + Permissions ถูกสร้างในเซิร์ฟเวอร์ปลายทางแล้ว")


if __name__ == "__main__":
    clone()
