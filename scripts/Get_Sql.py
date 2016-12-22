import os
import shutil

directory = "D:/Dropbox/000_AEC_Hackathon2016/Runs"

dirs = os.listdir(directory)
for i in range(len(dirs)):
        print (dirs[i])

#for i in range(len(dirs)):
 #       print (directory+"/"+dirs[i]+"/OpenStudio/"+dirs[i]+"/ModelToIdf/")
  #      if "eplusout.sql" in os.listdir(directory+"/"+dirs[i]+"/OpenStudio/"+dirs[i]+"/ModelToIdf/"):
   #             shutil.copyfile(directory+"/"+dirs[i]+"/OpenStudio/"+dirs[i]+"/ModelToIdf"+"/eplusout.sql",directory+"/"+dirs[i]+".sql")
    #            shutil.copyfile(directory+"/"+dirs[i]+"/OpenStudio/"+dirs[i]+"/ModelToIdf"+"/eplustbl.htm",directory+"/"+dirs[i]+".htm")