from utils import *
from ml import *

global_path = "data/"
directory_name = "2018-05-26"

def main():
    # Process all files in one directory
    #data = parse_folder(global_path + '/2018-05-21')

    if not os.path.exists(global_path + "lines"):
        print("Processing directory: ", global_path + directory_name)
        parse_folder(global_path + directory_name)
        print("Finished, all the data saved in" + global_path + "lines")

    if not os.path.exists(global_path + "c_lines"):
        os.makedirs(global_path + "c_lines")
        print("Processing all csv files to triples")
        path_to_traverse = global_path + "lines"
        path_to_save = global_path + "c_lines"
        convert_all_csv(path_to_traverse, path_to_save)
        print("Finished, all the data saved in: ", path_to_save)

    filename_to_process = "concatenated.csv"
    if not os.path.exists(filename_to_process):
        print("Processing all triples-csv files")
        path_to_traverse = global_path + "c_lines"
        all_csv_to_single_csv(path_to_traverse, filename_to_process)
        print("Finished, filename to process is: ", filename_to_process)

    if os.path.exists(filename_to_process):
        df = pd.read_csv(filename_to_process, header=None)
        df.dropna(inplace=True)
        run_neural_network(df)
    else:
        raise Exception("File does not exist")
    
if __name__ == "__main__":
    main()
