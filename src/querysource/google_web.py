from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class GoogleWeb:
    def __init__(self):
        super().__init__()

        self.chrome_options = Options()
        self.chrome_options.add_argument("--window-size=1024x768")
        self.chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=self.chrome_options)

    def search(self, query: str) -> str:

        # Search for query
        query = query.replace(" ", "+")

        self.driver.get("http://www.google.com/search?q=" + query)

        # Get text from answer box
        try:
            answer = self.driver.execute_script(
                "return document.querySelector(\"[data-attrid='wa:/description']\").textContent"
            )
        except:
            answer = None

        # Take first search result if no answer box
        if not answer:
            try:
                answer = self.driver.execute_script(
                    'return document.getElementsByClassName("st")[0].textContent'
                )
            except:
                answer = None

        return answer
