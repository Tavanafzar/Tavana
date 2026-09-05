"""نگاشت پیشوندهای جستجو (مثل «یوتیوب :») به موتور/سایت جستجوی مربوطه."""

import webbrowser

SEARCH_MAP: dict[tuple[str, ...], str] = {
    ("یوتیوب :", "youtube :"): "https://www.youtube.com/results?search_query=",
    ("ویکی پدیا :", "wiki :", "wikipedia:"): "https://fa.wikipedia.org/wiki/",
    ("ایکس :", "x :"): "https://x.com/search?q=",
    ("پرسش :","ask AI:"): "http://www.perplexity.ai/search/new?&q="
}


def handle_search_prefix(text: str) -> bool:
    """اگر متن با یکی از پیشوندهای SEARCH_MAP شروع شود، جستجوی مربوطه را در مرورگر باز می‌کند."""
    text_lower = text.lower()

    for prefixes, url in SEARCH_MAP.items():
        for prefix in prefixes:
            if text_lower.startswith(prefix.lower()):
                query = text[len(prefix):].strip()
                webbrowser.open(url + query)
                return True

    return False
