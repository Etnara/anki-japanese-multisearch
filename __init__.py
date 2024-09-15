from anki import hooks
from aqt.qt import QDesktopServices, QUrl, QGuiApplication, QClipboard

JISHO_URL= "https://jisho.org/search/"
RTK_URL = "https://hochanh.github.io/rtk/"
WIKITIONARY_URL = "https://en.wiktionary.org/wiki/"
TOOLZAR_URL = "https://kanji.toolzar.com/"
YOUGLISH_URL = "https://youglish.com/pronounce/"

def keep_kanji(text):
    kanji = [x for x in text if 19968 <= ord(x) <= 40895]
    return ''.join(kanji)

def add_to_context_menu(view, menu):
    selected = view.page().selectedText()
    if not selected:
        return

    gap = menu.addAction(" ")

    # Search Everything
    jisho = menu.addAction("Jisho: " + selected)
    jisho.triggered.connect(lambda: QDesktopServices.openUrl(QUrl(JISHO_URL + selected)))
    wiktionary = menu.addAction("Wikitionary: " + selected)
    wiktionary.triggered.connect(lambda: QDesktopServices.openUrl(QUrl(WIKITIONARY_URL + selected)))
    youglish = menu.addAction("YouGlish: " + selected)
    youglish.triggered.connect(lambda: QDesktopServices.openUrl(QUrl(YOUGLISH_URL + selected + "/japanese")))

    # Search Kanji Only
    selected_kanji = keep_kanji(selected)
    if not selected_kanji:
        return

    gap2 = menu.addAction(" ")

    jishoKanji = menu.addAction("Jisho Kanji: " + selected_kanji)
    jishoKanji.triggered.connect(lambda: QDesktopServices.openUrl(QUrl(JISHO_URL + selected_kanji + " %23kanji")))

    rtk = menu.addAction("RTK: " + selected_kanji)
    for x in selected_kanji:
        rtk.triggered.connect(lambda check, x=x: QDesktopServices.openUrl(QUrl(RTK_URL + x)))

    toolzar = menu.addAction("Toolzar: " + selected_kanji + " (Paste manually)")
    toolzar.triggered.connect(lambda: QDesktopServices.openUrl(QUrl(TOOLZAR_URL)))
    toolzar.triggered.connect(lambda: QGuiApplication.clipboard().setText(selected_kanji))

hooks.addHook("AnkiWebView.contextMenuEvent", add_to_context_menu)

