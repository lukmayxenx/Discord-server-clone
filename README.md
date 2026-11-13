# Discord Cloner

เครื่องมือโคลนเซิร์ฟเวอร์ Discord แบบครบจบในไฟล์เดียว — ดูด **Role / Category / Channel / Permissions** จากเซิร์ฟเวอร์ต้นทาง ไปสร้างใหม่ในเซิร์ฟเวอร์ปลายทาง

> **คำเตือน:** เครื่องมือนี้ใช้งานผ่าน Discord API โดยตรง การใช้ **User Token (self-bot)** ผิดข้อกำหนดของ Discord (ToS) และมีความเสี่ยงถูกแบนบัญชี โปรดใช้วิจารณญาณ — ผู้ใช้รับผิดชอบการใช้งานเองทั้งหมด ใช้ได้เฉพาะกับเซิร์ฟเวอร์ที่คุณมีสิทธิ์เท่านั้น

---

## ฟีเจอร์

| ฟีเจอร์ | รายละเอียด |
|---|---|
| โครงสร้างเซิร์ฟเวอร์ | Role, Category, Text/Voice/Announcement/Forum channel + Permission Overwrites |

---

## ติดตั้ง (Ubuntu Linux / Debian / Ubuntu)

```bash
sudo apt update && sudo apt install -y python3 python3-pip
pip3 install requests --break-system-packages
```

> หรือใช้ venv เพื่อไม่ปน system package:
> ```bash
> python3 -m venv venv && source venv/bin/activate
> pip install requests
> ```

---

## วิธีใช้งาน

```bash
# 1) ดูรายชื่อช่องทั้งหมดของเซิร์ฟเวอร์ต้นทาง (✓ = ช่องที่จะถูกก็อป)
python3 discord.py list

# 3) ก็อปเต็มรูปแบบ
python3 discord.py
```

### การหา ID / Token

- **Guild / Channel ID:** Discord → Settings → Advanced → เปิด **Developer Mode** → คลิกขวาที่เซิร์ฟเวอร์/ช่อง → Copy ID
- **User Token:** เปิด discord.com บนเบราว์เซอร์ → F12 → tab **Network** → หา request ไป `discord.com/api` → ดู header `Authorization`
- **Bot Token:** [Discord Developer Portal](https://discord.com/developers/applications) → Application → Bot → Reset Token


## ปัญหาที่เจอบ่อย

| อาการ | สาเหตุ / วิธีแก้ |
|---|---|
| `401 Unauthorized` | ใช้ user token แต่ลืมตั้ง `*_is_bot: False` (หรือ token หมดอายุ ต้องดึงใหม่) |
| `403 Forbidden` | token ไม่มีสิทธิ์ในช่อง/เซิร์ฟเวอร์นั้น |
| ช่องบางช่องไม่โผล่ใน `list` | token ไม่มี `View Channel` ในช่องนั้น |
| ข้อความชื่อเราเองหมด | สร้าง webhook ไม่ได้ (ขาด `Manage Webhooks`) หรือ `use_webhook: False` |
| `429` บ่อย | เพิ่ม `speed_delay` เช่น `[1.0, 2.0]` |
| ไฟล์ไม่ถูกอัปโหลด | ไฟล์ใหญ่เกิน `max_attachment_mb` (จะเขียนลิงก์แทน) |

---

## ข้อจำกัด

- สมาชิก / voice state / ข้อความเสียง ก็อปผ่าน API ไม่ได้
- ไฟล์ใหญ่กว่าขีดจำกัด upload ของเซิร์ฟเวอร์ปลายทาง (เริ่มต้น 10MB) ต้องมี boost
- Role ที่เป็น managed (ของ bot) จะถูกข้าม
- ช่องที่ token ไม่มีสิทธิ์มองเห็น จะอ่าน/ก็อปไม่ได้
- ใช้ User token ผิด ToS — เสี่ยงถูกแบนบัญชี ควรใช้ bot token ที่เป็นไปได้

---

## License

โปรเจกต์นี้เผยแพร่เพื่อการศึกษาและใช้กับเซิร์ฟเวอร์ของตนเองเท่านั้น ผู้ใช้รับผิดชอบการใช้งานของตนเอง

## ⭐ ถ้าชอบกด Star ให้ด้วยนะ
