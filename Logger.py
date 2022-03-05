import csv

class Logger():

    def __init__(self):
        pass
    

    def loadFile(self, filename):
        x = []
        step = []
        load = []

        with open(filename, 'r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')

            for index, row in enumerate(lines):
                if index == 0:
                    filler = ", ".join(row)
                else:
                    try:
                        x.append(index)
                        step.append(float(row[0]))
                        load.append(float(row[1]))
                    except:
                        pass

        return x, step, load


    def saveFile(self, filename, x, step, load):
        # make sure we have a .csv file ending
        if not filename.endswith(".csv"):
            filename += ".csv"

        with open(filename, mode='w') as csvfile:
            lines = csv.writer(csvfile, delimiter=',')
            lines.writerow(["Step", "Load"])

            for i in range(min(len(x), len(step), len(load))):
                lines.writerow([step[i], load[i]])

