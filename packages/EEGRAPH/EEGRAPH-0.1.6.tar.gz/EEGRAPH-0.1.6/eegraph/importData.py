import mne
import pandas as pd
from .tools import process_channel_names
    
class InputData:
    def __init__(self, path, exclude):
        self.path = path
        self.exclude = exclude
        
    def load(self):       
        #Split the path in two parts, left and right of the dot. 
        file_type = self.path.split(".")

        #https://mne.tools/0.17/manual/io.html
        #Check the extension of the file, and read it accordingly. 
        if(file_type[-1] == 'edf'):
            self.data = mne.io.read_raw_edf(self.path, exclude= self.exclude)
        elif(file_type[-1] == 'gdf'):
            self.data = mne.io.read_raw_gdf(self.path, exclude= self.exclude)
        elif(file_type[-1] == 'vhdr'):
            self.data = mne.io.read_raw_brainvision(self.path, exclude= self.exclude)
        elif(file_type[-1] == 'cnt'):
            self.data = mne.io.read_raw_cnt(self.path, exclude= self.exclude)   
        elif(file_type[-1] == 'bdf'):
            self.data = mne.io.read_raw_edf(self.path, exclude= self.exclude)
        elif(file_type[-1] == 'egi'):
            self.data = mne.io.read_raw_egi(self.path, exclude= self.exclude)
        elif(file_type[-1] == 'mff'):
            self.data = mne.io.read_raw_egi(self.path, exclude= self.exclude)
        elif(file_type[-1] == 'nxe'):
            self.data = mne.io.read_raw_eximia(self.path, exclude= self.exclude)
        
        return self.data
    
    def set_montage(self, electrode_montage_path):
        nodes = process_channel_names(self.data.ch_names)
        df = pd.read_csv(electrode_montage_path, delimiter= "\s+|;|:", engine='python')

        
        positions_number = []
        for column in df:
            counter = 0
            for item in list(df[column]):
                if(str(item) in nodes):
                    counter+=1;
                    if(counter > 4):
                        positions_number = list(df[column])
        
        standard_electrodes = ['Cz', 'Pz', 'Oz', 'Fz', 'Nz']
        positions_labels = []
        for column in df:
            for item in list(df[column]):
                if(str(item) in standard_electrodes):
                    positions_labels = list(df[column])
            
        
        new_channel_names= []
        for node in nodes:
            for i in range(len(positions_number)):
                if(str(node) == str(positions_number[i])):
                    new_channel_names.append(positions_labels[i])
                
        return new_channel_names
        

    def display_info(self, ch_names):
        #Extract the raw_data and info with mne methods. 
        self.raw_data = self.data.get_data()
        self.info = self.data.info
        
        #Display information from the data. 
        print('\n\033[1m' + 'EEG Information.')
        print('\033[0m' + "Number of Channels:", self.info['nchan'])
        print("Sample rate:", self.info['sfreq'], "Hz.")
        print("Duration:", round(self.data.times.max(),3), "seconds.")
        print("Channel Names:", ch_names)