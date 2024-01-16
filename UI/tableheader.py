from flet import *
from UI.controls import add_to_control_reference, return_control_reference

class AppTableHeader(UserControl):
    def __init__(self):
        super().__init__()
        self.left = self.header_container_left()
        self.right = self.header_container_right()

    def app_Tableheader_instance(self):
        """
        This fuction sets the class instance as a key:value 
        pair in the global dicth
        """
        
        add_to_control_reference("AppTableHeader", self)

    def header_container_left(self):
        self.header_text_left = Text("Saved Files", color=colors.WHITE, size=24, weight="bold")
        
        
        return Container(
            content=self.header_text_left,
            expand=1  
        )

    def header_container_right(self):
        header_text_right = Text("Actions", color=colors.WHITE, size=24, weight="bold", text_align="right")
        
        
        return Container(
            content=header_text_right,
            expand=1  
        )
    
    def build(self):
        return Row(
            controls=[self.left, self.right],
            alignment="space_between",  
            vertical_alignment="center"
        )