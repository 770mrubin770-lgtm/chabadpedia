import mwclient
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

site = mwclient.Site('chabadpedia.co.il', path='/')
site.login('רובין בוט', '0537311474')

# -------------------------
# בדיקה אם הדף הוא הפניה
# -------------------------
def is_redirect(page):
    try:
        if page.redirect:
            return True
    except Exception:
        pass

    try:
        text = page.text()
        if text.lstrip().lower().startswith(('#redirect', '#הפניה')):
            return True
    except Exception:
        pass

    return False


# -------------------------
# בדיקה האם הערך עומד בקריטריונים
# -------------------------
def is_valid_page(page):
    if page.namespace != 0:
        return False

    if is_redirect(page):
        return False

    if page.length is None or page.length < 3000:
        return False

    text = page.text()

    forbidden_templates = [
        '{{להשלים', '{{בעבודה', '{{למ', '{{שכתוב', '{{חשיבות',
        '{{קצרמר', '{{עריכה', '{{מקורות', '{{לשכתב',
        '{{איחוד', '{{
