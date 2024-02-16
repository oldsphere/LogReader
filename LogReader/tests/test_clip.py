from LogReader.content import clip

def test_clip():

    content = (
        "This is part of the file\n"
        "-- 08:10 --\n"
        "Log entry number 1\n"
        "It has much more information\n"
        "\n"
        "\n"
        "-- 10:45 --\n"
        "Next entry on the log\n"
        "-- 11:35 --\n"
        "Last Entry on the log\n"
    )

    clip_pattern = r"^--\s*(?P<time>\d\d:\d\d)\s*--$"
    list_clips = clip(clip_pattern, content)

    assert len(list_clips) == 3
    assert list_clips[1] == "Next entry on the log\n"
