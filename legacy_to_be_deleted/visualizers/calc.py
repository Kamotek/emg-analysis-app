import pandas as pd
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


    
def main():
    def get_absolute_path(relative_path: bytes | str) -> bytes | str:
        """
        Get Absolute path from relative_path
        Args:
            relative_path: Relative path (in relation to current file)

        Returns: Absolute path
        """
        return os.path.join(Path(os.path.abspath(__file__)).parent, relative_path)

    import scipy.io

    def extract_data(relative_path: bytes | str, name: str) -> np.ndarray:
        """
        Extract data from MatLab file to an array.
        Args:
            relative_path: Relative path to .mat file
            name: Name of the column with desired data in .mat file

        Returns: Array with desired data
        """
        path = get_absolute_path(relative_path)
        print(relative_path)
        print(path)
        return np.array(scipy.io.loadmat(path)[name])


    def get_ninapro_dataset() -> pd.DataFrame:
        """
        Go through original files of NinaPro dataset and convert them into form useful for computation in python.
        Returns: Dataframe with dataset.
        """
        recordings = []
        labels = []
        restimulus = []  # Added restimulus list
        series = []
        subjects = []
        last_series = -1
        for subject in range(1, 10):
            start_gest = 0
            for session in range(1, 4):
                data = extract_data(os.path.join(
                    '../../',
                    'db',
                    f's{str(subject)}',
                    f'E{str(session)}_A1.mat'),
                    'emg')
                gesture = extract_data(os.path.join(
                    '../'
                    'db',
                    f's{str(subject)}',
                    f'E{str(session)}_A1.mat'),
                    'stimulus')
                restimulus_data = extract_data(os.path.join(
                    '../../',
                    'db',
                    f's{str(subject)}',
                    f'E{str(session)}_A1.mat'),
                    'restimulus')  # Extract restimulus data
                recordings.extend([d.reshape(16, -1) for d in data])
                proper_gesture = [(g if g == 0 else g + start_gest) for g in gesture[:, 0]]
                start_gest = max(proper_gesture)
                labels.extend(proper_gesture)
                restimulus.extend(restimulus_data)  # Append restimulus data
                counter = 1 + last_series
                series.append(counter)
                previous = gesture[0, 0]
                for gest in gesture[1:, 0]:
                    if gest != previous:
                        counter += 1
                    previous = gest
                    series.append(counter)
                last_series = counter
                subjects.extend([subject for _ in range(gesture.shape[0])])
        df = pd.DataFrame({'record': recordings, 'label': labels, 'restimulus': restimulus, 'spectrograms': series, 'subject': subjects})
        df = df.loc[df['label'] != 0]
        df['label'] = df['label'] - 1
        df.reset_index(inplace=True)
        return df



    def draw_charts_x():
            df = get_ninapro_dataset()
            subjects = df['subject'].unique()
            labels = df['label'].unique()
            
            for subject in subjects:
                for label in labels:
                    patient_data = df[(df['subject'] == subject) & (df['label'] == label)]
                    spectrograms = patient_data['record']
                    
                    for spectrogram in spectrograms:
                        # Ignore extreme values
                        spectrogram = np.clip(spectrogram, np.percentile(spectrogram, 1), np.percentile(spectrogram, 99))
                        plt.plot(spectrogram, color='blue', alpha=0.7, linewidth=1)
                    
                    plt.title(f'Charts for Label {label} (Patient {subject})')
                    plt.xlabel('Time')
                    plt.ylabel('Value')
                    plt.show()

    #draw_charts_x()



    def draw_charts():
        df = get_ninapro_dataset()
        patient_data = df[(df['subject'] == 1) & (df['label'] == 3)]
        spectrograms = patient_data['record']
        
        for spectrogram in spectrograms:
            # Ignore extreme values
            spectrogram = np.clip(spectrogram, np.percentile(spectrogram, 1), np.percentile(spectrogram, 99))
            plt.plot(spectrogram, color='blue', alpha=0.7, linewidth=1)
        
        plt.title('Charts for Label 3 (Patient 1)')
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.show()

    #draw_charts()
        

    def draw_chart_by_restimulus(df: pd.DataFrame):
        chart_values = []
        current_chart_label = None
        
        for index, row in df.iterrows():
            record = row['record']
            restimulus = row['restimulus']
            label = row['label']
            
            if restimulus != 0:
                chart_values.append(record)
                
            if restimulus == 0 or index == len(df) - 1:
                if chart_values:
                    chart_values = np.array(chart_values).reshape(-1, 16)  # Reshape chart_values to (787, 16)
                    
                    
                    plt.plot(chart_values, color='blue', alpha=0.7, linewidth=1)
                    plt.title(f'Chart for Label {current_chart_label}')
                    plt.xlabel('Time')
                    plt.ylabel('Value')
                    plt.ylim(-100, 100)  # Set fixed y-axis limits
                    plt.show()
                
                chart_values = []
                current_chart_label = label


    draw_chart_by_restimulus(get_ninapro_dataset())

if __name__ == '__main__':
   main() 