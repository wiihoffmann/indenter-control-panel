
import csv
from datalogger.MeasurementData import *

class Logger():
    """ Data logger for loading/saving CSV files
    This class allows for the loading and saving of step and load
    data from CSV files.
    """

    def loadFile(self, filename):
        """ Given a path/filename for a CSV file, load the data from it.
        Parameters:
            filename (str): the path/filename of the CSV file to load data from
        Returns:
            x (int): array of sample numbers
            step (int): array of step (displacement) data
            load (float): array of load data
        """
        data = MeasurementData([],[],[], filename)
        phaseMessage = ""

        # try opening the file and iterating over the data
        with open(filename, 'r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            for index, row in enumerate(lines):
                # discard the first row (column headers)
                if index == 0:
                    ", ".join(row)
                else:
                    # append the data from the row
                    try:
                        data.sample.append(index)
                        data.step.append(float(row[0])/100)
                        data.load.append(float(row[1]))

                        # load in the phase info (if applicable)
                        if len(row) >= 3 and row[2] != phaseMessage:
                            phaseMessage = row[2]

                            if data.initialApproachStart == -1:
                                data.initialApproachStart = index
                            elif data.preloadHoldStart == -1:
                                data.preloadHoldStart = index
                            elif data.mainApproachStart == -1:
                                data.mainApproachStart = index              
                            elif data.mainHoldStart == -1:
                                data.mainHoldStart = index
                            elif data.retractStart == -1:
                                data.retractStart = index        
                    except:
                        pass

        return data


    def saveFile(self, filename, data):
        """ Save the results of a measurement to a CSV file.
        Parameters:
            filename (str): the path/filename of the CSV file to load data from
            x (int): array of sample numbers
            step (int): array of step (displacement) data
            load (float): array of load data
        """
        # make sure we have a .csv file ending
        if not filename.endswith(".csv"):
            filename += ".csv"

        # open the file for writing the data
        with open(filename, mode='w') as csvfile:
            lines = csv.writer(csvfile, delimiter=',')
            lines.writerow(["Step (steps)", "Load (N)"])
            stage = ""

            # insert the data
            for i in range(min(len(data.sample), len(data.step), len(data.load))):
                
                if data.sample[i] == data.initialApproachStart:
                    stage = "initial approach"
                elif data.sample[i] == data.preloadHoldStart:
                    stage = "holding preload" 
                elif data.sample[i] == data.mainApproachStart:
                    stage = "applying full load"                 
                elif data.sample[i] == data.mainHoldStart:
                    stage = "holding full load" 
                elif data.sample[i] == data.retractStart:
                    stage = "retracting"
                                  
                lines.writerow([data.step[i]*100, data.load[i], stage])
        return

