import os
import tkinter as tk
from tkinter import ttk, filedialog
import shutil
import threading

class MetaShape_App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MetaShape Application")
        self.geometry("680x400")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.create_frames()

    def create_frames(self):
        self.project_frame = ttk.Frame(self)
        self.project_frame.grid(row=0, column=0, columnspan=2, pady=30, sticky="n")
        self.create_project_frame()

        self.input_frame = ttk.Frame(self)
        self.input_frame.grid(row=1, column=0, columnspan=5, pady=10, sticky="ew")
        self.create_input_frame()
        self.input_frame.grid(padx=10, pady=10)

        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=2, column=0, columnspan=5, pady=10, sticky="ew")
        self.create_button_frame()

        self.logger_frame = ttk.Frame(self)
        self.logger_frame.grid(row=3, column=0, columnspan=2, pady=30, sticky="ew")
        self.create_logger_frame()

    def create_project_frame(self):
        padding = 10
        font = ("Arial", 12)

        # folder label (project name)
        self.folder_label = tk.Label(self.project_frame, text="Project Name:", font=font)
        self.folder_label.grid(row=0, column=0, padx=padding, pady=padding)

        # folder entry (project names list)
        self.folder_var = tk.StringVar()
        self.folder_entry = ttk.Combobox(self.project_frame, textvariable=self.folder_var, values=self.get_existing_projects(), font=font)
        self.folder_entry.grid(row=0, column=1, padx=padding, pady=padding)

    def create_input_frame(self):
        padding = 10
        font = ("Arial", 12)

        # CSV
        self.csv_label = tk.Label(self.input_frame, text="CSV File:")
        self.csv_label.grid(row=0, column=0)
        self.csv_entry = tk.Entry(self.input_frame)
        self.csv_entry.grid(row=0, column=1)
        self.csv_button = tk.Button(self.input_frame, text="Browse", command=lambda: browse_file(self.csv_entry))
        self.csv_button.grid(row=0, column=2)

        # Add padding
        self.csv_label.grid(padx=(100, 0)) 
        self.csv_button.grid(padx=(5, 10)) 


        # image
        self.images_label = tk.Label(self.input_frame, text="Images Folder:")
        self.images_label.grid(row=0, column=4)
        self.images_entry = tk.Entry(self.input_frame)
        self.images_entry.grid(row=0, column=5)
        self.images_button = tk.Button(self.input_frame, text="Browse", command=lambda: browse_folder(self.images_entry))
        self.images_button.grid(row=0, column=6)

    def create_button_frame(self):
        padding = 10

        # submit
        self.submit_button = tk.Button(self.button_frame, text="Submit", command=self.submit_data)
        self.submit_button.grid(row=0, column=0, padx=padding)
        self.submit_button.grid(padx=(300, 10),pady=(10,10)) 

        # Run
        self.run_button = tk.Button(self.button_frame, text="  Run  ", command=self.run_process)
        self.run_button.grid(row=0, column=1, padx=padding)
        self.run_button.grid(padx=(10, 10)) 

        # # geotag
        # self.geotag_button = tk.Button(self.button_frame, text="Geotag", command=self.geotag_images)
        # self.geotag_button.grid(row=0, column=2, padx=padding)
        # self.geotag_button.grid(padx=(10, 0)) 

    def create_logger_frame(self):
        padding = 10

        # Text widget for logging
        self.log_text = tk.Text(self.logger_frame, height=5, width=80, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, padx=padding, pady=padding)

        # Scrollbar for the text widget
        log_scrollbar = tk.Scrollbar(self.logger_frame, command=self.log_text.yview)
        log_scrollbar.grid(row=0, column=1, sticky='nsew')
        self.log_text['yscrollcommand'] = log_scrollbar.set

    def log(self, message):
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)

    def get_existing_projects(self):
        existing_projects = []
        # Assuming all directories in the current working directory are project folders
        for item in os.listdir(os.getcwd()):
            if os.path.isdir(item):
                existing_projects.append(item)
        return existing_projects

    def select_folder(self):
        selected_folder = self.folder_var.get()
        if selected_folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, selected_folder)



    # FOLDER LOGIC
    def submit_data(self):
        project_name = self.folder_entry.get()
        # check if empty string is not inserted
        if project_name == "":
            self.log("Enter a valid project name")
            return

        # Check if the specified project folder exists; if not, create it
        project_path = os.path.join(os.getcwd(), project_name)
        if not os.path.exists(project_path):
            os.makedirs(project_path)

        # Find the next flight folder number
        flight_folder_number = 1
        while os.path.exists(os.path.join(project_path, f"flight_{flight_folder_number:02d}")):
            flight_folder_number += 1

        # Create a new flight folder
        new_flight_folder = os.path.join(project_path, f"flight_{flight_folder_number:02d}")
        os.makedirs(new_flight_folder)

        # Create GeoTag, Output, and Raw folders inside the new flight folder
        geo_tag_folder = os.path.join(new_flight_folder, "GeoTag")
        output_folder = os.path.join(new_flight_folder, "Output")
        raw_folder = os.path.join(new_flight_folder, "Raw")
        os.makedirs(geo_tag_folder)
        os.makedirs(output_folder)
        os.makedirs(raw_folder)

        # Inside Raw, create 'csv' and 'images' folders
        raw_csv_folder = os.path.join(raw_folder, "csv")
        raw_images_folder = os.path.join(raw_folder, "images")
        os.makedirs(raw_csv_folder)
        os.makedirs(raw_images_folder)


        # Inside Output, create 'logs' folders
        raw_logs = os.path.join(output_folder, "Log")
        os.makedirs(raw_logs)
        

        # Move the selected CSV file to the raw_csv_folder
        csv_file_path = self.csv_entry.get()
        if os.path.isfile(csv_file_path):
            new_csv_path = os.path.join(raw_csv_folder, os.path.basename(csv_file_path))
            shutil.move(csv_file_path, new_csv_path)
            self.log(f"CSV File moved to: {new_csv_path}")

        # Move the selected Images folder to the raw_images_folder
        images_folder_path = self.images_entry.get()
        
        if os.path.isdir(images_folder_path):
            new_images_path = os.path.join(raw_images_folder, os.path.basename(images_folder_path))
            shutil.move(images_folder_path, new_images_path)
            self.log(f"Images Folder moved to: {new_images_path}")

        
        # Update the list of project names
        self.project_names = self.get_existing_projects()

        # Set the updated project names as the values for the Combobox
        self.folder_entry['values'] = self.project_names

        # Select the newly created folder in the Combobox
        self.folder_entry.set(new_flight_folder)
        self.log("Data submitted successfully.")
        
        # Update the flight entry to the new flight folder
        self.folder_entry.delete(0, tk.END)
        self.folder_entry.insert(0, new_flight_folder)

    def geotag_images(self):
        self.log("Geotagging images...")
        # Add your geotagging logic here
        self.log("Geotagging completed.")

    def run_process(self,csv_entry,images_entry):

        csv_file_path = self.csv_entry.get()
        images_folder_path = self.images_entry.get()
        
        self.log(csv_file_path)
        self.log(images_folder_path)
        # Add your process logic here
        
        self.log("start process")


def browse_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)


def browse_folder(entry):
    folder_path = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, folder_path)


if __name__ == "__main__":
    app = MetaShape_App()
    app.mainloop()
