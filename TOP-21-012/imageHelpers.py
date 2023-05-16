import os

def convertToPNG(filename):
    rawname = filename.replace(".pdf", "")
    olddir = os.getcwd()
    os.chdir(olddir+"/input")
    os.system("pdftoppm "+filename+" "+rawname+" -png")
    os.system("mv "+rawname+"-1.png "+olddir+"/output/"+rawname+".png")
    os.chdir(olddir+"/output")
    os.system("cp "+rawname+".png thumb_"+rawname+".png")
    os.chdir(olddir)
