from LogReader.LogReader import LogReader

filename = '../log'
reader = LogReader(filename)
reader.start()

print("------------- FINISHED ------------------ ")
