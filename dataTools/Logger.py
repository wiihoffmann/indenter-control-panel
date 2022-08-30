
import csv
from dataTools.MeasurementData import *

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
        data = MeasurementData([],[],[],[], filename)

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
                        data.phase.append(int(row[2]))   
                    except:
                        pass
        return data


    def saveFile(self, dataset, filename):
        """ Save the results of a measurement to a CSV file.
        Parameters:
            filename (str): the path/filename of the CSV file to load data from
            x (int): array of sample numbers
            step (int): array of step (displacement) data
            load (float): array of load data
        """
        if len(dataset) > 1:
            count = 0
            for data in dataset:
                if count == 0:
                    data.filename += "-full"
                else:
                    data.filename += "-trial" + str(count)
                count += 1
        else:
            dataset[0].filename = filename
        
        for data in dataset:
            # make sure we have a .csv file ending
            if not data.filename.endswith(".csv"):
                data.filename += ".csv"

            # open the file for writing the data
            with open(data.filename, mode='w') as csvfile:
                lines = csv.writer(csvfile, delimiter=',')
                lines.writerow(["Step (steps)", "Load (N)", "Stage"])

                # insert the data
                for i in range(min(len(data.sample), len(data.step), len(data.load), len(data.phase))):                                  
                    lines.writerow([int(round(data.step[i]*100)), data.load[i], data.phase[i]])
        return

