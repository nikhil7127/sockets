from bs4 import BeautifulSoup
import requests


class Amazon():

    def __init__(self, link):
        self.link = link
        HEADERS = ({'User-Agent': 'Nikhil\'s_request'})
        response = requests.get(self.link, headers=HEADERS)
        self.soup = BeautifulSoup(response.text, "lxml")
        self.productName = self.soup.find("h1", attrs={"id": "title"}).text.strip()
        self.rating = self.soup.find("span", attrs={"id": "acrPopover"}).text.strip()

    def availabilityStatus(self):
        let = self.soup.select("#availability")[0].text.strip().lower()
        # print(let)
        if (let == "in stock."):
            return ["In Stock", True]
        if (let == "available from these sellers."):
            return ["availabile from some sellers", False]
        if ("on" in let):
            return [let.split("\n")[0], False]
        if ("only" in let):
            return [let, True]
        else:
            return ["Out Of Stock", False]

    def getPrice(self):
        if (self.availabilityStatus()[-1]):
            orginal = self.soup.find("span", attrs={"class": "priceBlockStrikePriceString"}).text.strip().replace(
                u"₹\xa0", "")
            try:
                offer = self.soup.select("#priceblock_ourprice")[0].text.strip().split(" ")[-1].replace(u"₹\xa0", "")
            except:
                offer = self.soup.select("#priceblock_dealprice")[0].text.strip().split(" ")[-1].replace(u"₹\xa0", "")
            return [orginal, offer,
                    round(100 - (float(offer.replace(",", "")) / float(orginal.replace(",", ""))) * 100)]
        else:
            print("OUT OF STOCK")
            return False

# Amazon("https://www.amazon.in/dp/B085J1J32G?pf_rd_r=PEE54ZZ3J43JWXB3XQZY&pf_rd_p=b2edca66-3363-4fbb-9de4-24447d59ce98").getPrice()

Amazon('https://www.amazon.in/Fujifilm-Instax-Mini-Cobalt-Blue/dp/B06WWL4JD8').getPrice()