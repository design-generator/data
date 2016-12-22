import os

directory = "D:/Dropbox/000_AEC_Hackathon2016/Runs"

dirs = os.listdir(directory)

while True:
    for i in range(len(dirs)):
        end_dir = directory+"/"+dirs[i]+"/OpenStudio/"+dirs[i]+"/ModelToIdf"
        if "in.idf" in os.listdir(end_dir):
            os.system("C:/EnergyPlusV8-6-0/energyplus.exe -w D:/Dropbox/000_AEC_Hackathon2016/USA_NY_New.York-LaGuardia.AP.725030_TMY3/USA_NY_New.York-LaGuardia.AP.725030_TMY3.epw -d "+end_dir+" "+end_dir+"/in.idf")
        else:
            pass