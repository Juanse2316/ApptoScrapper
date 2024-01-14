import requests
import os
from bs4 import BeautifulSoup 
import pandas as pd





class MercadoLibreScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def _get_total_pages(self, soup):
        try:
            page_count_text = soup.find("li", class_="andes-pagination__page-count").text
            
            return int(page_count_text.split()[-1])
        except Exception as e:
            print(f"Error extracting total pages: {e}")
            return 1  



    def search(self, query: str, update_progress) -> list:
        url = f"{self.base_url}{query.replace(' ', '-')}"
        products = []
        current_page = 1
    
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            total_pages = self._get_total_pages(soup)  
    
            while url:
                update_progress(current_page / total_pages)
                current_page += 1
    
                products.extend(self._parse_results(soup))
                url = self._get_next_page(soup)
    
                if url:
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Error durante la búsqueda: {e}")
    
        return products
    
    
    def _parse_results(self, soup: BeautifulSoup) -> list:
        products = []
        for item in soup.find_all("li", class_="ui-search-layout__item"):
            title = item.find("h2", class_="ui-search-item__title")
            price = item.find("span", class_="andes-money-amount__fraction")
            rating = item.find("span", class_="ui-search-reviews__rating-number")
            rating = item.find("span", class_="ui-search-reviews__rating-number")
            discount_tag = item.find("span", class_="ui-search-price__discount")

        
            try:
                clean_price = price.text.strip().replace(',', '').replace('.', '').replace('$', '')
                clean_rating = None if rating is None else rating.text.strip()
                has_discount = discount_tag is not None
                discount_value = None
                if has_discount:
                    discount_value = int(discount_tag.text.strip().replace('%', '').replace(' ', '').replace('OFF', ''))

                products.append({
                    "Title": title.text.strip(),
                    "Price": int(clean_price),
                    "Rating": clean_rating,
                    "Has_discount": has_discount,  
                    "Discount": discount_value,  
                    })
            except ValueError:
                
                print(f"Error al convertir el precio: {price.text}")
        return products

    def _get_next_page(self, soup):
        next_page = soup.find("a", class_="andes-pagination__link ui-search-link", attrs={"title": "Siguiente"})
        if next_page:
            return next_page.get('href')
        return None

    def save_to_csv(self, products, filename, on_success):
        folder_path = "./Scrapper_saved"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        full_path = os.path.join(folder_path, filename)         

        df = pd.DataFrame(products)
        

        try:
            df.to_csv(full_path, index=False)
            on_success(True)
            
        except Exception as e:
            print(f"Error saving file: {e}")



    

        # print(f"Data saved to '{full_path}'")

