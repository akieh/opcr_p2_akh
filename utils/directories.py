import os


def create_directories():
    print("Creation des dossiers 'imagesbooks' et 'csvbooks'")
    if not os.path.exists("imagesbooks"):
        os.mkdir("imagesbooks")
        print("Le repetoire 'imagesbooks' a été créé.")
    else:
        print("Le reportoire 'imagesbooks' existe déjà.")
    if not os.path.exists("csvbooks"):
        os.mkdir("csvbooks")
        print("Le repetoire 'csvbooks' a été créé.")
    else:
        print("Le reportoire 'csvbooks' existe déjà.")

