
import mwclient
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

site = mwclient.Site('chabadpedia.co.il', path='/')
site.login('רובין בוט', '0537311474')

def is_valid_page(page):
    if page.namespace != 0:
        return False
    if page.length is None or page.length < 3000:
        return False
    text = page.text()
    forbidden_templates = ['{{להשלים', '{{בעבודה', '{{למ', '{{שכתוב', '{{חשיבות', '{{קצרמר', '{{עריכה', '{{מקורות', '{{לשכתב', '{{איחוד', '{{לעריכה דחופה']
    for tmpl in forbidden_templates:
        if tmpl in text:
            return False
    return True

def get_new_pages(site, limit=15, max_check=100):
    new_pages = []
    checked = 0
    for change in site.recentchanges(type='new', namespace=0, dir='older', limit=max_check):
        title = change['title']
        page = site.pages[title]
        if is_valid_page(page):
            new_pages.append(title)
        checked += 1
        if len(new_pages) >= limit or checked >= max_check:
            break
    return new_pages

def format_new_entries(pages):
    return '[[{}]]'.format(']] {{*}} [['.join(pages))

def update_template(site, new_line):
    page = site.pages['תבנית:ערכים חדשים']
    text = page.text()

    start_tag = '<!-- התחילו לערוך מכאן -->'
    end_tag = '<!-- נא לא לערוך מתחת לשורה זו -->'

    start_index = text.find(start_tag) + len(start_tag)
    end_index = text.find(end_tag)

    if start_index == -1 or end_index == -1:
        print("שגיאה: לא נמצאו התגיות בתבנית")
        return

    new_text = (
        text[:start_index] + '\n' +
        new_line.strip() + '\n' +
        text[end_index:]
    )

    page.edit(text=new_text, summary='עדכון ערכים חדשים על ידי הבוט')
    print("התבנית עודכנה בהצלחה")

# הרצה
if __name__ == '__main__':
    pages = get_new_pages(site, limit=15)
    print("הערכים שהתקבלו:", pages)
    new_line = format_new_entries(pages)
    update_template(site, new_line)
