def create_download_link(song_uri, **params) -> str:
    """Creates the Spotify Code Download Link from the songs uri. 
    The download links always have the same prefix, then the details of
    the code is given and at the end the uri. Also every : must be replaced
    by %3A. 

    Args:
        song_uri (str): uri (Uniform Resource Identifier) identifies each track,
        album, artist or playlist on Spotify and can be received from the API.

    Returns:
        str: Download link which instantly triggers an download in a browser
        or using a get request (same think anyway).
    """
    img_f = params["image_format"]
    bg_c = params["background_color"]
    bar_c = params["bar_color"]
    img_s = params["image_size_in_px"]
    prefix = params["download_link_prefix"]

    download_link = f"{prefix}uri={img_f}%2F{bg_c}%2F{bar_c}%2F{img_s}%2F{song_uri.replace(':', '%3A')}"

    return download_link