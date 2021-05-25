# Visual Object Dataset converter

Converts between object dataset formats. Requires Python 3.6.

Run  step 1 to 3 

and then 
python vod_converter/main.py --from voc --from-path VOCDATA --to kitti --to-path KITTIDATA



#自有数据集操作步骤
第一步: 先把离散的mp4数据放到record下面,运行Getimgname,输入2,生成filelist.txt

第二步: 在record目录下,运行 ffmpeg -f concat -i filelist.txt -c copy out.mp4,生成一个out.mp4文件

第三步: 把out.mp4切成图片,后面日期记得要改一下！！！！！！
！！！！！！！！！！！！！
！！！！！！！！！！！！！可以变化
ffmpeg -i out.mp4 -r 1 20210524%7d.jpg 

第四步: 将all images 拷贝到另一个工程Zhangw/yolov5-5.0/data/images
运行python3 resizepic.py 将图片统一成960*544
运行python3 detect.py,生成label文件
再运行convert2kitti,生成kitti格式label

第五步: 将所有的yolo标签转化为kitti格式

第六步:转好之后,再回炉到这个工程里面来,转化成voc格式,这一步为了校验数据标注情况.也可以直接省略

6.1\这一步要先生成train.txt,调用GetImgName
6.2\先可以执行changekittlabel,记住只运行输入1,后两个不运行
6.3\ python3 vod_converter/main.py --from kitti --from-path KITTIDATA --to voc --to-path VOCDATA


第七步: 人工审阅没问题之后,再将原有KITTI文件删除,重新运行脚本生成KITTI,从voc转过去
python3 vod_converter/main.py --from voc --from-path VOCDATA --to kitti --to-path KITTIDATA

第八步: 将准备好的数据再拷贝到tlt工程目录下面,好了之后再运行changekitti脚本,过滤选项2和3,至此全部完毕.

