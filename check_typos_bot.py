import requests
import re

# --- הגדרות ---
API_URL = "https://chabadpedia.co.il/api.php"  # כתובת ה-API של חב"דפדיה
HEADERS = {"User-Agent": "ChabadBot/1.0 (Script for checking typos)"}

# --- פונקציה להביא דפים מבוקשים ---
def get_mostwanted_pages(limit=50):
    params = {
        "action": "query",
        "list": "mostwantedpages",
        "mwlimit": limit,
        "format": "json"
    }
    response = requests.get(API_URL, params=params, headers=HEADERS)
    data = response.json()
    return [page["title"] for page in data.get("query", {}).get("mostwantedpages", [])]

# --- פונקציה לבדוק שגיאות כתיב פשוטות (דוגמה: אותיות חוזרות, תווים לא תקינים) ---
def check_typos(title):
    issues = []
    # דוגמה: שתי אותיות זהות רצופות יותר מדי פעמים
    if re.search(r'(.)\1{2,}', title):
        issues.append("אותות חוזרות")
    # דוגמה: תווים לא חוקיים (למשל סמלים מיוחדים)
    if re.search(r'[!@#$%^&*_=+<>]', title):
        issues.append("תווים מיוחדים")
    return issues

# --- לולאה ראשית ---
def main():
    pages = get_mostwanted_pages(limit=50)
    for title in pages:
        typos = check_typos(title)
        if typos:
            print(f"בעיות בדף: '{title}' -> {typos}")

if __name__ == "__main__":
    main()
