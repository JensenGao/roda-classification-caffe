#include<iostream>
#include<opencv2/opencv.hpp>
using namespace std;
int main()
{
	int frameCount = 0;//视频帧数计数
	char imageName[1000000];//图像名
	int i = 0, j = 0;//保存图像命名用
	cv::Rect ROIRect;//抠图的ROI
	cv::Mat frame;//原视频帧
	cv::Mat ROIImage;//抠图后的
	int ROIWidth = 150;//抠图后的大小
	int ROIHeight = 150;
	int gap = 100;//每隔gap个像素进行采集

	cv::VideoCapture videoCapture;
	videoCapture.open("C:/Users/lenovo/Desktop/Road Classification/[]Bayes Technology's Video/DJI_0019.MOV");
	if (!videoCapture.isOpened())
	{
		cout << "Failed to open the video!\n";
		exit(1);
	}
	
	while (1)
	{
		videoCapture.read(frame);
		if (frame.empty())
		{
			cout << "Failed to read video!\n" ;
			exit(1);//没读到帧时程序结束

		}
		cout << "Video's  width:" << frame.cols << endl << 
		"Video's height:" << frame.rows << endl;//图像的宽和高
		
		int resultHeight = frame.rows - ROIHeight + 1;//行的循环
		int resultWidth = frame.cols - ROIWidth + 1;//列的循环

		if (frameCount%60==0)//每隔30帧时间才抠图(时间短的视频每30帧抠图;时间长的每60帧抠图)
		{
			for (int row = 0; row < resultHeight; row += gap)
			{
				for (int col = 0; col < resultWidth; col += gap)
				{
					ROIRect = cv::Rect(col, row, ROIWidth, ROIHeight);//用来抠图的RIO的大小
					ROIImage = frame(ROIRect);
					//cv::rectangle(frame,ROIRect,cv::Scalar(100,100,100));
					sprintf_s(imageName, "%s%d%s%d%s%d%s",
						"C:/Users/lenovo/Desktop/raod/",
						frameCount, "_", i, "_",j++, ".jpg");//保存的图片名,命名规则：帧_图像行_图像列
					//注意上面的命名，名字相同覆盖的问题
					cv::imwrite(imageName, ROIImage);
				}
				i++;

			}
		}
		
		cv::namedWindow("VideoCut");//显示图像
		cv::imshow("VideoCut", frame);

		frameCount++;
		cout << frameCount << endl << endl;//帧数

		char c = (char)cv::waitKey(33);
		if (c == (char)27 || c == 'q' || c == 'Q')
			break;
	}

	return 0;
}
