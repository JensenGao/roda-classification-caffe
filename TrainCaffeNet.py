# -*- coding: utf-8 -*-

'''
这个程序是用ImageData层训练CaffeNet
'''


# -*- coding: utf-8 -*-

import caffe
from caffe import layers as L,params as P,proto,to_proto
#设定文件的保存路径
root='C:/Users/Jensen Gao/Desktop/'                           #图像所在的根目录
train_list=root+'mnist/train/train.txt'     #训练图片列表
test_list=root+'mnist/test/test.txt'        #测试图片列表
train_proto=root+'mnist/train.prototxt'     #训练配置文件
test_proto=root+'mnist/test.prototxt'       #测试配置文件
solver_proto=root+'mnist/solver.prototxt'   #参数文件

def conv_relu(bottom,ks,nout,stride=1,pad=0,group=1,weight_filler=dict(type='xavier')):
    conv=L.Convolution(bottom,kernel_size=ks,stride=stride,
                       num_output=nout,pad=pad,group=group,weight_filler=weight_filler)
    return conv,L.ReLU(conv,in_place=True)

def fc_relu(bottom,nout,weight_filler=dict(type='xavier')):
    fc=L.InnerProduct(bottom,num_output=nout,weight_filler=weight_filler)
    return fc,L.ReLU(fc,in_place=True)

def max_pool(bottom,ks,stride=1):
    return L.Pooling(bottom,pool=P.Pooling.MAX,kernel_size=ks,stride=stride)

#编写一个函数，生成配置文件prototxt
def Lenet(img_list,batch_size,include_acc=False):
    #第一层，数据输入层，以ImageData格式输入
    data, label = L.ImageData(source=img_list, batch_size=batch_size, ntop=2,root_folder=root,
        transform_param=dict(scale= 0.00390625))
    #第二层：卷积层
    conv1,relu1=conv_relu(data,11, 96, stride=4,pad=0)
    #池化层
    pool1=max_pool(relu1, 3, stride=2)
    norm1=L.LRN(pool1,local_size=5,alpha=1e-4,beta=0.75)
    
    #卷积层
    conv2,relu2=conv_relu(norm1, 5, 256, stride=4,pad=2,group=2)
    #池化层
    pool2=max_pool(relu2, 3, stride=2)
    norm2=L.LRN(pool2,local_size=5,alpha=1e-4,beta=0.75)
    
    conv3,relu3=conv_relu(norm2, 3, 384, pad=1)
    conv4,relu4=conv_relu(relu3, 3, 384, pad=1,group=2)
    conv5,relu5=conv_relu(relu4, 3, 256, pad=1,group=2)
    
    pool5 = max_pool(relu5, 3, stride=2)
    fc6, relu6 = fc_relu(pool5, 4096)
    drop6 = L.Dropout(relu6, in_place=True)
    fc7, relu7 = fc_relu(drop6, 4096)
    drop7 = L.Dropout(relu7, in_place=True)
    
    #全连接层
    fc8 = L.InnerProduct(drop7, num_output=10,weight_filler=dict(type='xavier'))
    #softmax层
    loss = L.SoftmaxWithLoss(fc8, label)
    
    if include_acc:             # test阶段需要有accuracy层
        acc = L.Accuracy(fc8, label)
        return to_proto(loss, acc)
    else:
        return to_proto(loss)
    
def write_net():
    #写入train.prototxt
    with open(train_proto, 'w') as f:
        f.write(str(Lenet(train_list,batch_size=64)))

    #写入test.prototxt    
    with open(test_proto, 'w') as f:
        f.write(str(Lenet(test_list,batch_size=100, include_acc=True)))

#编写一个函数，生成参数文件
def gen_solver(solver_file,train_net,test_net):
    s=proto.caffe_pb2.SolverParameter()
    s.train_net =train_net
    s.test_net.append(test_net)
    s.test_interval = 1000    #60000/64，测试间隔参数：训练完一次所有的图片，进行一次测试  
    s.test_iter.append(1000)  #50000/100 测试迭代次数，需要迭代500次，才完成一次所有数据的测试
    s.max_iter = 100000       #10 epochs , 938*10，最大训练次数
    s.base_lr = 0.01    #基础学习率
    s.momentum = 0.9    #动量
    s.weight_decay = 5e-4  #权值衰减项
    s.lr_policy = 'step'   #学习率变化规则
    s.stepsize=10000         #学习率变化频率
    s.gamma = 0.1          #学习率变化指数
    s.display = 20         #屏幕显示间隔
    s.snapshot = 10000       #保存caffemodel的间隔
    s.snapshot_prefix = root+'mnist/'   #caffemodel前缀
    s.type ='SGD'         #优化算法
    s.solver_mode = proto.caffe_pb2.SolverParameter.GPU    #加速
    #写入solver.prototxt
    with open(solver_file, 'w') as f:
        f.write(str(s))
  
#开始训练
def training(solver_proto):
    caffe.set_device(0)
    caffe.set_mode_gpu()
    #caffe.set_mode_cpu()
    solver = caffe.SGDSolver(solver_proto)
    solver.solve()
#
if __name__ == '__main__':
    write_net()
    gen_solver(solver_proto,train_proto,test_proto) 
    print 'Start Train, Please Waiting......'
    training(solver_proto)
