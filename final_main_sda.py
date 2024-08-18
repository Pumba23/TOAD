# final_main_sda.py
from sda_process_load import SDAProcessLoad

class FinalMainSDA:
    def __init__(self, sda_type, start_year, end_year, selected_demand, selected_region, refapp):
        self.sda_type = sda_type
        self.start_year = start_year
        self.end_year = end_year
        self.selected_demand = selected_demand
        self.selected_region = selected_region
        self.refapp = refapp
        self.display_info()

    def display_info(self):
        print("Wir sind in Final Main")
        print(f"SDA Type: {self.sda_type}")
        print(f"Start Year: {self.start_year}")
        print(f"End Year: {self.end_year}")
        print(f"Selected Demand: {', '.join(self.selected_demand)}")
        print(f"Selected Region: {', '.join(self.selected_region)}")
        print(f"Reference Approach: {self.refapp}")

        self.app.show_sda_process_load_page(self.sda_type, self.start_year, self.end_year, self.selected_demand,
                                            self.selected_region, self.refapp)

