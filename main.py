from utils import *
from ml import *

global_path = 'data'

def main():
    # Process all files in one directory
    #data = parse_folder(global_path + '/2018-05-21')
    #data = parse_folder(global_path + '/2018-05-26')

    if os.path.exists("concatenated.csv"):
        df = pd.read_csv("concatenated.csv")
        run_neural_network(df)
    
if __name__ == "__main__":
    main()
