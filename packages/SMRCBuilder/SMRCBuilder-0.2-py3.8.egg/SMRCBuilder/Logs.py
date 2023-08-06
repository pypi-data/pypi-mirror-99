from SMRCBuilder import Exceptions
import os

def log(name, logmsg, folder=True):
    """
    Creates A Log File And Writes Log Info
    """
    if type(logmsg) != tuple:
        raise Exceptions.ArgError("Log Message Can Only Be Tuple")
    else:
        if type(name) != str:
            raise Exceptions.ArgError("Datatype Can Only Be A String")
        elif name == "":
            raise Exceptions.ArgError("File Name Cannot Be Blank")
    

        info = ""
        for i in range(len(logmsg)):
            if i+1 == len(logmsg):
                info += f"{str(logmsg[i])}"
            else:
                info += f"{str(logmsg[i])},"

        if folder == True:
            try:
                os.makedirs("Logs")
            except:pass
            
            finally:
                if len(name.split(".")) > 1:
                    fh = open(f"Logs/{name}.csv", 'a')
                    fh.write(info+"\n")
                    fh.close()
                else:
                    fh = open(f"Logs/{name}.csv", 'a')
                    fh.write(info+"\n")
                    fh.close()
        
        else:
            fh = open(f"{name}.csv", 'a')
            fh.write(info+"\n")
            fh.close()

def dellog(name, folder=True):
    try:
        if len(name.split(".")) > 1:
            if folder == True:
                os.remove(f"Logs/{name}")
            else:
                os.remove(f"{name}")
        else:
            if folder == True:
                os.remove(f"Logs/{name}.csv")
            else:
                os.remove(f"{name}.csv")

    except:
        raise Exceptions.FileRemovalError("Error Removing File Does File Exist?")