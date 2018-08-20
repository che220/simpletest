#include <iostream>
#include <opencv2/opencv.hpp>

using std::cout;
using std::cerr;
using std::endl;
using std::string;

using namespace cv;

int main(int argc, char **argv) {
	string path = "/Users/hwang7/tmp/simpletest/OCR/irs1099misc.png";
	cout << "load image from " << path << endl;

	Mat image = imread(path, IMREAD_UNCHANGED);
	if (!image.data) {
		printf("No image data \n");
		return -1;
	}
	namedWindow("Display Image", WINDOW_AUTOSIZE);
	imshow("Display Image", image);
	waitKey(0);

	return 0;
}
