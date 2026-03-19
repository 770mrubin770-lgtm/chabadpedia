#!/usr/bin/env python3

# clean_list_lines.py

# גרסה: 1.0

# שימוש: python3 clean_list_lines.py -i input.txt -o output.txt

# או: python3 clean_list_lines.py -i input.txt --inplace     (לשימור במקום + יצירת backup)

import argparse
import re
from pathlib import Path
import shutil
import sys

def clean_line(line: str) -> str:
"""
אם השורה (לאחר ריסוס רווחים מובילים) מתחילה ב־'*',
מסיר נקודות בסוף ומנקה רווחים מיותרים.
השיטה שומרת על ההזחה המקורית (leading whitespace).
"""
# שמירה על ההזחה המקורית
m = re.match(r'^(\s*)(.*)$', line)
if not m:
return line
leading, rest = m.group(1), m.group(2)
if rest.startswith('*'):
# מסיר רווחים אחרי הכוכבית ואז מסיר נקודה בסוף אם קיימת
# שומרים על המראה: leading + cleaned rest
# נרצה לא להסיר נקודות בתוך המשפט, רק בסוף
rest_clean = rest.rstrip()  # מסיר whitespace בסוף
if rest_clean.endswith('.'):
rest_clean = rest_clean[:-1]
# גם נוודא שאין רווח כפול מיותר אחרי הכוכבית:
rest_clean = re.sub(r'^*\s*', '* ', rest_clean)  # כוכבית ואחריה רווח אחד
return leading + rest_clean
else:
return line.rstrip('\n')

def process_text(text: str) -> str:
lines = text.splitlines()
cleaned = [clean_line(line) for line in lines]
# החזיר עם סיום שורה אחיד '\n'
return '\n'.join(cleaned) + ('\n' if text.endswith('\n') else '')

def main():
ap = argparse.ArgumentParser(description="נקה נקודות בסוף שורות שמתחילות ב-* בקובץ טקסט.")
ap.add_argument('-i', '--input', required=True, help="קובץ קלט (utf-8).")
ap.add_argument('-o', '--output', help="קובץ פלט. אם לא צוין — יודפס ל־stdout.")
ap.add_argument('--inplace', action='store_true', help="לערוך במקום (כותב חזרה לקובץ הקלט). יוצרת גיבוי input.bak.")
ap.add_argument('--backup-ext', default='.bak', help="סיומת הגיבוי כש--inplace פעיל (ברירת מחדל: .bak).")
args = ap.parse_args()

```
in_path = Path(args.input)
if not in_path.exists():
    print(f"ERROR: קובץ לא נמצא: {in_path}", file=sys.stderr)
    sys.exit(2)

raw = in_path.read_text(encoding='utf-8')
out_text = process_text(raw)

if args.inplace:
    backup_path = in_path.with_suffix(in_path.suffix + args.backup_ext) if in_path.suffix else Path(str(in_path) + args.backup_ext)
    shutil.copy2(in_path, backup_path)
    in_path.write_text(out_text, encoding='utf-8')
    print(f"נערך במקום. גיבוי נוצר ב: {backup_path}")
elif args.output:
    out_path = Path(args.output)
    out_path.write_text(out_text, encoding='utf-8')
    print(f"נכתב לקובץ: {out_path}")
else:
    # פלט ל־stdout
    sys.stdout.write(out_text)
```

if **name** == '**main**':
main()
