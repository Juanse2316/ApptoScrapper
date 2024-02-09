from Scrapper.scrapper import MercadoLibre, Amazon
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
        self.app_dropdown =self.app_header_dropdown()        
        self.search_bar = self.app_header_search()
        self.search_button = self.app_header_button()
        



    def app_header_instance(self):
        """
        This fuction sets the class instance as a key:value 
        pair in the global dicth
        """
        
        add_to_control_reference("AppHeader", self)
        
    def app_header_dropdown(self):
        return Container(
            padding= 10,
            content= Dropdown(
            hint_text="Select a page to search",
            content_padding= 8,
            focused_border_width=colors.BLUE_200,
            options=[
                dropdown.Option("MercadoLibre"),
                dropdown.Option("Amazon"),
            ],
        )
        )

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
                   Icon(name=icons.SEARCH_ROUNDED, size=20, opacity=0.85, color="black"),
                   TextField(
                       border_color="transparent",
                       expand = True,
                       height=30,
                       text_size=19,
                       content_padding=0,
                       cursor_color="black",
                       cursor_width=1,
                       hint_text="Search a Product",
                       hint_style=TextStyle(color= "black", font_family="Roboto",  ),
                       text_style=TextStyle(color= "black",),
                       on_change= lambda e: self.obtain_data(e),
                       on_submit=lambda e: self.search_products(e) if self.query.strip() else None,
                   )
               ]
           ),
        )
    
    def obtain_data(self, e):
        self.query = e.data 
        self.search_button.disabled = not bool(self.query.strip())
        self.update()

    def create_banner_success(self, show: bool, message: str):
        
        self.banner = self.app_banner.create_success_banner_saved()
        self.app_banner.show_success_banner(show, message)
        self.update()

    def create_banner_error(self, show: bool, message: str):
        
        self.banner = self.app_banner.create_error_banner_saved()
        self.app_banner.show_error_banner(show, message)
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

        self.selected_scraper = self.app_dropdown.content.value
        if self.selected_scraper == "MercadoLibre":
            scraper = MercadoLibre("https://listado.mercadolibre.com.co/")
        elif self.selected_scraper == "Amazon":
            scraper = Amazon("https://www.amazon.com/s?k=")

        def update_progress(value):
            self.progress_bar.value = value
            self.update()
        
        try:

            products = scraper.search(self.query, update_progress)
            
            file_name = f"mercadolibre_products_{self.query}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.csv"
            print(f"{file_name}")
            scraper.save_to_csv(products, file_name, self.create_banner_success, self.create_banner_error)
            
            
        except Exception as e:
            print(f"{e}")
            self.create_banner_error(True, e)
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
            height= 100,
            width= 200,
            padding=10,
            content= ElevatedButton(
                text="Search",
                on_click= self.search_products,
                style= ButtonStyle(
                    shape= StadiumBorder(),
                    color={
                        MaterialState.DEFAULT: colors.BLACK,
                        MaterialState.DISABLED: colors.WHITE,
                    },
                    bgcolor={
                        MaterialState.DEFAULT: "#E2EAFD",
                        MaterialState.DISABLED: colors.GREY,
                    },
                    side={
                        MaterialState.DEFAULT: BorderSide(1, "wite"),
                        MaterialState.HOVERED: BorderSide(3, "#4140C2"),
                    },
                    elevation={"pressed": 0, "": 1},

                    
                )
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
                    self.app_banner,
                    self.app_dropdown,
                    self.search_bar,
                    self.progress_bar,
                    self.search_button,
                ],
            )

        )
        