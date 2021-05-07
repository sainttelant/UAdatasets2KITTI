# Visual Object Dataset converter

Converts between object dataset formats. Requires Python 3.6.

Run  step 1 to 3 

and then 
python vod_converter/main.py --from voc --from-path VOCDATA --to kitti --to-path KITTIDATA



#自有数据集操作步骤
第一步: 先把离散的mp4数据放到record下面,运行Getimgname,输入2,生成filelist.txt

第二步: 在record目录下,运行 ffmpeg -f concat -i filelist.txt -c copy out.mp4,生成一个out.mp4文件

第三步: 把out.mp4切成图片,后面日期可以变化
ffmpeg -i out.mp4 -r 1 20210507%7d.jpg 

第四步: 将all images 拷贝到另一个工程Zhangw/data/images
运行python3 detect.py,生成label文件

第五步: 将所有的yolo标签转化为kitti格式

第六步:转好之后,再回炉到这个工程里面来,转化成voc格式,这一步为了校验数据标注情况.也可以直接省略
先可以执行changekittlabel
注意,这一步要先生成train.txt,调用GetImgName

第七步: 人工审阅没问题之后,再将原有KITTI文件删除,重新运行脚本生成KITTI,从voc转过去

