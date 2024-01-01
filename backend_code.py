def function1(images_folder_path,csv_file_path):
    print("images_folder_path",images_folder_path)
    print("csv_file_path",csv_file_path)

def function2(geolocation_path, output_path):
    print("geolocation_path", geolocation_path)   
    print("output_path",  output_path) 


def function3(PSX_path, log_path):
    print("PSX_path", PSX_path) 
    print("log_path", log_path)
    

def main(images_folder_path, csv_file_path, geolocation_path, output_path, PSX_path, log_path):

    print("\n")
    function1(images_folder_path,csv_file_path)
    function2(geolocation_path, output_path)
    function3(PSX_path, log_path)

# if __name__ == "__main__":
#     main()
