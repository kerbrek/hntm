from hntm.utils import trademarkify_page_html


def test_trademarkify_home_page():
    with open("tests/fixtures/home_before.html", encoding="utf-8") as before_fp:
        home_before_html = before_fp.read()
    with open("tests/fixtures/home_after.html", encoding="utf-8") as after_fp:
        home_after_html = after_fp.read()

    assert trademarkify_page_html(home_before_html) == home_after_html


def test_trademarkify_post_page():
    with open("tests/fixtures/post_before.html", encoding="utf-8") as before_fp:
        post_before_html = before_fp.read()
    with open("tests/fixtures/post_after.html", encoding="utf-8") as after_fp:
        post_after_html = after_fp.read()

    assert trademarkify_page_html(post_before_html) == post_after_html


def test_trademarkify_ask_page():
    with open("tests/fixtures/ask_before.html", encoding="utf-8") as before_fp:
        ask_before_html = before_fp.read()
    with open("tests/fixtures/ask_after.html", encoding="utf-8") as after_fp:
        ask_after_html = after_fp.read()

    assert trademarkify_page_html(ask_before_html) == ask_after_html
