import fernet as fr
import os
import sys

def clear():
    if os.name == "posix":
        os.system("clear")
    elif os.name in ("ce","nt","dos"):
        os.system("cls")

def find_key(kpath):
    if os.path.isdir(kpath):
        files = os.listdir(kpath)
        for key in files:
            nom, formato = os.path.splitext(key)
            if formato == '.key':
                return key
    elif os.path.isfile(kpath):
        nom, formato = os.path.splitext(key)
        if formato == '.key':
            return key
    else:
        print("Key does not found")
        exit()
def usage():
    print('''
            1.- Create a key to encrypt the informacion
            2.- Encrypt information
            3.- Decrypt information
            Enter any other key to exit
            ''')
def main():
    usage()
    opt = input()

    if opt == '1':
        print('''The key create will be joined with the encrypt password 
                if one of them is not the same, decrypt will not allowed''') 

        fr.key_generation_fernet()
        

    elif opt == '2':
        print('''This password will be used to encrypt files
        if the key or password are not the same the files 
        will not be able to decrypt''')
        password = input('Password: ')
        
        rootDir = input('Files Path: ')
        dirKey = input('Key Path: ')
        find_key(dirKey)
        if not os.path.isdir(rootDir):
            name_file = os.path.basename(rootDir)
            nom, formato = os.path.splitext(name_file)
            if '.ini' != formato:
                if formato != '.py' and formato != '.key' and formato != '.enc':
                    fr.encrypt_file_fernet(rootDir, kname = fr.use_key(find_key(dirKey), password))
                    os.rename(rootDir, rootDir + '.enc')
        else:
            for dirName, subdirList, fileList in os.walk(rootDir):
                for fname in fileList:
                    fname = os.path.join(dirName, fname)
                    nom , formato = os.path.splitext(fname)
                    if '.ini' != formato:
                        if formato != '.py' and formato != '.key' and formato != '.enc':
                            fr.encrypt_file_fernet(fname, kname = fr.use_key(find_key(dirKey), password))
                            os.rename(fname, fname + '.enc')
                            clear()
                            usage()
                            print(fname)
                            

    elif opt == '3':
        print('''The same password which was used to encrypt the files''')
        password = input('Password: ')
        rootDir = input('Files Path: ')
        dirKey = input('Key Path: ')
        find_key(dirKey)

        if not os.path.isdir(rootDir):
            name_file = os.path.basename(rootDir)
            nom, formato = os.path.splitext(name_file)

            if '.ini' != formato:
                if formato == '.enc':
                    try:
                        fr.decrypt_file_fernet(rootDir, kname = fr.use_key(find_key(dirKey), password))
                    except:
                        print("The password and/or the key are not correct")
                        exit()
                    os.rename(rootDir, rootDir[:-4])
        else:
            for dirName, subdirList, fileList in os.walk(rootDir):
                for fname in fileList:
                    fname = os.path.join(dirName, fname)
                    nom , formato = os.path.splitext(fname)
                    if '.ini' != formato:
                        if formato == '.enc':
                            try:
                                fr.decrypt_file_fernet(fname, kname = fr.use_key(find_key(dirKey), password))
                            except:
                                print("The password and/or the key are not correct")
                                exit()
                        os.rename(fname, fname[:-4])
                        clear()
                        usage()
                        print(fname)
    else:
        exit()

main()

