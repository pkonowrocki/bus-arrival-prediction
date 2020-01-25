from utils import *
from ml import *
from plotting_functions import *
from sklearn.model_selection import train_test_split

def norm(x, stats):
    return (x - stats['mean']) / stats['std']

global_path = "data/"
directory_name = "2018-05-26"

def main():
    # Process all files in one directory
    #parse_folder(global_path + '2018-05-21', with_old_delay=True)
    #parse_folder_PCA(global_path + '2018-05-21', with_old_delay=False)
    #create_single_file(global_path + '2018-05-21', with_old_delay=True)

    if not os.path.exists(global_path + "lines-PCA"):
        print("Processing directory: ", global_path + directory_name)
        parse_folder_PCA(global_path + directory_name, with_old_delay=False)
        print("Finished, all the data saved in" + global_path + "lines-PCA")

    if not os.path.exists(global_path + "c_lines"):
        os.makedirs(global_path + "c_lines")
        print("Processing all csv files to triples")
        path_to_traverse = global_path + "lines-PCA"
        path_to_save = global_path + "c_lines"
        convert_all_csv(path_to_traverse, path_to_save)
        print("Finished, all the data saved in: ", path_to_save)

    filename_to_process = "concatenated.csv"
    if not os.path.exists(filename_to_process):
        print("Processing all triples-csv files")
        path_to_traverse = global_path + "c_lines"
        all_csv_to_single_csv(path_to_traverse, filename_to_process)
        print("Finished, filename to process is: ", filename_to_process)

    print("Reading data from " + filename_to_process)
    df = pd.read_csv(filename_to_process, header=None)
    #df.dropna(inplace=True)
    length = len(df.columns)

    print("Splitting data into training and test datasets")
    X_train, X_test = train_test_split(df, test_size=0.3)
    
    Y_train = X_train.pop(length - 1)
    Y_test = X_test.pop(length - 1)

    #print("Running neural network on datasets")
    #predictions = run_neural_network(X_train, Y_train, X_test, Y_test)

    #print("Running random forest on datasets")
    #run_random_forest(X_train, Y_train, X_test, Y_test)

    #print("Running decision tree on datasets")
    run_decision_tree(X_train, Y_train, X_test, Y_test)

    #plot_predictions(predictions, Y_test)

if __name__ == "__main__":
    main()
