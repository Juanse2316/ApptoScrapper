from flet import *
from UI.controls import add_to_control_reference, return_control_reference
import os

class AppTable(UserControl):
    def __init__(self):
        super().__init__()
        

    def app_Table_instance(self):
        """
        This fuction sets the class instance as a key:value 
        pair in the global dicth
        """
        
        add_to_control_reference("AppTable", self)

    def search_csv_file(self):
        try:

            csv_files = [(file, os.path.getmtime(os.path.join("./Scrapper_saved", file))) 
                            for file in os.listdir("./Scrapper_saved") 
                            if file.endswith('.csv')]

            csv_files.sort(key=lambda x: x[1], reverse=True)


            last_files = [file[0] for file in csv_files[:10]]

            return last_files

        except Exception as e:
            print(f"Error  CSV: {e}")
            return None
        
    def show_csv_file (self):
        files= self.search_csv_file()
        row_list= []


        header_text_left = Text("Saved Files", color=colors.WHITE, size=24, weight="bold")
        header_container_left = Container(
            content=header_text_left,
            expand=1  
        )

        
        header_text_right = Text("Actions", color=colors.WHITE, size=24, weight="bold", text_align="right")
        header_container_right = Container(
            content=header_text_right,
            expand=1  
        )
        header_row = Row(
            controls=[header_container_left, header_container_right],
            alignment="space_between",  
            vertical_alignment="center"
        )
        row_list.append(header_row)

        if files is not None:
            for file in files:

                file_icon= Icon(
                    icons.INSERT_DRIVE_FILE,
                    size=24,
                    color= colors.BLUE
                )

                file_name= Text(
                    file,
                    color=colors.WHITE,
                    size=16, 
                    weight="bold",
                    )
                
                container = Container(
                    expand=True,
                    content=file_name,
                    border_radius=6,
                    padding=8,
                    bgcolor="#29295C",
                )

                row = Row(
                    controls=[file_icon, container],
                    alignment="left",
                    vertical_alignment="center",
                )                


                row_list.append(row)

        return row_list





    def build(self):
        self.app_Table_instance()
        rows = self.show_csv_file()

        return Container(
            expand= True,
            border=border.all(1, "#ebebeb"),
            border_radius=8,
            padding=15, 
            content= Column(
                expand=True,
                controls= rows
            ) 
        )