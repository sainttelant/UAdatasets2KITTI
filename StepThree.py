
import os
import random
import time

xmlfilepath=r'Annotations'
saveBasePath=r"ImageSets/Main/"

if os.path.exists(saveBasePath)==False: #鍒ゆ柇鏂囦欢澶规槸鍚﹀瓨鍦?
     os.makedirs(saveBasePath)

trainval_percent=0.8
train_percent=0.85
total_xml = os.listdir(xmlfilepath)
num=len(total_xml)
list=range(num)
tv=int(num*trainval_percent)
tr=int(tv*train_percent)
trainval= random.sample(list,tv)
train=random.sample(trainval,tr)

print("train and val size",tv)
print("traub suze",tr)
ftrainval = open(saveBasePath+"trainval.txt", 'w')
ftest = open(saveBasePath+"test.txt", 'w')
ftrain = open(saveBasePath+'train.txt', 'w')
fval = open(saveBasePath+'val.txt', 'w')
# Start time
start = time.time()
for i  in list:
    name=total_xml[i][:-4]+'\n'
    if i in trainval:
        ftrainval.write(name)
        if i in train:
            ftrain.write(name)
        else:
            fval.write(name)
    else:
        ftest.write(name)
# End time
end = time.time()
seconds=end-start
print( "Time taken : {0} seconds".format(seconds))

ftrainval.close()
ftrain.close()
fval.close()
ftest .close()
