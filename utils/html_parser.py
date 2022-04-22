from bs4 import BeautifulSoup


def get_csrf_token(html):
    soup = BeautifulSoup(html, 'html.parser')
    csrf_tag = soup.find(attrs={"name": "_csrf"})
    if csrf_tag:
        return csrf_tag["content"]
    return ""
