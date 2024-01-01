from tkinter import *
import os
import tkinter as tk
from tkinter import ttk, filedialog
import shutil
import threading
import tkinter.ttk as ttk
from backend_code import *
from PIL import Image, ImageTk

images_folder_path = ""
csv_file_path = ""
geolocation_path = ""
output_path = ""
PSX_path = ""
log_path = ""

project_path = ""
selected_quality = ""
csv_selected = False
images_selected = False

window = Tk()

def create_button(input_frame, text, bd, command, size, icon=None, shape='sunken', width=None):
    def on_enter(event):
        button.config(bg='#DADADA', relief=shape)  
    def on_leave(event):
        button.config(bg='#EFEFEF', relief=shape) 
    def on_click(event):
        button.config(bg='white', relief="sunken") 
    def on_release(event):
        button.config(bg='#D0CFC9',relief=shape)  

    button_params = {
        "text": text,
        "bd": 0,  # Set to 1 for a single-bordered outline
        "command": command,
        "background": "#EFEFEF",
        "relief": shape,  # Set the initial relief
    }

    
    if icon:
       
        button_params["image"] = icon
        button_params["compound"] = tk.LEFT  # Set the icon to appear to the left of the text

    button = tk.Button(input_frame, **button_params)

    # Set the size of the button if provided
    if size:
        button.config(height=size[0], width=size[1])

    # Set the width of the button if provided
    if width:
        button.config(width=width)

    # Bind events to functions
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    button.bind("<Button-1>", on_click)
    button.bind("<ButtonRelease-1>", on_release)

    return button

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    return file_path


def browse_folder():
    folder_path = filedialog.askdirectory()
    return folder_path

def get_image_path():
    global images_folder_path,images_selected
    images_folder_path = browse_folder()
    name_image = images_folder_path.split('/')[-1]

    if images_folder_path!="":
        log(name_image+"Image folder selected")
        images_selected = True
    

def get_csv_path():
    global csv_file_path,csv_selected
    csv_file_path = browse_file()
    name_csv = csv_file_path.split('/')[-1]

    if csv_file_path!="":
        log(name_csv+" file selected")
        csv_selected = True
    
def run_process():

    if not os.path.exists(project_path):
        log("Choose or Create a new project before running")
        return
    if selected_quality=="":
        log("Choose quality before running")
        return
    if not csv_selected:
        log("Choose csv")
        return 
    if not images_selected:
        log("Choose images")
        return
    #calling main function 
    main(images_folder_path, csv_file_path, geolocation_path, output_path, PSX_path, log_path)

    #Error and process print
    log(f"running process \n Quality: {selected_quality}")


def geotag_images():
    log("geotag images")


def create_logger_frame(logger_frame):
    global log_text
    padding = 10

    # Text widget for logging
    log_text = tk.Text(logger_frame, wrap=tk.WORD, background='#DADADA', fg='black', width=40)
    log_text.grid(row=0, column=0, padx=padding, pady=padding, sticky="nsew")

    # Make the Text widget resizable
    logger_frame.grid_rowconfigure(0, weight=1)
    logger_frame.grid_columnconfigure(0, weight=1)

    # Set a fixed height for the logger frame
    logger_frame.config(height=300)  # Set the desired height

    # Make the window resizable with a minimum size
    window.minsize(width=50, height=500)


def log(message):
    global log_text
    log_text.insert(tk.END, '>' + message + '\n\n')
    log_text.see(tk.END)

def create_button_frame(button_frame):
    padding = 2

    # Submit Button
    # Configure column and row weights
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    button_frame.columnconfigure(2, weight=1)
    button_frame.rowconfigure(0, weight=1)

    size=(2,8)
    submit_button = create_button(button_frame, "Submit", 0, submit_data,size, shape='ridge')
    submit_button.grid(row=0, column=0, padx=padding,pady=padding, sticky="ew")

    # Run Button
    run_button = create_button(button_frame, "Run", 0, run_process, size,shape='ridge')
    run_button.grid(row=0, column=1, padx=padding, pady=padding,sticky="we")

    # Geotag Button
    geotag_button = create_button(button_frame, "Geotag", 0, geotag_images,size, shape='ridge')
    geotag_button.grid(row=0, column=2, padx=padding,pady=padding, sticky="we")

def create_input_frame(input_frame):

    padding = 10

    # Project Name Label and Combobox
    folder_label = tk.Label(input_frame, text="Project Name", background='white')
    folder_label.grid(row=1, column=0, padx=padding, pady=padding, sticky="ew")

    global folder_var, folder_entry
    folder_var = tk.StringVar()
    folder_entry = ttk.Combobox(input_frame, textvariable=folder_var, values=get_existing_projects(), font=("Arial", 12))
    folder_entry.grid(row=1, column=1, padx=padding, pady=padding, sticky="we")

    # Quality Label and Combobox
    quality_label = tk.Label(input_frame, text="Select Quality", background='white',width=10,height=1)
    quality_label.grid(row=2, column=0, padx=padding, pady=padding, sticky="we")

    global quality_var, quality_combobox
    quality_var = tk.StringVar()
    quality_combobox = ttk.Combobox(input_frame, textvariable=quality_var, values=["ultra high", "high", "medium", "low"], font=("Arial", 12))
    quality_combobox.grid(row=2, column=1, padx=padding, pady=padding, sticky="we")

    # Function to capture selected quality
    def on_quality_selected(event):
        global selected_quality,project_path
        selected_quality = quality_var.get()
        project_name = folder_entry.get()
        project_path = os.path.join(os.getcwd(), project_name)
        # print(project_path)
        # print(selected_quality)
  


    # Bind the function to "<<ComboboxSelected>>" event
    folder_entry.bind("<<ComboboxSelected>>", on_quality_selected)
    quality_combobox.bind("<<ComboboxSelected>>", on_quality_selected)


    # CSV Browse Button
    csv_button = create_button(input_frame, "Choose csv", 2, get_csv_path, size=(2, 16))
    csv_button.grid(row=3, column=0,columnspan=2, padx=padding, pady=padding, sticky="we")

    # Image Browse Button
    images_button = create_button(input_frame, "Choose images", 2, get_image_path, size=(2, 16))
    images_button.grid(row=4, column=0, columnspan=2,padx=padding, pady=padding, sticky="we")


    # Make folder_entry and quality_combobox responsive
    folder_entry.grid_configure(sticky="we")
    quality_combobox.grid_configure(sticky="we")

