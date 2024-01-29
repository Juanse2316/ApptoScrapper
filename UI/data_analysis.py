import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
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

    def card_stats(self, expand:int, content, color:str="white")->Container:
        return Container(
            expand= expand,
            height=175,
            border=border.all(2, color),
            border_radius=8,
            padding=8,
            content= content
        )
        
   
    def load_csv(self, file_path: str) -> pd.DataFrame:
        try:
            self.df = pd.read_csv(file_path)
        except Exception:
            self.create_banner_error(True)
        return self.df
    
    def create_graphic_page_vs_price(sef, df: pd.DataFrame):
        if df is not None:
            sns.set(style="darkgrid")

            precios_por_pagina = df.groupby('Page')['Price'].mean()

            plt.figure(figsize=(10, 5))

            sns.lineplot(x=precios_por_pagina.index, y=precios_por_pagina.values)

            plt.title('Precio Promedio por Página', color='white')
            plt.xlabel('Página', color='white')
            plt.ylabel('Precio Promedio', color='white')
            
            fig = plt.gcf()

            fig.set_facecolor('#121212')
            ax = plt.gca()
            ax.set_facecolor('#1e1e1e')

            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    
            graphic = MatplotlibChart(fig)
            return Container(expand=True, 
                             content=graphic, 
                             border_radius=6,
                             )
        else:
            return Text("No data available to display")
        
    def create_price_analysis(self, df: pd.DataFrame):
        if df is not None:
            minimum_price_product = df.loc[df['Price'].idxmin()]
            maximum_price_product = df.loc[df['Price'].idxmax()]
            average_price = round(df['Price'].mean(), 2)

            

            

            minimum_price_list = [
                Row(controls=[
                    Text(value= f"Minimum Price: {minimum_price_product['Price']}", 
                         color='#00ff7f',
                         weight="bold", 
                         size=20 
                         ),
                    Icon(name=icons.TRENDING_DOWN, color='#00ff7f') ],alignment=alignment.top_center),
                    ResponsiveRow(controls=[Text(value= f"Product Title: {minimum_price_product['Title']}",color='white', size= 16 )],)
                    ]
            
            maximum_price_list = [
                Row(controls=[
                    Text(value= f"Maximum Price: {maximum_price_product['Price']}",
                         color="#DC143C",
                         weight="bold", 
                         size=20),
                    Icon(name=icons.TRENDING_UP, color="#DC143C")]),
                    ResponsiveRow(controls=[Text(value= f"Product Title: {maximum_price_product['Title']}",color='white', size= 16 )],)
                    ]
            
            average_list = [
                Row(controls=[
                    Text(value=f"Average Price: {average_price}", color="white", weight="bold", size=20, text_align=TextAlign.CENTER),
                    Icon(name=icons.ATTACH_MONEY, color='green')
                ], alignment=alignment.center)]

            minimum_price = Column(expand=True, controls=minimum_price_list)
            maximum_price = Column(expand=True, controls=maximum_price_list)
            average = Column(expand=True, controls=average_list, alignment=alignment.top_center) 

            con1 = self.card_stats(expand=1,content=minimum_price, color= "#00ff7f")
            con2 = self.card_stats(expand=1,content=maximum_price, color='#DC143C')
            con3 = self.card_stats(expand=1,content=average)
            
            row = Row(expand=True,controls=[con1,con2,con3])

            
            return row
        else:
            return Text("No data available to display")
        
        
    def visualize_data(self, file_path):
        self.main_column.controls.clear()

        df = self.load_csv(file_path)

        
        graphic_container = self.create_graphic_page_vs_price(df)
        price_analysis_container = self.create_price_analysis(df)

        
        
        
        row1 = Row(controls=[price_analysis_container,])
        row2 = Row(controls=[ graphic_container,])

        self.main_column.controls.append(row1)
        self.main_column.controls.append(row2)
        

        self.update()

    def build(self):
        self.app_data_analysis_instance()
        self.main_column = Column(expand=True,alignment=alignment.center ) 
        return Container(
            expand=True,
            border=border.all(1, "#ebebeb"),
            border_radius=8,
            padding=8, 
            content= self.main_column
        )