from flet import *
from UI.controls import add_to_control_reference, return_control_reference

control_map = return_control_reference()


class AppBanner(UserControl):
    def __init__(self):
        super().__init__()
        self.success_banner = self.create_success_banner()
        self.error_banner = self.create_error_banner()

    def app_banner_instance(self):
        """
        This fuction sets the class instance as a key:value 
        pair in the global dicth
        """
        
        add_to_control_reference("AppBanner", self)
    
    def create_success_banner(self,):
        return Banner(
            bgcolor=colors.GREEN_100,
            leading=Icon(icons.CHECK_CIRCLE, color=colors.GREEN, size=40),
            content=Text(
                "Your file has been saved successfully in the directory Scraper_saved"
                ),
            actions=[
                TextButton("Close", on_click= self.close_banner)
            ],
        )


    def create_error_banner(self,):
        return Banner(
            bgcolor=colors.RED_100,
            leading=Icon(icons.ERROR_OUTLINE, color=colors.RED, size=40),
            content=Text(
                "Oops, there were some errors while trying to save the file."
                         ),
            actions=[
                TextButton("Close", on_click= self.close_banner)
            ],
        )
    
    def show_success_banner(self, show: bool):
        self.success_banner.open = show
        self.update()

    def show_error_banner(self, show: bool):
        self.error_banner.open = show
        self.update()
    

    def close_banner(self, e):
        self.success_banner.open = False
        self.error_banner.open = False
        self.update()

    def build(self):
        self.app_banner_instance()
        return Container(
            content=Row(
                controls=[
                    self.success_banner,
                    self.error_banner
                ]
            )
        )