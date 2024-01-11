import flet 
from flet import *



def main(page: Page):
    page.bgcolor = "#1A1A40"
    page.padding = 20
    page.add(
        Column(
            expand= True,
            controls=[
                
            ]
        )
    )
    page.update()
    pass




if __name__ == '__main__':
    flet.app(target=main)
