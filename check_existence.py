from bs4 import BeautifulSoup
import requests

headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

def exist(word):
    if word != "":
        word = word.lower().strip()
        url = 'https://www.dictionary.com/browse/' + word

        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")

        data = soup.find_all(class_="hp91nlVaykGzCu7JxmyY")
        for element in data:
            if "no results found" in element.text.lower():
                return False

        return True
