import os

directory = "Y:/Dropbox/000_Projects/000_AEC_Hackathon2016/DF"

dirs = os.listdir(directory)

for i in range(len(dirs)):
	end_dir = directory+"/"+dirs[i]+"/DF/"
	os.system(end_dir+"/"+dirs[i]+"_0_RAD.bat")
