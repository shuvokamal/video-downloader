from video_downloader.utils.helpers import detect_platform


def test_detect_youtube():
    assert detect_platform("https://www.youtube.com/watch?v=abc") == "youtube"
    assert detect_platform("https://youtu.be/abc") == "youtube"


def test_detect_facebook():
    assert detect_platform("https://www.facebook.com/watch?v=123") == "facebook"
    assert detect_platform("https://fb.watch/abc") == "facebook"


def test_detect_twitter():
    assert detect_platform("https://twitter.com/user/status/123") == "twitter"
    assert detect_platform("https://x.com/user/status/123") == "twitter"


def test_detect_unknown():
    assert detect_platform("https://vimeo.com/abc") == "unknown"
