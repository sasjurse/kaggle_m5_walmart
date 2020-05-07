import twitter

from src.twitter_collector import clean_text, search_api


def test_clean_text_removes_escape_chars():
    case1 = 'abc"#¤%.,;()'
    assert clean_text(case1) == 'abc'


def test_search_api_returns_results():
    search_result = search_api(query='Covid', location='Manhattan', count=5)
    assert isinstance(search_result, list), 'Expected list as result'
    assert len(search_result) > 0, 'Expected non-empty list'
    assert isinstance(search_result[0], twitter.models.Status), \
        'expected items in list to be of type twitter.models.Status'
