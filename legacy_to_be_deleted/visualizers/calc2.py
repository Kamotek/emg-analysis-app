
from scipy.io import loadmat
from matplotlib.widgets import Button
import matplotlib.pyplot as plt


def main():
    # Load the .mat file
    data = loadmat('db/s1/E1_A1.mat')

    # Define the data keys to plot
    data_keys = ['acc', 'stimulus', 'glove', 'repetition', 'restimulus', 'rerepetition']

    # Get patient information
    age = data['age'][0][0]
    gender = data['gender'][0]
    weight = data['weight'][0][0]
    # Import the required modules
    import matplotlib.pyplot as plt
    # Define the dataset folders and files
    folders = ['db/s1', 'db/s2', 'db/s3', 'db/s4', 'db/s5', 'db/s6', 'db/s7', 'db/s8', 'db/s9', 'db/s10']
    files = ['E1_A1.mat', 'E2_A1.mat', 'E3_A1.mat']

    # Define the initial dataset index
    current_folder_index = 0
    current_file_index = 0

    # Function to load the current dataset
    def load_current_dataset():
        folder = folders[current_folder_index]
        file = files[current_file_index]
        data = loadmat(f'{folder}/{file}')
        return data

    # Function to update the plots with the current dataset
    def update_plots():
        data = load_current_dataset()

        # Clear the subplots
        for ax in axs.flat:
            ax.clear()

        # Plot the data keys
        for i, key in enumerate(data_keys):
            ax = axs[i // 3, i % 3]
            ax.set_title(f'{key.capitalize()} Data')
            ax.set_xlabel('Time')
            ax.set_ylabel(key.capitalize())
            ax.plot(data[key])

            # Add patient information to the plot
            ax.text(0.95, 0.95, f'Age: {data["age"][0][0]}\nGender: {data["gender"][0]}\nWeight: {data["weight"][0][0]} kg',
                    verticalalignment='top', horizontalalignment='right', transform=ax.transAxes)

        # Plot the EMG data
        emg_ax = axs[1, 2]  # Define the emg_ax variable
        emg_ax.clear()
        for i, col in enumerate(data['emg'].T):
            emg_ax.set_title('EMG Data')
            emg_ax.set_xlabel('Time')
            emg_ax.set_ylabel('EMG')
            emg_ax.plot(col)
            emg_ax.legend(['electrode 1', 'electrode 2', 'electrode 3', 'electrode 4', 'electrode 5', 'electrode 6', 'electrode 7', 'electrode 8', 'flexor digitorum superficialis', 'extensor digitorum superficialis', 'biceps brachii', 'triceps brachii'])

            # Add patient information to the plot
            emg_ax.text(0.95, 0.95, f'Age: {data["age"][0][0]}\nGender: {data["gender"][0]}\nWeight: {data["weight"][0][0]} kg\nHeight: {data["height"]} cm',
                        verticalalignment='top', horizontalalignment='right', transform=emg_ax.transAxes)

        plt.tight_layout()
        plt.draw()

    # Function to handle the next button click
    def next_dataset(event):
        global current_folder_index, current_file_index
        current_file_index += 1
        if current_file_index >= len(files):
            current_file_index = 0
            current_folder_index += 1
            if current_folder_index >= len(folders):
                current_folder_index = 0
        update_plots()

    # Function to handle the previous button click
    def previous_dataset(event):
        global current_folder_index, current_file_index
        current_file_index -= 1
        if current_file_index < 0:
            current_folder_index -= 1
            if current_folder_index < 0:
                current_folder_index = len(folders) - 1
            current_file_index = len(files) - 1
        update_plots()

    # Load the initial dataset
    data = load_current_dataset()

    # Create subplots
    fig, axs = plt.subplots(2, 3, figsize=(16, 12))
    fig.subplots_adjust(hspace=0.5)  # Increase the vertical spacing between subplots

    # Create the next and previous buttons
    next_button_ax = plt.axes([0.9, 0.05, 0.1, 0.075])
    next_button = Button(next_button_ax, 'Next')
    next_button.on_clicked(next_dataset)

    previous_button_ax = plt.axes([0.8, 0.05, 0.1, 0.075])
    previous_button = Button(previous_button_ax, 'Previous')
    previous_button.on_clicked(previous_dataset)

    # Plot the initial dataset
    update_plots()

    # Show the plots
    plt.show()

    # Create subplots
    fig, axs = plt.subplots(2, 3, figsize=(16, 12))
    fig.subplots_adjust(hspace=0.5)  # Increase the vertical spacing between subplots

    # Plot the data keys
    for i, key in enumerate(data_keys):
        ax = axs[i // 3, i % 3]
        ax.set_title(f'{key.capitalize()} Data')
        ax.set_xlabel('Time')
        ax.set_ylabel(key.capitalize())
        ax.plot(data[key])

        # Add patient information to the plot
        ax.text(0.95, 0.95, f'Age: {age}\nGender: {gender}\nWeight: {weight} kg\nHeight: {data["height"]} cm',
                verticalalignment='top', horizontalalignment='right', transform=ax.transAxes)

    # Plot the EMG data
    plt.figure(figsize=(16, 12))
    for i, col in enumerate(data['emg'].T):
        plt.title('EMG Data')
        plt.xlabel('Time')
        plt.ylabel('EMG')
        plt.plot(col)
        plt.legend(['electrode 1', 'electrode 2', 'electrode 3', 'electrode 4', 'electrode 5', 'electrode 6', 'electrode 7', 'electrode 8', 'flexor digitorum superficialis', 'extensor digitorum superficialis', 'biceps brachii', 'triceps brachii'])

        # Add patient information to the plot
        plt.text(0.95, 0.95, f'Age: {age}\nGender: {gender}\nWeight: {weight} kg\nHeight: {data["height"]} cm',
                verticalalignment='top', horizontalalignment='right', transform=plt.gca().transAxes)

    plt.tight_layout()
    plt.show()

    # dict_keys(['__header__', '__version__', '__globals__', 
    # 'emg', 'acc', 'stimulus', 'glove', 'subject', 
    # 'exercise', 'repetition', 'restimulus', 'rerepetition', 
    # 'age', 'circumference', 'frequency', 'gender', 'height', 'weight', 'laterality', 'sensor'])

if __name__ == '__main__':
    main()