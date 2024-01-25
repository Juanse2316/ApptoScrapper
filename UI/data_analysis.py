import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn
from flet import *
from flet.matplotlib_chart import MatplotlibChart
from UI.controls import add_to_control_reference, return_control_reference


control_map = return_control_reference()

matplotlib.use("svg") 

class DataVisualizer(UserControl):
    def __init__(self):
        super().__init__()
        
    def app_data_analysis_instance(self):
        """
        This fuction sets the class instance as a key:value 
        pair in the global dicth
        """
        
        add_to_control_reference("AppHeader", self)

    def content_componet(self, content, expand):
        return Container(
            expand= expand,
            border=border.all(1, "#ebebeb"),
            border_radius=8,
            padding=8,
            content= content
        )
        

    def text_component(self, text:str, width: int):
        return Container(
        width=width,
        bgcolor="#ebebeb",
        border_radius=6,
        padding=8,
        # margin=5,
        content=Column(
            controls=[
                Text(value=text,color="black", weight="bold"),
                ]
            )
        )
   
    def load_csv(self, file_path: str) -> pd.DataFrame:
        try:
            self.df = pd.read_csv(file_path)
        except Exception:
            self.create_banner_error(True)
        return self.df
    
    def create_graphic_page_vs_price(sef, df: pd.DataFrame):
        if df is not None:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.scatter(df['Page'], df['Price'])
            ax.set_title('Relación entre Precio y Página')
            ax.set_xlabel('Página')
            ax.set_ylabel('Precio')
            ax.grid(True)
            graphic= MatplotlibChart(fig)
            return Container(expand=True, 
                             content=graphic, 
                             border_radius=6,
                             border=border.all(1, "#ebebeb"),
                             )
        else:
            return Text("No data available to display")
        
    def create_price_analysis(self, df: pd.DataFrame):
        if df is not None:
            minimum_price = round(df['Price'].min(), 2)
            maximum_price = round(df['Price'].max(), 2)
            average_price = round(df['Price'].mean(), 2)

            stat_width = 200

            stats = [

                Row(controls=[self.text_component(f"Minimum Price: {minimum_price}", stat_width)]),
                Row(controls=[self.text_component(f"Maximum Price: {maximum_price}", stat_width)]),
                Row(controls=[self.text_component(f"Average Price: {average_price}", stat_width)]),
            ]
            stats_column= Column(expand=True, controls=stats)
            
            con= self.content_componet(stats_column, None)

            
            return con
        else:
            return Text("No data available to display")
        
        
    def visualize_data(self, file_path):
        df = self.load_csv(file_path)

        
        graphic = self.create_graphic_page_vs_price(df)
        price_analysis = self.create_price_analysis(df)

        
        row = Row()
        row.controls.append(price_analysis)
        row.controls.append(graphic)

        
        self.main_column.controls.append(row)

        self.update()

    def build(self):
        self.app_data_analysis_instance()
        self.main_column = Column(expand=True) 
        return Container(
            expand= True,
            border=border.all(1, "#ebebeb"),
            border_radius=8,
            padding=8, 
            content= self.main_column
        )