def get_existing_projects():
    existing_projects = []
    for item in os.listdir(os.getcwd()):
        if os.path.isdir(item):
            existing_projects.append(item)
    return existing_projects

def select_folder():
    selected_folder = folder_var.get()
    if selected_folder:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, selected_folder)

def submit_data():
    
    global project_path
    global geolocation_path, output_path, PSX_path, log_path
    project_name = folder_entry.get()
    if project_name == "":
        log("Enter a valid project name")
        return

    project_path = os.path.join(os.getcwd(), project_name)
    if not os.path.exists(project_path):
        os.makedirs(project_path)
        log(f"{project_name} Folder Structure Created")
    

    flight_folder_number = 1
    while os.path.exists(os.path.join(project_path, f"flight_{flight_folder_number:02d}")):
        flight_folder_number += 1

    new_flight_folder = os.path.join(project_path, f"flight_{flight_folder_number:02d}")
    os.makedirs(new_flight_folder)

    geo_tag_folder = os.path.join(new_flight_folder, "GeoTag")
    output_folder = os.path.join(new_flight_folder, "Output")
    raw_folder = os.path.join(new_flight_folder, "Raw")
    os.makedirs(geo_tag_folder)
    os.makedirs(output_folder)
    os.makedirs(raw_folder)

    raw_csv_folder = os.path.join(raw_folder, "csv")
    raw_images_folder = os.path.join(raw_folder, "images")
    os.makedirs(raw_csv_folder)
    os.makedirs(raw_images_folder)

    raw_logs = os.path.join(output_folder, "Log")
    os.makedirs(raw_logs)

    raw_psx = os.path.join(output_folder, "PSX")
    os.makedirs(raw_psx)

    geolocation_path = geo_tag_folder
    output_path = output_folder
    PSX_path = raw_psx
    log_path = raw_logs

    

    if os.path.isfile(csv_file_path):
        csv_name = csv_file_path.split("/")[-1]
        new_csv_path = os.path.join(raw_csv_folder, csv_name)
        shutil.move(csv_file_path, new_csv_path)
        log(f"CSV File moved to: {new_csv_path}")

    if os.path.isdir(images_folder_path):
        new_images_path = os.path.join(raw_images_folder, os.path.basename(images_folder_path))
        shutil.move(images_folder_path, new_images_path)
        log(f"Images Folder moved to: {new_images_path}")

    project_names = get_existing_projects()
    folder_entry['values'] = project_names
    folder_entry.set(new_flight_folder)
    
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, new_flight_folder)

def create_frames():
    padding = 10

    # menubar frame
    menubar_frame = Frame(window, bg="#92BABC", height=60)
    menubar_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

    # menubar frame
    menubar_frame2 = Frame(window, bg="white", height=60)
    menubar_frame2.grid(row=1, column=0, columnspan=2, sticky="nsew")

    small_label = Label(menubar_frame2, text=" Automation Software", font=("narrow", 8),background="white")
    small_label.grid(row=1, column=0, sticky="nsew")



    # input frame
    input_frame = ttk.Frame(window, padding=(20, 10), style='input.TFrame')
    input_frame.grid(row=2, column=0, padx=(60,0), pady=(50, 0), sticky="new")  # Adjusted pady
    create_input_frame(input_frame)
    # button_frame
    button_frame = ttk.Frame(window, padding=(10, 10), style='button.TFrame')
    button_frame.grid(row=3, column=0, padx=(60,0), pady=(0, 50), sticky="nsew")  # Adjusted pady
    create_button_frame(button_frame)


    # logger frame
    logger_frame = ttk.Frame(window, padding=(10, 10), style='logger.TFrame')
    logger_frame.grid(row=2, column=1, rowspan=2, padx=(0,50),pady=(28, 28), sticky="nsew")  # Adjusted rowspan to 2
    create_logger_frame(logger_frame)

    # Make frames and window resizable
    window.grid_rowconfigure(0, weight=0)  # Menubar
    window.grid_rowconfigure(1, weight=0)  # Spacer
    window.grid_rowconfigure(2, weight=1)  # Input frame
    window.grid_rowconfigure(3, weight=1)  # Button frame
    window.grid_rowconfigure(4, weight=1)  # Logger frame

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    # Set a fixed initial size for the window
    #window.geometry("800x500")
    # Set a minimum size for the window
    #window.minsize(width=700, height=5


window.title(".")
#737366

window.config(bg='#E7F2F4')
style = ttk.Style()
# Frame background
style.configure('input.TFrame', background='white')
style.configure('button.TFrame', background='white')
style.configure('project.TFrame', background='#E1E0DB')
style.configure('logger.TFrame', background='#E7F2F4')


create_frames()
window.mainloop()
