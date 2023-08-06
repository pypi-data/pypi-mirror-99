from SMRCBuilder import Exceptions
import os
import csv
import time

def check(name, directory):
    """
    Checks The GitHub Repository For The Latest Commit Returns True If The Commit Is Different
    """
    try:
        fh = open(f"{directory}/{name}/.linker",'r')
        reader = csv.reader(fh)
        info = []             

    except FileNotFoundError:
        raise Exceptions.LinkerReadError("Could Not Find Interface. Does It Exist?")

    try:
        for line in reader:
            temp = []
            temp.append(line[0])
            temp.append(line[1])
            info.append(temp)
    except:
        raise Exceptions.LinkerReadError("Error Reading Linker File. Is It Properly Formatted?")

    if info[2][0] == "Folder":
        raise Exceptions.NotOnlineError("Interface Cannot Be Local")

    fh = open("Check.sh",'w')
    fh.write(f"""
cd "{directory}/{name}"
rm Temp
rm Temp2
git log -n 1 > Temp
git log -n 1 origin/main > Temp2
""")
    fh.close()
    os.startfile("Check.sh")
    time.sleep(3)

    fh = open(f"{info[0][1]}/Temp",'r')
    interfaceversion = fh.readline().split(" ")[1]
    fh.close()
    
    fh = open(f"{info[0][1]}/Temp2",'r')
    repoversion = fh.readline().split(" ")[1]
    fh.close()

    if interfaceversion != repoversion:
        return True
    
    else:
        return False
    
def getupdate(name, directory, branch="main"):
    """
    Dowloads The Update From GitHub Repository
    """
    try:
        fh = open(f"{directory}/{name}/.linker",'r')
        reader = csv.reader(fh)
        info = []             

    except FileNotFoundError:
        raise Exceptions.LinkerReadError("Could Not Find Interface. Does It Exist?")

    try:
        for line in reader:
            temp = []
            temp.append(line[0])
            temp.append(line[1])
            info.append(temp)
    except:
        raise Exceptions.LinkerReadError("Error Reading Linker File. Is It Properly Formatted?")

    if info[2][0] == "Folder":
        raise Exceptions.NotOnlineError("Interface Cannot Be Local")
    
    fh = open("Update.sh",'w')
    fh.write(f"""
cd "{directory}/{name}"
git reset --hard origin/{branch}
""")
    fh.close()
    os.startfile("Update.sh")