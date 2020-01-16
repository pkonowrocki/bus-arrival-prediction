from utils import *
from ml import *

global_path = 'data'

def main():
    # Process all files in one directory
    #data = parse_folder(global_path + '/2018-05-21')
    #data = parse_folder(global_path + '/2018-05-26')

    filename_to_process = "concatenated.csv"
    if os.path.exists(filename_to_process):
        df = pd.read_csv(filename_to_process, header=None)
        df.dropna(inplace=True)
        print(df.tail())
        #run_neural_network(df)
    else:
        raise Exception("File does not exist")
    
if __name__ == "__main__":
    main()
