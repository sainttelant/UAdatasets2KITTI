# modify_annotations_txt.py
import glob
import string
import os

txt_list = glob.glob('KITTIDATA/training/label_2/*.txt') # 存储Labels文件夹所有txt文件路径
images_list = glob.glob("KITTIDATA/training/image_2/*.jpg")
def show_category(txt_list):
    print("show_category!!")
    category_list= []
    for item in txt_list:
        try:
            with open(item) as tdf:
                for each_line in tdf:
                    if each_line == "":
                        continue
                    else:
                        #print("each_line:",each_line)
                        labeldata = each_line.strip().split(' ') # 去掉前后多余的字符并把其分开
                        if labeldata[0] == "":
                            continue
                        else:
                            category_list.append(labeldata[0]) # 只要第一个字段，即类别
        except IOError as ioerr:
            print('File error:'+str(ioerr))
    print(set(category_list)) # 输出集合

def merge(line):
    each_line=''
    for i in range(len(line)):
        if i!= (len(line)-1):
            each_line=each_line+line[i]+' '
        else:
            each_line=each_line+line[i] # 最后一条字段后面不加空格
    each_line=each_line+'\n'
    return (each_line)


if __name__ == "__main__":
    print("想要去除txt的空格输入1，想要删除空的txt文件输入2,删除对应的图片输入3")
    print("想要去除txt的空格输入1，想要删除空的txt文件输入2,删除对应的图片输入3")
    print("想要去除txt的空格输入1，想要删除空的txt文件输入2,删除对应的图片输入3")
    choose = input("输入你要做的动作：")
    if choose == "1":
        print('before modify categories are:\n')
        show_category(txt_list)
        for item in txt_list:
            print("txt_list:", item)
            new_txt=[]
            try:
                with open(item, 'r') as r_tdf:
                    for each_line in r_tdf:
                        labeldata = each_line.strip().split(' ')
                        if labeldata[0] == 'car':
                            labeldata[0] = labeldata[0].replace(labeldata[0],'Car')
                        if labeldata[0] == "bus":
                            labeldata[0]= labeldata[0].replace(labeldata[0],"Bus")
                        if labeldata[0] == "truck":
                            labeldata[0]= labeldata[0].replace(labeldata[0],"Truck")
                        if labeldata[0] == 'person' or labeldata[0]== "pedestrian" or labeldata[0]=="Pedestrian": # 合并行人类
                            labeldata[0] = labeldata[0].replace(labeldata[0],'Person')
                        if labeldata[0] == 'bicycle' or labeldata[0] == "cyclist" or labeldata[0] == "Cyclist" or  \
                            labeldata[0]== "motorcycle": # 忽略Dontcare类
                            labeldata[0] = labeldata[0].replace(labeldata[0],'Bicycle')
                        if labeldata[0] == 'road_sign' or labeldata[0] == "stop sign": # 忽略Misc类
                            labeldata[0] = labeldata[0].replace(labeldata[0],'Road_sign')
                        if labeldata[0] == '':
                            continue
                        if labeldata[0] in ['traffic','traffic light']:
                            continue
                        new_txt.append(merge(labeldata)) # 重新写入新的txt文件
                with open(item,'w+') as w_tdf: # w+是打开原文件将内容删除，另写新内容进去
                    for temp in new_txt:
                        print("temp:",temp)
                        if temp == None:
                            continue
                        else:
                            w_tdf.write(temp)
            except IOError as ioerr:
                print('File error:'+str(ioerr))

        print('\nafter modify categories are:\n')
        show_category(txt_list)
    elif choose == "2":
        with open ("emptyfile.txt", "w+") as file:
            for item in txt_list:
                size = os.path.getsize(item)
                if size == 0:
                    xieru = "文件是空的："+item
                    print('文件是空的：%s'%(item))
                    file.write(xieru+"\n")
                    os.remove(item)
        file.close()
    elif choose == "3":
        print("删除对应的图片")
        with open("emptyfile.txt") as file1:
            lines = file1.readlines()
            for line in lines:
                info = line.split('/')[1].split('.')[0]
                imagedetail = os.path.join("KITTIDATA/training/image_2",info+'.jpg')
                print("去掉对应的图片:",imagedetail)
                os.remove(imagedetail)
                
                


