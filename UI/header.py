from Scrapper.scrapper import MercadoLibreScraper
from datetime import datetime
from flet import *
from UI.controls import add_to_control_reference, return_control_reference


control_map = return_control_reference()

class AppHeader(UserControl):
    def __init__(self):
        super().__init__()
        self.query = ""

    def app_heade_instance(self):
        """
        This fuction sets the class instance as a key:value 
        pair in the global dicth
        """
        
        add_to_control_reference("AppHeader", self)
        
    def app_header_brand(self):
        return Container(content= Text( "Market Miner", size= 20, color= "#ffffff"))
    
    def app_header_search(self):
        return Container(
           width= 600,
           bgcolor= "#eae9e9", 
           border_radius=6,
           padding=8,
           content=Row(
               spacing=10,
               vertical_alignment=CrossAxisAlignment.CENTER,
               controls=[
                   Icon(name=icons.SEARCH_ROUNDED, size=20, opacity=0.85),
                   TextField(
                       border_color="transparent",
                       height=30,
                       text_size=19,
                       content_padding=0,
                       cursor_color="black",
                       cursor_width=1,
                       hint_text="Search a Product",
                       on_change= lambda e: self.optain_data(e)
                   )
               ]
           ),
        )
    
    def optain_data(self, e):
        self.query = e.data 


    def search_products(self, e):
        scraper = MercadoLibreScraper("https://listado.mercadolibre.com.co/")
        products = scraper.search(self.query)
        scraper.save_to_csv(products, f"mercadolibre_products_{self.query}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    
    def app_header_button(self):
        return Container(
            height= 50,
            width= 200,
            padding=10,
            content= ElevatedButton(
                text= "Search",
                on_click= self.search_products
            )
        )

    def build(self):
        self.app_heade_instance()

        return Container(
            expand= True,
            height=60,
            bgcolor="#3D4F91",
            border_radius= border_radius.only(top_left=15, top_right=15),
            padding= padding.only(left=15, right=15),
            content=Row(
                expand=True,
                alignment= MainAxisAlignment.SPACE_BETWEEN,
                controls= [
                    self.app_header_brand(),
                    self.app_header_search(),
                    self.app_header_button(),
                ],
            )

        )
        