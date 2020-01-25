from utils import *
from ml import *
from sklearn.model_selection import train_test_split

def norm(x, stats):
    return (x - stats['mean']) / stats['std']

global_path = "data/"
directory_name = "2018-05-26"

def main():
    # Process all files in one directory
    #data = parse_folder(global_path + '/2018-05-21')
    #parse_folder_PCA(global_path + '/2018-05-21')

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

    print("Reading data from " + filename_to_process)
    df = pd.read_csv(filename_to_process, header=None)
    df.dropna(inplace=True)
    length = len(df.columns)

    print("Splitting data into training and test datasets")
    training_data, testing_data = train_test_split(df, test_size=0.3)
    
    Y_train = training_data.pop(length - 1)
    Y_test = testing_data.pop(length - 1)

    train_stats = training_data.describe().transpose()
    test_stats = testing_data.describe().transpose()

    X_train = norm(training_data, train_stats)
    X_test = norm(testing_data, train_stats)

    #print("Running neural network on datasets")
    #run_neural_network(X_train, Y_train, X_test, Y_test)

    #print("Running random forest on datasets")
    #run_random_forest(X_train, Y_train, X_test, Y_test)

    print("Running KMeans on datasets")
    run_k_means(X_train, Y_train, X_test, Y_test)
    
if __name__ == "__main__":
    main()
