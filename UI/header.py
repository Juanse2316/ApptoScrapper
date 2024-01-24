from Scrapper.scrapper import MercadoLibreScraper
from datetime import datetime
from flet import *
from UI.controls import add_to_control_reference, return_control_reference
from UI.banner import AppBanner


control_map = return_control_reference()

class AppHeader(UserControl):
    def __init__(self):
        super().__init__()
        self.query = ""
        self.app_banner = AppBanner()
        self.progress_bar = ProgressBar(visible=False, expand=True)
        self.searching = False
        self.search_bar = self.app_header_search()
        self.search_button = self.app_header_button()

    def app_header_instance(self):
        """
        This fuction sets the class instance as a key:value 
        pair in the global dicth
        """
        
        add_to_control_reference("AppHeader", self)
        
    def app_header_brand(self):
        return Container(padding=8,content= Text( "Market Miner", size= 20, color= "#ffffff", ))
    
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
                       expand = True,
                       height=30,
                       text_size=19,
                       content_padding=0,
                       cursor_color="black",
                       cursor_width=1,
                       hint_text="Search a Product",
                       on_change= lambda e: self.optain_data(e),
                       on_submit=lambda e: self.search_products(e) if self.query.strip() else None,
                   )
               ]
           ),
        )
    
    def optain_data(self, e):
        self.query = e.data 
        self.search_button.disabled = not bool(self.query.strip())
        self.update()

    def create_banner_success(self, show: bool):
        
        self.banner = self.app_banner.create_success_banner_saved()
        self.app_banner.show_success_banner(show)
        self.update()

    def create_banner_error(self, show: bool):
        
        self.banner = self.app_banner.create_error_banner_saved()
        self.app_banner.show_error_banner(show)
        self.update()

    def search_products(self, e):
        if not self.query.strip():
            app_banner = control_map.get("AppBanner")
            if app_banner:
                app_banner.show_warning_banner(True)
            self.update()
            return

        self.set_searching_state(True)
        self.show_progress_bar(True)
        scraper = MercadoLibreScraper("https://listado.mercadolibre.com.co/")

        def update_progress(value):
            self.progress_bar.value = value
            self.update()
        
        try:

            products = scraper.search(self.query, update_progress)
            scraper.save_to_csv(products, f"mercadolibre_products_{self.query}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.csv", self.create_banner_success)
            
        except Exception as e:
            print(f"{e}")
            self.create_banner_error(True)
        finally:
            self.show_progress_bar(False)
            app_table = return_control_reference().get("AppTable")
            if app_table:
                app_table.update_csv_files()
            self.update()

    def show_progress_bar(self, show: bool):
        self.progress_bar.visible = show
        self.search_bar.visible = not show
        self.search_button.visible = not show
        self.update()
    
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
    
    def set_searching_state(self, is_searching):
        self.searching = is_searching
        self.search_bar.visible = not is_searching
        self.search_button.visible = not is_searching
        self.update()

    def build(self):
        self.app_header_instance()
         
    

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
                    self.search_bar,
                    self.progress_bar,
                    self.search_button,
                    self.app_banner,
                ],
            )

        )
        