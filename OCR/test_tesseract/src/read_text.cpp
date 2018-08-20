#include <string>
#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>
#include <opencv2/opencv.hpp>

using std::string;
using std::cout;
using std::cerr;
using std::endl;

using namespace tesseract;
using namespace cv;

int main(int argc, char* argv[])
{
    string outText;
	string imPath = "/Users/hwang7/tmp/simpletest/OCR/irs1099misc.png";
	cout << "load image from " << imPath << endl;

    // Create Tesseract object
    tesseract::TessBaseAPI ocr;

    // Initialize tesseract to use English (eng) and the LSTM OCR engine.
    ocr.Init(NULL, "eng", tesseract::OEM_TESSERACT_ONLY); // in 4.0, LSTM model can be selected.

    // Set Page segmentation mode to PSM_AUTO (3)
    ocr.SetPageSegMode(tesseract::PSM_AUTO);

    // Open input image using OpenCV
    Mat im = cv::imread(imPath, IMREAD_COLOR);

    // Set image data
    ocr.SetImage(im.data, im.cols, im.rows, 3, im.step);

    // Run Tesseract OCR on image
    outText = string(ocr.GetUTF8Text());

    // print recognized text
    cout << outText << endl;

    // Destroy used object and release memory
    ocr.End();

    return EXIT_SUCCESS;
}
