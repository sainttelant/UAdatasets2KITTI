# modify_annotations_txt.py
import glob
import string
import os

txt_list = glob.glob('KITTIDATA/training/label_2/*.txt') # 存储Labels文件夹所有txt文件路径
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
    print("想要去除txt的空格输入1，想要删除空的txt文件输入2")
    print("想要去除txt的空格输入1，想要删除空的txt文件输入2")
    print("想要去除txt的空格输入1，想要删除空的txt文件输入2")
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
                        if labeldata[0] =="Car":
                            labeldata[0] = labeldata[0].replace(labeldata[0],'car')
                        if labeldata[0] == 'Pedestrian' or labeldata[0] == "pedestrian": # 合并行人类
                            labeldata[0] = labeldata[0].replace(labeldata[0],'person')
                        if labeldata[0] == 'Cyclist' or labeldata[0]=="cyclist" : # 忽略Dontcare类
                            labeldata[0] = labeldata[0].replace(labeldata[0],'bicycle')
                        if labeldata[0] == 'Misc': # 忽略Misc类
                            continue
                        if labeldata[0] == '':
                            continue
                        else:
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
    else:
        with open ("emptyfile.txt", "w+") as file:
            for item in txt_list:
                size = os.path.getsize(item)
                if size == 0:
                    xieru = "文件是空的："+item
                    print('文件是空的：%s'%(item))
                    file.write(xieru+"\n")
                    os.remove(item)
        file.close()



