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

   
    def load_csv(self, file_path):
        try:
            self.df = pd.read_csv(file_path)
        except Exception:
            self.create_banner_error(True)
        return self.df
    
    def create_graphic_page_vs_price(sef, df):
        if df is not None:
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.scatter(df['Page'], df['Price'])
            ax.set_title('Relación entre Precio y Página')
            ax.set_xlabel('Página')
            ax.set_ylabel('Precio')
            ax.grid(True)
            return MatplotlibChart(fig)
        else:
            return Text("No data available to display")
        
    def visualize_data(self, file_path):
        df = self.load_csv(file_path)
        graphic = self.create_graphic_page_vs_price(df)
        self.controls.clear()
        self.controls.append(graphic)
        self.update()


    def build(self):
        self.app_data_analysis_instance()

        return Column(
            expand= True,
            controls= [],
        )