from flet import *
from threading import Timer
from UI.controls import add_to_control_reference, return_control_reference

control_map = return_control_reference()


class AppBanner(UserControl):
    def __init__(self):
        super().__init__()
        self.timer = 5
        self.current_timer = None
        self.success_banner = self.create_success_banner_saved()
        self.error_banner = self.create_error_banner_saved()
        self.warning = self.create_warning_banner_textfield()
        self.analysis_banner = self.create_analysis_banner()
        self.generic_erro_banner = self.create_generic_erro_banner()
        

    def app_banner_instance(self):
        """
        This fuction sets the class instance as a key:value 
        pair in the global dicth
        """
        
        add_to_control_reference("AppBanner", self)
    
    def create_success_banner_saved(self,):
        banner = Banner(
            bgcolor=colors.GREEN_100,
            leading=Icon(icons.CHECK_CIRCLE, color=colors.GREEN, size=40),
            content=Text(
                "Your file has been saved successfully in the directory Scrapper_saved",
                color= "#21130d"
                ),
            actions=[
                TextButton("Close", on_click= self.close_banner)
            ],
        )
        return banner


    def create_error_banner_saved(self,):
        banner= Banner(
            bgcolor=colors.RED_100,
            leading=Icon(icons.ERROR_OUTLINE, color=colors.RED, size=40),
            content=Text(
                "Oops, there were some errors while trying to save the file."
                         ),
            actions=[
                TextButton("Close", on_click= self.close_banner)
            ],
        )

        return banner
    
    def create_warning_banner_textfield(self):
        return Banner(
            bgcolor=colors.YELLOW_100,
            leading=Icon(icons.WARNING, color=colors.AMBER, size=40),
            content=Text(
                "Please enter a search query before searching.",
                color="#21130d"
            ),
            actions=[
                TextButton("Close", on_click=self.close_banner)
            ],
        )
    
    def create_analysis_banner(self):
        banner = Banner(
            bgcolor=colors.GREEN_100,
            leading=Icon(icons.CHECK_CIRCLE, color=colors.GREEN, size=40),
            content=Text(
                "Complete data analysis: Your information is waiting for you See the Data Analysis tab",
                color="#21130d"
            ),
            actions=[
                TextButton("Close", on_click=self.close_banner)
            ],
        )
        
        

        return banner
    
    def create_generic_erro_banner(self):
        banner = Banner(
            bgcolor=colors.RED_100,
            leading=Icon(icons.ERROR_OUTLINE, color=colors.RED, size=40),
            content=Text(
                "Oops, something went wrong"
                         ),
            actions=[
                TextButton("Close", on_click= self.close_banner)
            ],
        )
        return banner

    def show_warning_banner(self, show: bool):
        self.warning.open = show
        self.update()
    
    def show_success_banner(self, show: bool):
        self.success_banner.open = show
        self.update()

    def show_error_banner(self, show: bool):
        self.error_banner.open = show
        self.update()

    def show_analysis_banner(self, show: bool):
        self.analysis_banner.open = show
        self.update()

    def show_generic_erro_banner(self, show:bool):
        self.generic_erro_banner.open = show
        self.update()

    def close_banner(self, e):
        for banner in [self.success_banner, self.error_banner, self.warning, self.analysis_banner, self.generic_erro_banner]:
            banner.open = False
        self.update()



    def build(self):
        self.app_banner_instance()
        return Container(
            content=Row(
                controls=[
                    self.success_banner,
                    self.error_banner,
                    self.warning,
                    self.analysis_banner
                ]
            )
        )