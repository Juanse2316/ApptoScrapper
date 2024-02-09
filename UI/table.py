from flet import *
from UI.controls import add_to_control_reference, return_control_reference
import os

control_map = return_control_reference()

class AppTable(UserControl):
    def __init__(self, data_visualizer):
        super().__init__()
        self.main_column = Column(expand=True,)
        self.data_visualizer = data_visualizer

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
                file_with_path = "./Scrapper_saved/" + file
                

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
                    padding=10,
                    bgcolor="#29295C",
                    )
                is_current_file = self.data_visualizer.currently_displayed_file == file_with_path
                tooltip_text = "Create a report on Data Analysis" if not is_current_file else "Data Analysis already generated for this file"
                data_button = IconButton(
                        icon=icons.QUERY_STATS,
                        icon_color=colors.GREY if is_current_file else colors.GREEN,
                        icon_size= 30,
                        tooltip=tooltip_text,
                        on_click=lambda e, file=file: self.on_data_button_click(e, file),
                        disabled=is_current_file,
                    )
                

                row = Row(
                    controls=[file_icon, container, data_button],
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


    def on_data_button_click(self, e, file):
        app_banner = control_map.get("AppBanner")

        try:
            file_path = "./Scrapper_saved/" + file  
            self.data_visualizer.visualize_data(file_path) 
            if app_banner:
                app_banner.show_analysis_banner(True)
            self.update_csv_files()
        except:
            app_banner.show_generic_erro_bannerr(True)

    def update_csv_files(self):
        rows = self.show_csv_file()
        self.main_column.controls.clear()
        self.main_column.controls.extend(rows)
        self.update()

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