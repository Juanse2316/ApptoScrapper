import requests
from bs4 import BeautifulSoup 
import pandas as pd
from datetime import datetime


url = "https://listado.mercadolibre.com.co/"

class MercadoLibreScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def search(self, query: str) -> list:
        url = f"{self.base_url}{query.replace(' ', '-')}"
        products = []

        while url:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            products.extend(self._parse_results(soup))
            url = self._get_next_page(soup)

        return products

    def _parse_results(self, soup: BeautifulSoup) -> list:
        products = []
        for item in soup.find_all("li", class_="ui-search-layout__item"):
            title = item.find("h2", class_="ui-search-item__title")
            price = item.find("span", class_="andes-money-amount__fraction")
        
            try:
                clean_price = price.text.strip().replace(',', '').replace('.', '').replace('$', '')
                products.append({
                    "title": title.text.strip(),
                    "price": int(clean_price)
                    })
            except ValueError:
                # Manejo de situaciones donde el precio no se puede convertir
                print(f"Error al convertir el precio: {price.text}")
        return products

    def _get_next_page(self, soup):
        next_page = soup.find("a", class_="andes-pagination__link", attrs={"title": "Siguiente"})
        if next_page:
            return next_page.get('href')
        return None

    def save_to_csv(self, products, filename):
        df = pd.DataFrame(products)
        df.to_csv(filename, index=False)
        print(f"Data saved to '{filename}'")

scraper = MercadoLibreScraper(url)
products = scraper.search("ram ddr3 8gb")
scraper.save_to_csv(products, f"mercadolibre_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")