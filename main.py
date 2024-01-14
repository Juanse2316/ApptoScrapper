import flet 
from flet import *
from UI.header import AppHeader
from UI.banner import AppBanner
from UI.table import AppTable



def main(page: Page):
    page.title = "CSV Scrapper"
    page.bgcolor = "#1A1A40"
    page.padding = 20
    page.add(
        Column(
            expand= True,
            controls=[
                AppHeader(),
                AppBanner(),
                Divider(height=2, color= "transparent"),
                AppTable(),
            ]
        )
    )
    page.update()
    pass




if __name__ == '__main__':
    flet.app(target=main)
