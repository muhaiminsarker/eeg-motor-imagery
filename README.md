# EEG Motor Movement/Imagery Analysis by Muhaimin Sarker

This README includes:
1. Project overview
2. Key features
3. Dataset information
4. Experimental Runs
5. Installation 
6. Usage guide
7. Key functionality
8. Technical details
9. Citations

## 1. Project Overview 

A Streamlit-based interactive application for visualizing and analyzing EEG data from the PhysioNet EEG Motor Movement/Imagery Dataset.

Video link: https://drive.google.com/file/d/1pGV8UOL8_9fwNtRExJd_bbAQDL0SbZQL/view?usp=sharing

## 2. Key Features

- **Interactive Visualization**: Explore EEG time-series data for different subjects and experimental runs
- **Comparative Analysis**: Compare motor cortex activity between different experimental conditions
- **Power Spectrum Analysis**: Visualize Mu/Beta rhythms (8-30Hz) in motor cortex channels
- **Task Classification**: Automatic categorization of experimental runs into task types
- **Responsive Design**: Adapts to different screen sizes with a clean, modern interface

## 3. Dataset Information

This application uses the [EEG Motor Movement/Imagery Dataset](https://physionet.org/content/eegmmidb/1.0.0/) from PhysioNet, containing:
- 109 subjects
- 14 experimental runs per subject (1-2 minutes each)
- 64-channel EEG recordings
- Sampling rate: 160Hz

## 4. Experimental Runs

| Run  | Description                          |
| ---- | ------------------------------------ |
| 1    | Baseline (eyes open)                 |
| 2    | Baseline (eyes closed)               |
| 3    | Actual left/right fist movement      |
| 4    | Imagined left/right fist movement    |
| 5    | Actual both fists/feet movement      |
| 6    | Imagined both fists/feet movement    |
| 7-14 | Repeated tasks (see app for details) |

## 5. Installation

1. Clone this repository:
```bash
   git clone https://github.com/yourusername/capstone-project-muhaiminsarker.git
   cd capstone-project-muhaiminsarker
```
2. Install the required dependencies
```bash  
  pip install -r requirements.txt
```

## 6. Usage Guide
Run the application:
```bash
streamlit run app.py
```

## 7. Key Functionality
- Select subjects (1-109) and experimental runs (1-14)
- Toggle between different visualization options:
	- Sensor locations
	- Power spectrum density
	- All channels view
- Compare different experimental runs
- View detailed run descriptions and metadata

### 8. Technical Details
1. **Data Loading**: EDF files are loaded using MNE-Python
2. **Preprocessing**:
	- Channel renaming and standard montage application
    - Bandpass filtering (8-30Hz for Mu/Beta rhythms)
    - Epoch extraction (-0.5s to 2.0s around events)
3. **Visualization**:
    - Time-series plots of motor cortex activity
    - Power spectral density analysis
    - Comparative views between conditions
### 9. Citations
- Citation for dataset: [Schalk, G., McFarland, D.J., Hinterberger, T., Birbaumer, N., Wolpaw, J.R. BCI2000: A General-Purpose Brain-Computer Interface (BCI) System. IEEE Transactions on Biomedical Engineering 51(6):1034-1043, 2004.](http://www.ncbi.nlm.nih.gov/pubmed/15188875)
- Standard citation for PhysioNet: Goldberger, A., Amaral, L., Glass, L., Hausdorff, J., Ivanov, P. C., Mark, R., ... & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation [Online]. 101 (23), pp. e215–e220.







