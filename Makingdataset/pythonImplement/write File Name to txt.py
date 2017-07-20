# -*- coding: utf-8 -*-


import os

def ListFilesToTxt(dir,file,postFix):
     files = os.listdir(dir)#以列表的形式输出文件名
     print files
     print len(files)
     for name in files:
         fullname=os.path.join(dir,name)#路径+文件名（文件夹中是否还包含文件夹）
         if(os.path.isdir(fullname)):#当它是文件夹时，再写内层文件名
             ListFilesToTxt(fullname,file,postFix)
         elif name.endswith(postFix):
             file.write(name +' 1\n')#这里的 0/1 是类别标签

def writeToTxt():
   fileDir="C:/Users/lenovo/Desktop/Road Classification/[]Bayes Technology's Video/road Processed Data/train"#文件夹
   outTxtFile="C:/Users/lenovo/Desktop/raod/train_set.txt"#写入后的txt文件
   postFix = ".jpg"#处理后缀为.jpg的文件
   
   fileProcessed = open(outTxtFile,"w")
   if not file:
       print ("Cannot Open The File %s for Writing" % outTxtFile)

   ListFilesToTxt(fileDir,fileProcessed,postFix)
   
   fileProcessed.close()

writeToTxt()
