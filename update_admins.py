import requests
from datetime import date

# ---------- הגדרות ----------
API_URL = "https://chabadpedia.co.il/api.php"
USERNAME = "רובין בוט"
PASSWORD = "" 
PAGE_TITLE = "חב\"דפדיה:נתונים סטטיסטיים/משתמשים/מפעילים, ביורוקרטים ועורכי ממשק"

session = requests.Session()

# ---------- קבלת login token ----------
r = session.get(API_URL, params={
    "action": "query",
    "meta": "tokens",
    "type": "login",
    "format": "json"
})
login_token = r.json()["query"]["tokens"]["logintoken"]

# ---------- התחברות ----------
r = session.post(API_URL, data={
    "action": "login",
    "lgname": USERNAME,
    "lgpassword": PASSWORD,
    "lgtoken": login_token,
    "format": "json"
})
print("Login:", r.json())

# ---------- קבלת csrf token לעריכה ----------
r = session.get(API_URL, params={"action": "query", "meta": "tokens", "format": "json"})
csrf_token = r.json()["query"]["tokens"]["csrftoken"]

# ---------- פונקציה להבאת משתמשים לפי קבוצה ----------
def get_users(group):
    users = []
    r = session.get(API_URL, params={
        "action": "query",
        "list": "allusers",
        "augroup": group,
        "aulimit": "max",
        "format": "json"
    })
    for u in r.json()["query"]["allusers"]:
        users.append(u["name"])
    return users

# ---------- קבלת רשימות משתמשים ----------
admins = get_users("sysop")
bcrats = get_users("bureaucrat")
intadmins = get_users("interface-admin")

all_users = admins + bcrats + intadmins

# ---------- פונקציה לחישוב מיון לדוגמה ----------
def compute_sort_values(edits):
    return edits % 1000, edits  # 3 ספרות, 6 ספרות

# ---------- בניית תוכן הטבלה ----------
today = date.today().isoformat()
content = f"{{{{חב\"דפדיה - כותרת טבלת נתוני מפעילים - גרסת {today}||{today}||{today}}}}}\n"

for user in all_users:
    edits = 12345  # ניתן לשים כאן עריכת אמת אם רוצים למשוך מה-API
    m3, m6 = compute_sort_values(edits)
    content += (
        f"|-valign=\"top\"\n"
        f"|{{{{משתמש|{user}|קיצור=כן}}}}\n"
        f"!bgcolor=\"#CCCCCC\"|{{{{שינוי|0}}}}\n"
        f"|bgcolor=\"#CCCCCC\"|<b>{{{{מיון 3 ספרות|{m3}}}}}</b>\n"
        f"|bgcolor=\"#B0FFFF\"|<b>{{{{מיון 6 ספרות|{m6}}}}}</b>\n"
    )

# ---------- סיום הטבלה ----------
content += "\n{{ניווט סטטיסטיקת המכלול}}\n[[קטגוריה:המכלול:נתונים סטטיסטיים|מפעילים]]\n{{וח}}"

# ---------- עדכון הדף ----------
r = session.post(API_URL, data={
    "action": "edit",
    "title": PAGE_TITLE,
    "text": content,
    "token": csrf_token,
    "format": "json",
    "summary": "עדכון אוטומטי של הנתונים"
})
print("Edit:", r.json())
