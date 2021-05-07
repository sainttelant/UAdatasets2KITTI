#!/usr/bin/env python
# coding: utf-8
# coding:UTF-8
"""
里面用到的主要是os和字符串的截取，可以参考
"""

import os


def aquireDetails(path):
    allthings = os.listdir(path)
    return allthings


def judgeFiles(path, allthing):
    filenames = []
    for files in allthing:
        abspath = os.path.join(path, files)
        print("abspath:",abspath)
        if os.path.isdir(abspath):
            print("it is a folder,ingore it")
        if os.path.isfile(abspath):

            """
            reference
            str='https://www.guahao.com/department/125809921947822000?isStd='
            print(str.split('department/')[1].split('?')[0])
            print(str.replace('department/','').replace("https://www.guahao.com/",''))
            """
            tailname = abspath.split(".")[1]
            # \\代表单斜杠匹配
            prename = abspath.split(".")[0].split("/")[-1]
            #prename = abspath.split(".")[0]
            print("prename:",prename)
            if tailname == "jpg" or tailname == "jpeg" or tailname == "png":
                filenames.append(prename)
    return filenames

def generatefilelist(path, allthing):
    filenames = []
    for files in allthing:
        abspath = os.path.join(path, files)
        # print("abspath:",abspath)
        if os.path.isdir(abspath):
            print("it is a folder,ingore it")
        if os.path.isfile(abspath):
            """
            reference
            str='https://www.guahao.com/department/125809921947822000?isStd='
            print(str.split('department/')[1].split('?')[0])
            print(str.replace('department/','').replace("https://www.guahao.com/",''))
            """
            tailname = abspath.split(".")[1]
            # \\代表单斜杠匹配
            print("tailname:",tailname)
            #prename = abspath.split(".")[0].split("\\")[1]
            prename = abspath.split(".")[0].split("/")[1]
            print("prename:",prename)
            hang = "file"+"\t"+"'"+prename+"."+tailname+"'"
            filenames.append(hang)
    return filenames

def rename(path):
    f = os.listdir(path)
    n = 0
    for i in f:
        # 设置旧文件名（就是路径+文件名）
        oldname = path + f[n]
        # 设置新文件名
        newname = path + 'video' + str(n + 1) + '.mp4'
        # 用os模块中的rename方法对文件改名
        os.rename(oldname, newname)
        print(oldname, '======>', newname)
        n += 1
    return True


def saveFileNameIntotxt(file, list_thing):
    for filename in list_thing:
        #换行写入 \t空格
        file.write(filename + "\n")


if __name__ == "__main__":
    # print("it begins to get libfilenames")
    # print("it opened a txt files to store libfile names")
    #currentPath = os.getcwd()
    print("生成train.txt，输入1， 生成filelist.txt，输入2")
    print("生成train.txt，输入1， 生成filelist.txt，输入2")
    print("生成train.txt，输入1， 生成filelist.txt，输入2")
    interface = input("请输入你的选择：")
    if interface == "1":
        print("开始生成train.txt")
        path = "KITTIDATA/training/image_2"
        k = aquireDetails(path)
        a = judgeFiles(path, k)
        """
        r 只能读 （带r的文件必须先存在）
        r+ 可读可写 不会创建不存在的文件 从顶部开始写 会覆盖之前此位置的内容 
        w+ 可读可写 如果文件存在 则覆盖整个文件不存在则创建  //要close 之后才算完成写入
        w 只能写 覆盖整个文件 不存在则创建 
        a 只能写 从文件底部添加内容 不存在则创建 
        a+ 可读可写 从文件顶部读取内容 从文件底部添加内容 不存在则创建
        """
        with open("KITTIDATA/train.txt", "w+") as f:
            saveFileNameIntotxt(f, a)
        f.close()
        print("finish aquire jpeg files'names")
    elif interface =="2":
        print("开始规整视频")
        recordPath = "record/"
        flag = rename(recordPath)
        #flag = True
        if flag == True:
            detail = aquireDetails(recordPath)
            hang  = generatefilelist(recordPath,detail)
            with open("record/filelist.txt","w+") as file:
                saveFileNameIntotxt(file,hang)
            file.close()
            print("finish filelist.txt generate!!!")







