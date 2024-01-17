from flet import *
from UI.controls import add_to_control_reference, return_control_reference
import os

class AppTable(UserControl):
    def __init__(self):
        super().__init__()
        self.main_column = Column(expand=True,)
        

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


            last_files = [file[0] for file in csv_files[:100]]

            return last_files

        except Exception as e:
            print(f"Error  CSV: {e}")
            return None
        
    def show_csv_file (self):
        files= self.search_csv_file()
        row_list= []


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
        else:
            no_files_message = Text(
              "No saved information available yet",
              color=colors.WHITE,
              size=18,
              weight="bold",  
            )
            container = Row(
                controls=[no_files_message],
                alignment="center",
                vertical_alignment="center",
            )
            row_list.append(container)


        return row_list


    def update_csv_files(self):
        rows = self.show_csv_file()
        self.main_column.controls.clear()
        self.main_column.controls.extend(rows)
        self.update()


    def build(self):
        self.app_Table_instance()
        self.main_column.controls.extend(self.show_csv_file())

        return Container(
            expand= True,
            border=border.all(1, "#ebebeb"),
            border_radius=8,
            padding=15, 
            content= self.main_column 
        )