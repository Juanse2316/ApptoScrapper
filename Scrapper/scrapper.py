import requests
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup 
import pandas as pd






class MercadoLibreScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def _make_request(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Error en la solicitud HTTP: {e}")
            return None    

    def _get_total_pages(self, query):
        try:
            url = f"{self.base_url}{query.replace(' ', '-')}_Desde_451_NoIndex_True"
            soup = self._make_request(url)
            
            pagination_buttons = soup.find_all("button", class_="andes-pagination__link")
            if pagination_buttons:
                last_page_button = pagination_buttons[-1]
                page_count_text = last_page_button.text
                return int(page_count_text)
        except:
            url = f"{self.base_url}{query.replace(' ', '-')}"
            soup = self._make_request(url)
            pagination_list = soup.find('ul', class_="andes-pagination ui-search-andes-pagination andes-pagination--large")
            if pagination_list:
                pages = pagination_list.find_all('button',class_="andes-pagination__link")
                page = pages[-1]
                page_count = page.text
                return int(page_count)
            
            



    def search(self, query: str, update_progress) -> list:
        url = f"{self.base_url}{query.replace(' ', '-')}"
        products = []
        current_page = 1

        soup = self._make_request(url)
        if not soup:
            return products
    
        total_pages = self._get_total_pages( query) 
        extraction_date = datetime.now().strftime("%Y-%m-%d %H")  

        while url:
            update_progress(current_page / total_pages)
            products.extend(self._parse_results(soup, current_page, extraction_date))
            current_page += 1

            
            url = self._get_next_page(soup)
            soup = self._make_request(url) if url else None
    
        return products
    
    
    def _parse_results(self, soup: BeautifulSoup, current_page: int, extraction_date: datetime) -> list:
        products = []
        for item in soup.find_all("li", class_="ui-search-layout__item"):
            try:
                title_element = item.find("h2", class_="ui-search-item__title")
                price_element = item.find("span", class_="andes-money-amount__fraction")
                rating_element = item.find("span", class_="ui-search-reviews__rating-number")
                rating_amount_element = rating_element and item.find("span", class_="ui-search-reviews__amount")
                discount_tag = item.find("span", class_="ui-search-price__discount")
                free_shipping_tag = item.find("p", class_="ui-search-item__shipping ui-search-item__shipping--free")
                variant_element = item.find("span", class_="ui-search-item__group__element ui-search-item__variations-text")
                # Procesamiento de los campos extraídos
                title = title_element.text.strip() if title_element else None
                clean_price = int(price_element.text.strip().replace(',', '').replace('.', '').replace('$', '')) if price_element else 0
                clean_rating = rating_element.text.strip() if rating_element else 0
                clean_rating_amount = int(rating_amount_element.text.strip().replace('(','').replace(')','')) if rating_amount_element else 0
                has_discount = discount_tag is not None
                discount_value = int(discount_tag.text.strip().replace('%', '').replace(' ', '').replace('OFF', '')) if has_discount else 0
                has_free_shipping = free_shipping_tag is not None
                has_variants = variant_element is not None
                variant_count = int(re.search(r'\d+', variant_element.text).group()) if variant_element else 0

                products.append({
                    "Title": title,
                    "Price": clean_price,
                    "Rating": clean_rating,
                    "Rating Amount": clean_rating_amount,
                    "Has Discount": has_discount,
                    "Discount": discount_value,
                    "Has Free Shipping": has_free_shipping,
                    "Has Variants": has_variants,
                    "Variant Count": variant_count,
                    "Page":current_page,
                    "Extraction Date":extraction_date,
                })
            except (ValueError, AttributeError) as e:
                print(f"Error al procesar el artículo: {e}")
        return products

    def _get_next_page(self, soup):
        next_page = soup.find("a", class_="andes-pagination__link", title="Siguiente")
        
        return next_page.get('href') if next_page else None

    def save_to_csv(self, products, filename, on_success):
        folder_path = "./Scrapper_saved"
        os.makedirs(folder_path, exist_ok=True)  # Crea la carpeta si no existe

        full_path = os.path.join(folder_path, filename)

        df = pd.DataFrame(products)
        

        try:
            df.to_csv(full_path, index=False)
            on_success(True)
            
        except Exception as e:
            print(f"Error saving file: {e}")