import os
import re

from bs4 import BeautifulSoup

HN_HTTP = "http://news.ycombinator.com"
HN_HTTPS = "https://news.ycombinator.com"
HOST = os.environ.get('HOST', "127.0.0.1")
PORT = int(os.environ.get('PORT', 8000))
TM = "™"


def add_trademark_to_word(matchobj):
    word = matchobj.group(0)
    return f"{word}{TM}"


def trademarkify_text(tag_text):
    regex = r'(?<=[\s>("]{1})[a-zA-Z]{6}(?=[\s<)".,!?:;]{1})'
    new_tag_text = re.sub(regex, add_trademark_to_word, f" {tag_text} ")
    return new_tag_text[1:-1]


def trademarkify_tag(tag_soup):
    tag_text = str(tag_soup)
    new_tag_text = trademarkify_text(tag_text)
    new_tag_soup = BeautifulSoup(new_tag_text, "html.parser")
    return new_tag_soup


def rewrite_page_title(soup):
    title = soup.find("title")
    if not title:
        return

    title.string.replace_with(trademarkify_text(title.string))


def rewrite_links(soup):
    server_url = f"http://{HOST}:{PORT}"
    for link in soup("a"):
        if isinstance(link.contents[0], str):
            link.string.replace_with(trademarkify_text(link.string))

        href = link.get("href")
        if href.startswith(HN_HTTP):
            link["href"] = href.replace(HN_HTTP, server_url)
        if href.startswith(HN_HTTPS):
            link["href"] = href.replace(HN_HTTPS, server_url)


def rewrite_scores(soup):
    scores = soup.find_all("span", class_="score")
    for score in scores:
        score.string.replace_with(trademarkify_text(score.string))


def rewrite_post_description(soup):
    table = soup.find("table", class_="fatitem")
    if not table:
        return

    rows = table.find_all("tr")
    if len(rows) != 6:
        return

    fourth_row = rows[3]
    cols = fourth_row.find_all("td")
    second_col = cols[1]
    second_col.replace_with(trademarkify_tag(second_col))


def rewrite_post_comments(soup):
    tags = soup.find_all("span", class_="commtext")
    for tag in tags:
        tag.replace_with(trademarkify_tag(tag))


def rewrite_footer_search(soup):
    form = soup.find("form", action="//hn.algolia.com/")
    if not form:
        return

    form.replace_with(trademarkify_tag(form))


def trademarkify_page_html(html):
    soup = BeautifulSoup(html, "html.parser")
    rewrite_page_title(soup)
    rewrite_links(soup)
    rewrite_scores(soup)
    rewrite_post_description(soup)
    rewrite_post_comments(soup)
    rewrite_footer_search(soup)
    trademarkified_html = str(soup)
    return trademarkified_html
