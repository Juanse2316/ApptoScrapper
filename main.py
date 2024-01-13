import flet 
from flet import *
from UI.header import AppHeader
from UI.banner import AppBanner



def main(page: Page):
    page.bgcolor = "#1A1A40"
    page.padding = 20
    page.add(
        Column(
            expand= True,
            controls=[
                AppHeader(),
                AppBanner(),
            ]
        )
    )
    page.update()
    pass




if __name__ == '__main__':
    flet.app(target=main)
