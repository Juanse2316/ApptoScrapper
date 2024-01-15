import flet 
from flet import *
from UI.header import AppHeader
from UI.banner import AppBanner
from UI.table import AppTable



def main(page: Page):
    page.title = "CSV Scrapper"
    page.bgcolor = "#1A1A40"
    page.padding = 20

    search_proccess = Tab(
        text="Search Proccess",
        content= Column(
            expand= True,
            controls=[
                AppHeader(),
                AppBanner(),
                Divider(height=2, color= "transparent"),
                AppTable(),
            ]
        )
    )

    data_analysis = Tab(
        text= "Data Analysis",
        content= Column(
            expand=True,
            controls=[Container(
                expand=True,
                content=Text("Coming Soon..."),
                alignment=alignment.center,
                bgcolor=colors.WHITE
            ),
            ]
        )
    )

    tabs = Tabs(
        tabs=[
            search_proccess,
            data_analysis,
        ],
        expand=1,
        unselected_label_color=colors.WHITE,
        divider_color= "transparent",
        indicator_padding= 4,
    )
    
    page.add(tabs)
    page.update()
    




if __name__ == '__main__':
    flet.app(target=main)
