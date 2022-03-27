
import csv

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
        x = []
        step = []
        load = []
        
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
                        x.append(index)
                        step.append(float(row[0]))
                        load.append(float(row[1]))
                    except:
                        pass

        return x, step, load


    def saveFile(self, filename, x, step, load):
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
            lines.writerow(["Step", "Load"])
            
            # insert the data
            for i in range(min(len(x), len(step), len(load))):
                lines.writerow([step[i], load[i]])
        return

