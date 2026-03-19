import mwclient
import requests
import json

# התחברות לאתר חב"דפדיה
site = mwclient.Site('chabadpedia.co.il', path='/')
site.login('רובין בוט', '0537311474')

# כתובת ה-API שמספקת את הנתונים
STATS_URL = 'https://chabadpedia-stats.vercel.app/api/stats'

# מיפוי מחדש של שמות הפעולות
ACTION_MAP = {
    'activeusers': 'activeUsers',
    'admins': 'admins',
    'articles': 'articles',
    'edits': 'edits',
    'files': 'files',
    'pages': 'pages',
    'users': 'users',
}

# מיפוי שמות האתרים במבנה שמודול Lua מבין
SITE_MAP = {
    'chabadpedia.co.il': 'chabadpedia',
    'text.chabadpedia.com': 'text.chabadpedia',
    'zitut.chabadpedia.com': 'zitut.chabadpedia',
    'chabadpedia.com': 'chabadpedia.com'
}

def fetch_data():
    response = requests.get(STATS_URL)
    response.raise_for_status()
    return response.json()

def build_module_data(stats_data):
    lines = [
        "return {",
        "    map = {"
    ]
    for key, val in ACTION_MAP.items():
        lines.append(f"        {key} = '{val}',")
    lines.append("    },")
    lines.append("    data = {")

    for domain, site_name in SITE_MAP.items():
        if domain in stats_data:
            stats = stats_data[domain]
            lines.append(f"        ['{site_name}'] = {{")
            for key in ACTION_MAP.values():
                lines.append(f"            {key} = {stats.get(key, 0)},")
            lines.append("        },")
    lines.append("    }")
    lines.append("}")

    return '\n'.join(lines)

def update_module(content):
    page = site.pages['Module:NUMBEROF/data']
    page.edit(text=content, summary='עדכון נתוני סטטיסטיקה אוטומטי על ידי רובין בוט')

def main():
    print("טוען נתונים מהשרת...")
    stats = fetch_data()
    print("בונה קובץ LUA...")
    content = build_module_data(stats)
    print("מעדכן את הדף בוויקי...")
    update_module(content)
    print("העדכון בוצע בהצלחה!")

if __name__ == '__main__':
    main()
