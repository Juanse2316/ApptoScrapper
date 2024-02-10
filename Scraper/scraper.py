import requests
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup 
import pandas as pd



class ScraperBase:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'https://www.amazon.com',
        }

    def _make_request(self, url):
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Error en la solicitud HTTP: {e}")
            return None

    def save_to_csv(self, products, filename, on_success, on_error):
        folder_name = type(self).__name__
        folder_path = f"./Scraper_saved/{folder_name}"
        os.makedirs(folder_path, exist_ok=True)

        full_path = os.path.join(folder_path, filename)

        
        try:
            if not products:
                raise ValueError("The product list is empty, the CSV file will not be created.")
            
            df = pd.DataFrame(products)
            df.to_csv(full_path, index=False)
            on_success(True, f"Archivo guardado en {full_path}")  
        except Exception as e:
            print(f"Error saving file: {e}")
            on_error(True, e)


class MercadoLibre(ScraperBase):
    def __init__(self, base_url):
        super().__init__(base_url)


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
    
        total_pages = self._get_total_pages(query) 
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
    
class Amazon(ScraperBase):
    def __init__(self, base_url):
        super().__init__(base_url)

    def _get_total_pages(self, soup:BeautifulSoup):

        try:
            page_counter = soup.find("span", class_="s-pagination-item s-pagination-disabled")
            
            return int(page_counter.text)
        except:
            return 1



    def search(self, query: str, update_progress) -> list:
        url = f"{self.base_url}{query.replace(' ', '+')}&__mk_es_US=ÅMÅŽÕÑ&ref=nb_sb_noss"
        products = []
        current_page = 1

        soup = self._make_request(url)
        if not soup:
            return products
        
        total_pages = self._get_total_pages(soup) 
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
        for item in soup.find_all("div", class_="sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"):
            try:
                title_element = item.find("span", class_="a-size-medium a-color-base a-text-normal")
                price_element = item.find("span", class_="a-price-whole")
                # rating_element = item.find("span", class_="a-icon-alt")
                # rating_amount_element = item.find("span", class_="a-size-base s-underline-text")
                # discount_tag = item.find("span", class_="a-size-base s-highlighted-text-padding aok-inline-block s-coupon-highlight-color")
                
                # Procesamiento de los campos extraídos
                
                title = title_element.text.strip() if title_element else None
                clean_price = int(price_element.text.strip().replace(',', '').replace('.', '').replace('$', '')) if price_element else 0

                products.append({
                    "Title": title,
                    "Price": clean_price,
                    "Page":current_page,
                    "Extraction Date":extraction_date,
                })


            except (ValueError, AttributeError) as e:
                print(f"Error al procesar el artículo: {e}")    
        return products


    def _get_next_page(self, soup):
        try:
            next_page_element = soup.find("a", class_="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator")
            if next_page_element:
                next_page_url = next_page_element.get('href')
                if next_page_url.startswith(('http:', 'https:')):
                    return next_page_url
                else:
                    base_url = self.base_url
                    next_page_url = f"{base_url}{next_page_url}"
                    return next_page_url
            else:
                return None
        except Exception as e:
            print(f"Error constructing the URL of the following page:{e}")
            return None
        
# amazon = Amazon("https://www.amazon.com/s?k=")
# products = amazon.search("mouse gamer inalambrico", lambda x: print(x))
# query = "mouse gamer inalambrico"
# print(f"{query}")
# print(f"{len(products)} productos encontrados")
# file_name = f"mercadolibre_products_{query}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.csv"
# print(f"{file_name}")