
import os
import random
import shutil

#xml 转好后的路径地址
XmlPath=r'Annotations'
#原图片地址
pictureBasePath=r"../../DataSetTest/RawIMg"
#包存的图片地址
saveBasePath=r"JPEGImages"

total_xml = os.listdir(XmlPath)
num=len(total_xml)
list=range(num)
if os.path.exists(saveBasePath)==False: #鍒ゆ柇鏂囦欢澶规槸鍚﹀瓨鍦?
     os.makedirs(saveBasePath)


for xml in total_xml:
    xml_temp=xml.split("__")
    folder=xml_temp[0]
    filename=xml_temp[1].split(".")[0]+".jpg"
    # print(folder)
    # print(filename)
    temp_pictureBasePath=os.path.join(pictureBasePath,folder)
    filePath=os.path.join(temp_pictureBasePath,filename)
    # print(filePath)
    newfile=xml.split(".")[0]+".jpg"
    newfile_path=os.path.join(saveBasePath,newfile)
    print(newfile_path)
    shutil.copyfile(filePath, newfile_path)
print("xml file total number",num)


