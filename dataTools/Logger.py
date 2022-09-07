
import csv
from dataTools.MeasurementData import *

STEP_HEADER = "Step (steps)"
LOAD_HEADER = "Load (N)"
STAGE_HEADER = "Stage"
VAS_HEADER = "VAS score (1-100)"
THRESHOLD_HEADER = "Pain threshold (kg)"

class Logger():
    """ Data logger for loading/saving CSV files
    This class allows for the loading and saving of step and load
    data from CSV files.
    """

    def makeHeaderRow(self, data :List[MeasurementData]):        
        header = []
        if data.step != []:
            header.append(STEP_HEADER)

        if data.load != []:
            header.append(LOAD_HEADER)
        
        if data.phase != []:
            header.append(STAGE_HEADER)
        
        if data.VASScores != []:
            header.append(VAS_HEADER)
        
        if data.maxLoad != []:
            header.append(THRESHOLD_HEADER)
    
        return header


    def makeDataRow(self, data :MeasurementData, i):
        row = []
        if i < len(data.step):
            row.append(int(round(data.step[i]*100))) # unscale the displacement
        if i < len(data.load):
            row.append(data.load[i])
        if i < len(data.phase):
            row.append(data.phase[i])
        if i < len(data.VASScores):
            row.append(data.VASScores[i])
        if i < len(data.maxLoad):
            row.append(data.maxLoad[i])

        return row


    def readDataRow(self, header, row, index):        
        self.data.sample.append(index)

        if STEP_HEADER in header:
            self.data.step.append(float(row[header.index(STEP_HEADER)])/100)
        
        if LOAD_HEADER in header:
            self.data.load.append(float(row[header.index(LOAD_HEADER)]))

        if STAGE_HEADER in header:
            self.data.phase.append(int(row[header.index(STAGE_HEADER)]))

        if VAS_HEADER in header:
            self.data.VASScores.append(int(row[header.index(VAS_HEADER)]))

        if THRESHOLD_HEADER in header:
            self.data.maxLoad.append(float(row[header.index(THRESHOLD_HEADER)]))
        return


    def loadFile(self, filename):
        """ Given a path/filename for a CSV file, load the data from it.
        Parameters:
            filename (str): the path/filename of the CSV file to load data from
        Returns:
            x (int): array of sample numbers
            step (int): array of step (displacement) data
            load (float): array of load data
        """
        self.data = MakeBlankMeasurementData()
        self.data.filename = filename

        # try opening the file and iterating over the data
        with open(filename, 'r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            header = ""
            
            for index, row in enumerate(lines):
                # discard the first row (column headers)
                if index == 0:
                    header = row
                else:
                    # append the data from the row
                    try:
                        self.readDataRow(header, row, index)  
                    except:
                        pass
        return self.data


    def saveFile(self, dataset, filename):
        """ Save the results of a measurement to a CSV file.
        Parameters:
            filename (str): the path/filename of the CSV file to load data from
            x (int): array of sample numbers
            step (int): array of step (displacement) data
            load (float): array of load data
        """
        
        # name each trial if applicable
        if len(dataset) > 1:
            count = 0
            for data in dataset:
                if count == 0:
                    data.filename = filename + "-full"
                else:
                    data.filename += filename + "-trial" + str(count)
                count += 1
        else:
            dataset[0].filename = filename
        
        # save each file
        for data in dataset:
            # make sure we have a .csv file ending
            if not data.filename.endswith(".csv"):
                data.filename += ".csv"

            # open the file for writing the data
            with open(data.filename, mode='w') as csvfile:
                lines = csv.writer(csvfile, delimiter=',')
                # write the header 
                lines.writerow(self.makeHeaderRow(data))

                # insert the data
                for i in range(len(data.sample)):
                    lines.writerow(self.makeDataRow(data, i))
        return

