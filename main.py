def main_menu():
    while True:
        print("Main Menu")
        print("1. Prepare NinaPro Data")
        print("2. Prepare Band Data")
        print("3. Extract NinaPro Features")
        print("4. Extract Band Features")
        print("5. Perform Statistical Analysis")
        print("6. Classification")
        print("7. Visualization")

        choice = input("Enter your choice: ")

        if choice == "1":
            prepare_nina_pro_data()
        elif choice == "2":
            prepare_band_data()
        elif choice == "3":
            extract_nina_pro_features()
        elif choice == "4":
            extract_band_features()
        elif choice == "5":
            perform_statistical_analysis()
        elif choice == "6":
            classification_menu()
        elif choice == "7":
            visualization_menu()
        else:
            print("Invalid choice. Please try again.")


def visualization_menu():
    while True:
        print("Visualization Menu")
        print("1. Plot Raw Data from NinaPro")
        print("2. Plot Raw Data from NinaPro 2")
        print("3. Plot linear regression of Kalman Filtered Data")
        print("4. Plot processed data from NinaPro") 
        print("5. Plot processed data from Band")
        print("6. Plot Wavelet Transform of Kalman Filtered Data")
        choice = input("Enter your choice: ")
        if choice == "1":
            plot_raw_data_ninapro()
        elif choice == "2":
            plot_raw_data_ninapro2()
        elif choice == "3":
            plot_linear_regression_kalman_filtered_data()
        elif choice == "4":
            plot_processed_data_ninapro()
        elif choice == "5":
            plot_processed_data_band()
        elif choice == "6":
            plot_wavelet_transform_kalman_filtered_data()
        else:
            print("Invalid choice. Please try again.")

def classification_menu():
    while True:
        print("Classification Menu")
        print("1. Classification using SVM")
        print("2. Classification using Random Forest")
        print("3. Classification using Logistic Regression")
        print("4. Classification using Random Forest with Feature Selection")
        choice = input("Enter your choice: ")
        if choice == "1":
            classifier_svm()
        elif choice == "2":
            classifier_tree()
        elif choice == "3":
            classifier_logistic_regression()
        elif choice == "4":
            classifier_tree_with_feature_selection()
        else:
            print("Invalid choice. Please try again.")


def plot_raw_data_ninapro():
    import visualizers.calc as calc
    calc.main()

def plot_raw_data_ninapro2():
    import visualizers.calc2 as calc2
    calc2.main()
def plot_linear_regression_kalman_filtered_data():
    import visualizers.draw_linear_regression as draw_linear_regression
    draw_linear_regression.main()
def plot_processed_data_ninapro():
    import visualizers.draw_raw_charts as draw_raw_charts
    draw_raw_charts.main()
def plot_processed_data_band():
    import visualizers.draw as draw_raw_charts_band
    draw_raw_charts_band.main()
def plot_wavelet_transform_kalman_filtered_data():
    import visualizers.show_wavelet as draw_wavelet_transform
    draw_wavelet_transform.main()

def classifier_svm():
    import classifiers_and_tests.classifier_svm as svm
    svm.main()

def classifier_tree():
    import classifiers_and_tests.classifier_tree as tree
    tree.main()


def classifier_tree_with_feature_selection():
    import classifiers_and_tests.classifier_tree_with_feature_selection as tree_with_feature_selection
    tree_with_feature_selection.main()
    
def classifier_logistic_regression():
    import classifiers_and_tests.classifier_logistic_regression as logistic_regression
    logistic_regression.main()

def prepare_nina_pro_data():
    extract_nina_pro_db_by_gender()
    reduce_noises()
    kalman_filter()

    def kalman_filter():
        import nina_pro_tools.kalman_filter as kalman_filter
        kalman_filter.main()


    def extract_nina_pro_db_by_gender():
        import nina_pro_tools.to_csv_by_gender as to_csv
        to_csv.main()

    def reduce_noises():
        import nina_pro_tools.reduce_noises as reduce_noises
        reduce_noises.main()


def prepare_band_data():
    filter_gathered_data()

    def filter_gathered_data():
        import band_tools.kalman_filter as kalman_filter
        kalman_filter.main()



def extract_nina_pro_features():
    import nina_pro_tools.extract_features as extract_features
    extract_features.main()

def extract_band_features():
    import band_tools.extract_features as extract_features
    extract_features.main()

def perform_statistical_analysis():
    import classifiers_and_tests.statistical_tests as statistical_tests
    statistical_tests.main()



if __name__ == "__main__":
    main_menu()