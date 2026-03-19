from pathlib import Path
import shutil
p = Path('.')

def Create_folder():
            try:
                Show_folder()
                fileName = input("\nEnter Path with folder Name:- ")

                dic = Path(fileName)

                dic.mkdir()

                if dic.exists():
                    print(f"\nFolder Succesfully '{dic}' Created")
            except Exception as err:
                print(f"Error: {err}")

def Rename_folder():
    try:
        Show_folder()
        fileName = input("\nEnter Path with folder Name:- ")
        newFileName = input("\nEnter New Name:- ")
        dic = Path(fileName)
        dic.rename(newFileName)
        print(f"Rename Succesfully from Folder '{dic}' to '{newFileName}'")
    except Exception as err:
        print(f"Error: {err}")

def Show_folder():
    print(f"\nAll Folders In Current working directory:- ")
    for i in p.iterdir():
        if i.exists() and i.is_dir():
            print(f"• {i}")
        else:
            print("Oops! There is no such Folders")

def Remove_folder():
    try:
        Show_folder()
        fileName = input("\nEnter Path with folder Name:- ")
        dic = Path(fileName)
        if dic.exists() and dic.is_dir():
            shutil.rmtree(dic)
            print(f"{dic} is Removed Succesfully")
    except Exception as err:
        print(f"Error: {err}")

    ...

def Create_file():
        try:
            Show_files()
            fileName = input("\n File Name With Extension:- ")
            dic = Path(fileName)
            dic.touch()
            if dic.exists():
                print(f"\nFile Succesfully '{dic}' Created")
        except Exception as err:
            print(f"Error: {err}")

def Show_files():
    print(f"\nList Of Directroy Or file Available In Current working directory:- ")
    files = list(p.rglob('*'))
    for i,v in enumerate(files):
        if v.is_file():
            print(f"\n• {i+1}) {v}")

def Rename_file():
    try:
        Show_files()
        fileName = input("\nFile Name With Extension:- ")
        newFileName = input("\n Enter New Name:- ")
        dic = Path(fileName)
        dic.rename(newFileName)
    except Exception as err:
        print(f"Error: {err}")
    ...

def Remove_file():
    try:
        Show_files()
        fileName = input("\nFile Name With Extension:- ")
        dic = Path(fileName)
        if dic.exists() and dic.is_file():
            dic.unlink()
            print(f"{dic} is Removed Succesfully")
    except Exception as err:
        print(f"Error: {err}")
    ...

def Write_file():
    try:
        Show_files()
        fileName = input("\nFile Name With Extension:- ")
        dic = Path(fileName)
        with open(dic, 'w') as f:
            f.write(input("\nEnter Data:- "))
        print(f"Data Written To {dic} Succesfully")
    except Exception as err:
        print(f"Error: {err}")

def Read_file():
    try:
        Show_files()
        fileName = input("\nFile Name With Extension:- ")
        dic = Path(fileName)
        with open(dic, 'r') as f:
            print(f.read())
    except Exception as err:
        print(f"Error: {err}")

def Append_file():
    try:
        Show_files()
        fileName = input("\nFile Name With Extension:- ")
        dic = Path(fileName)
        with open(dic, 'a') as f:
            data = input("\nEnter Data:- ")
            f.write(f" {data}")
        print(f"Data Appended To {dic} Succesfully")
    except Exception as err:
        print(f"Error: {err}")
    ...


while True:
    opt = int(input("\nFolder Operation\n1. Create Folder\n2. Show Folders\n3. Rename Folder\n4. Delete Folder\n\nFile Operation \n5. Create File\n6. Show Files\n7. Rename File\n8. Remove File\n9. Write File\n10. Read File\n11. Append To File\n12. exit():- "))

    if not 0 < opt <=12:
        print("\nInvalid Input")

    match  opt:
        case 1:
            Create_folder()
        case 2:
            Show_folder()
        case 3:
            Rename_folder()
        case 4:
            Remove_folder()
        case 5:
            Create_file()
        case 6:
            Show_files()
        case 7:
            Rename_file()
        case 8:
            Remove_file()
        case 9:
            Write_file()
        case 10:
            Read_file()
        case 11:
            Append_file()
        case 12:
            exit()

