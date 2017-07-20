/*将文件夹中的文件名保存到一个txt文件中主要用到struct _finddata_t结构体（io.h头文件中），
该结构体详细介绍：http://blog.sina.com.cn/s/blog_9fe22ab701013yfo.html */

#include<iostream>
#include<vector>
#include<fstream>
#include<string>
#include<io.h>
using namespace std;

/*先用_findfirst查找第一个文件，若成功则用返回的句柄调用_findnext函数查找其他的文件，
当查找完毕后用，用_findclose函数结束查找。*/
void getJustCurrentFile(string path, vector<string>& files)//读取当前文件夹下的文件名
{
	//文件句柄 
	long  hFile = 0;
	//文件信息 
	struct _finddata_t fileinfo;//用来存储文件各种信息的结构体->io.h头文件中
	string p;
	if ((hFile = _findfirst(p.assign(path).append("\\*").c_str(), &fileinfo)) != -1)
		//_findfirst查找第一个文件，查找成功则执行if语句
	{
		do
		{
			if ((fileinfo.attrib & _A_SUBDIR))//_文件属性，A_SUBDIR表示文件夹
			{
				cout << "It's a directory!\n";
			}
			else
			{
				files.push_back(fileinfo.name);//保存文件名
				//files.push_back(p.assign(path).append("\\").append(fileinfo.name) ); //这是保存路径+文件名
			}
		} 
		while (_findnext(hFile, &fileinfo) == 0);//查找下一个文件，存在则继续执行
		_findclose(hFile);//结束查找
	}
}

int main()
{
	/*主程序需要修改的地方：
	1、txtFileName-表示训练/测试/验证数据
	2、filePath-文件夹的路径
	3、标签0或1*/
	string filePath = "C:/Users/lenovo/Desktop/道路分类/[]Bayes Technology's Video/processed data/val/road";//文件路径（图像根目录）
	vector<string> imageName;//保存文件名
	string txtFileName = "C:/Users/lenovo/Desktop/道路分类/[]Bayes Technology's Video/processed data/val/val_set1.txt";
	getJustCurrentFile(filePath, imageName);
	ofstream fout(txtFileName);
	int size = imageName.size();//文件数
	cout << size << endl;
	for (int i = 0; i<size; i++)
	{
		fout << imageName[i] ;//文件名
		fout << " " << 1 << endl;//标签；对于不同的数据集相应地修改标签
	}
	fout.close();

	return 0;
}
