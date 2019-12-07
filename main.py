from utils import *

global_path = 'data'

def main():
    # Read single file
    #data = parse_file(global_path + '/2018-05-26/part-0-0')

    # Read all files in one directory
    data = parse_folder(global_path + '/2018-05-21')

    # show_rows(data, amount=10)
    # show_row_details(data, i=0)

    # filenames is hashmap in form of -> line (string) : list (list of strings)
    #filenames = traverse_directory(global_path + "/lines")

if __name__ == "__main__":
    main()
