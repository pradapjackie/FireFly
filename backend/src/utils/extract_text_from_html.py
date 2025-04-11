from lxml.html.clean import Cleaner


def extract_text_from_html(html: str) -> str:
    if "<" in html and ">" in html:
        cleaner = Cleaner(remove_unknown_tags=False, remove_tags=["a", "p", "div", "ul", "li"], page_structure=False)
        html = cleaner.clean_html(html)
        html = html.replace("\n", " ")
        html = html.replace("\r", "")
        html = html.replace("<div>", "")
        html = html.replace("</div>", "")
        html = html.strip()
        return html
    return html
