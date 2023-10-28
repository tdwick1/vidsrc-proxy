import re,requests


def match_regex(pattern, text):
    """
    Returns a regex match if there is one
    """
    matches = re.findall(pattern, text)
    value = None
    if matches:
        value = matches[0]
    return value
def vidsrc(external_id):

    base_helper_url = "https://9anime.eltik.net"


    data_id_response = requests.get(f"https://vidsrc.to/embed/movie/{external_id}", timeout=10)
    pattern = r'.*data-id="([^"]*)".*'
    data_id = match_regex(pattern, data_id_response.text)

    if not data_id:
        return


    vidplay_id_response = requests.get(f"https://vidsrc.to/ajax/embed/episode/{data_id}/sources", timeout=10)
    pattern = r'\"id\":\"([^\"]*)\".*\"Vidplay'
    vidplay_id = match_regex(pattern, vidplay_id_response.text)

    if not vidplay_id:
        return

    encrypted_provider_url_response = requests.get(f"https://vidsrc.to/ajax/embed/source/{vidplay_id}", timeout=10)
    pattern = r'\"url\":\"([^\"]*)\"'
    encrypted_provider_url = match_regex(pattern, encrypted_provider_url_response.text)

    if not encrypted_provider_url:
        return

    provider_embed_response = requests.get(f"{base_helper_url}/fmovies-decrypt?query={encrypted_provider_url}&apikey=jerry", timeout=10)
    pattern = r'\"url\":\"([^\"]*)\"'
    provider_embed = match_regex(pattern, provider_embed_response.text)

    if not provider_embed:
        return

    pattern = r'.*/e/([^\?]*)(\?.*)'
    matches = re.search(pattern, provider_embed)
    provider_query = None
    params = None
    if matches.lastindex == 2:
        provider_query = matches.group(1)
        params = matches.group(2)

    if not provider_query or not params:
        return


    futoken = requests.get("https://vidplay.site/futoken", timeout=10).text

    if not futoken:
        return


    raw_url_response = requests.post(f"{base_helper_url}/rawvizcloud?query={provider_query}&apikey=jerry", data={"query": provider_query, "futoken": futoken}, timeout=10)
    pattern = r'\"rawURL\":\"([^\"]*)\"'
    raw_url = match_regex(pattern, raw_url_response.text)

    if not raw_url:
        return


    video_link_response = requests.get(f"{raw_url}{params}", headers={"Referer": provider_embed}, timeout=10)
    cd_link = re.sub(r'\\/', '/', video_link_response.text)
    pattern = r'\"file\":\"([^\"]*)\"'
    matches = re.search(pattern, cd_link)
    video_link = None
    if matches:
        video_link = matches.group(1)

    if not video_link:
        return

    index = cd_link.find('"file":"')
    if index == -1:
        return
    first_file_url = cd_link[index + len('"file":"'):]


    index = first_file_url.find('"')
    if index == -1:
        return
    first_file_url = first_file_url[:index]


    return first_file_url
