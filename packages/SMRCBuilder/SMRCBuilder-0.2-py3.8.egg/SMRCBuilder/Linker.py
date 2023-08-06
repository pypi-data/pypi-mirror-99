from SMRCBuilder import Exceptions
import csv
import os
import zipfile

def setup(name, version, repository, author):
    """
    Creates Your Linker File With A GitHub Repository
    """
    info = [name, version, repository, author]
    for i in info:
        if type(i) != str:
            raise Exceptions.ArgError("Argument Must Be String")
            
    fh = open(f"{name}.linker",'w')
    try:
        fh.write(f"Name,{name}\n")
        fh.write(f"Version,{version}\n")
        fh.write(f"Repository,{repository}\n")
        fh.write(f"Author,{author}")
        fh.close()
    except:
        raise Exceptions.LinkerBuildError("Error Building Linker File")
    print(f"Linker '{name}' Created")

def localsetup(name, version, folder, author):
    """
    If You Don't Have A GitHub Repo, You Can Use A Zip File. However, You May Not Be Able To Install Updates With This Method.
    """
    def zipdir(path, ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file))

    info = [name, version, folder, author]
    for i in info:
        if type(i) != str:
            raise Exceptions.ArgError("Argument Must Be String")

    try:
        os.rename(folder, name)

    except:
        raise Exceptions.LinkerBuildError("Could Not Rename Folder, Does Folder Exist?")

    try:
        fh = open(f"{name}/.linker",'w')
        fh.write(f"Name,{name}\n")
        fh.write(f"Version,{version}\n")
        fh.write(f"Folder,{folder}\n")
        fh.write(f"Author,{author}")
        fh.close()
    
    except FileNotFoundError:
        raise Exceptions.LinkerBuildError("Error Building Linker File, Does Folder Exist?")

    zipf = zipfile.ZipFile(f'{name}.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir(f'./{name}', zipf)
    zipf.close()
    print(f"Linker {name} created")

def install(name, directory, prompt=True):
    """
    Installs The Linker Or Zip File
    """
    try:
        fh = open(f"{name}.linker",'r')
        reader = csv.reader(fh)
        info = []
        try:
            for line in reader:
                temp = []
                temp.append(line[0])
                temp.append(line[1])
                info.append(temp)
        except:
            raise Exceptions.LinkerReadError("Error Reading Linker File. Is It Properly Formatted?")

        if os.path.exists(info[0][1]):
            if prompt == True:
                check = input(f"The Interface {info[0][1]} Already Exists. Do You Want To Overwrite It? (Y/N): ")
                if check == "Y":
                    os.system(f"rmdir /Q /S {info[0][1]}")
                    os.system(f'git clone {info[2][1]} "{directory}/{info[0][1]}"')
                elif check == "N":
                    return
                else:
                    pass
        
        else:
            os.system(f'git clone {info[2][1]} "{directory}/{info[0][1]}"')

        fh = open(f"{info[0][1]}/.linker",'w')
        fh.write(f"Name,{info[0][1]}\n")
        fh.write(f"Version,{info[1][1]}\n")
        fh.write(f"Repository,{info[2][1]}\n")
        fh.write(f"Author,{info[3][1]}")
        fh.close()
        print(f"'{info[0][1]}' Created")

    except FileNotFoundError:
        try:
            with zipfile.ZipFile(f"{name}.zip", 'r') as zip_ref:
                zip_ref.extractall(str(os.path.dirname(name))+"interfaces")
            print("Interface Created")
        except:
            raise Exceptions.LinkerReadError("Could Not Find Linker File")