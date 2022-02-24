#import unreal
import os
print("Start web client")
path = os.getcwd()
print(path)
newpath = os.path.join(path, "BatFiles")
print(newpath)
os.chdir(newpath)
path = os.getcwd()
print(path)
os.system("start_client.bat")