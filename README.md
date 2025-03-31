# EMG Analysis App

## Project Description

The **EMG Analysis App** is an application designed for the comprehensive analysis of electromyography (EMG) signals. It offers a user-friendly interface to capture, process, and visualize data from EMG bands. The application aims to streamline signal processing and analysis by integrating various modules that handle data visualization, machine learning-based classification, and real-time charting.

## Functionalities

### User Interface (PyQT)
- **EMG Band Interface:**  
  Connect and interact with EMG hardware to capture signals.
- **Data Visualization:**  
  Real-time charts and graphical representations of EMG signals.
- **Data Management:**  
  Integrated module for logging, database synchronization, and managing stored data.
- **User Authentication:**  
  Basic login system for secure access.
- **Classification & Machine Learning:**  
  Tools for classifying and training on the collected data.

### Data Synchronization
- Framework integration for consistent synchronization with a database.

### Containerization
- Docker support for deploying the application in isolated environments, ensuring consistency across different setups.

## Technologies Used

- **Programming Language:** Python
- **User Interface Framework:** PyQT
- **Containerization:** Docker (with accompanying Docker Compose configurations)
- **Machine Learning & Data Processing:**  
  Python libraries for signal processing and classification (exact libraries to be specified based on implementation)
- **Database Integration:**  
  Frameworks or custom connectors for handling data storage and retrieval

## Project Structure

- **assets/**  
  Contains graphic resources and supplementary files for the UI.

- **backend/**  
  Manages server-side logic and data handling.

- **band_interface/**  
  Module responsible for interfacing with the EMG band hardware.

- **band_tools/**  
  A set of tools and scripts dedicated to the processing and analysis of EMG signals.

- **classifiers_and_tests/**  
  Houses the implementations of various classifiers and the corresponding unit tests for machine learning components.

- **cloud_storage/**  
  Integration module for cloud-based storage solutions.

- **legacy_to_be_deleted/**  
  Contains outdated code or experimental features marked for removal.

- **visualizers/**  
  Modules dedicated to rendering data visualizations and real-time charts.

### Key Files

- **connector.py:**  
  Manages the connection with the database.

- **main.py:**  
  The main entry point of the application.

- **setup_env.sh:**  
  Script for setting up the project environment.

- **unit_tests.py:**  
  Contains unit tests for verifying the functionality of various modules.
