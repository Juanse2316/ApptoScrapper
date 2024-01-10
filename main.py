import flet as ft
from scrapper import MercadoLibreScraper
from datetime import datetime


def main(page: ft.Page):
    def search_products(e):
        query = txt_search.value
        scraper = MercadoLibreScraper("https://listado.mercadolibre.com.co/")
        products = scraper.search(query)
        scraper.save_to_csv(products, f"mercadolibre_products_{query}.csv")
        txt_result.value = f"Resultados guardados en: mercadolibre_products_{query}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    # Creando los componentes de la UI
    txt_search = ft.TextField(hint_text="Escribe aquí el producto a buscar", expand=1)
    btn_search = ft.ElevatedButton(text="Buscar", on_click=search_products)
    txt_result = ft.TextField(label="Resultado", multiline=True, expand=1,)

    # Añadiendo los componentes a la página
    page.add(txt_search, btn_search, txt_result)

ft.app(target=main)
