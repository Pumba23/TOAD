import pymrio

def mrio_load():

    antwort = input("Using TOAD first time? (yes/no): ")
    input_path = input("Type (or copy) in the path to your current project folder (e.g. C:/Users/Daisy/PycharmProjects/Project_X) ")  # input individual path

    if antwort.lower() == "yes":

        exio3_folder = input_path+'\EXIO3_IXI'
        print("Download Exiobase3. It will take some time... you may get a tee :) ...")
        exio_downloadlog = pymrio.download_exiobase3(storage_folder=exio3_folder, system="ixi") # download of current version ixi

        print(exio_downloadlog)


    elif antwort.lower() == "no":
        print("Okay. Welcome to TOAD :)")

    else:
        print("irregular input. restart")
        exit()  # terminate TOAD

    return input_path