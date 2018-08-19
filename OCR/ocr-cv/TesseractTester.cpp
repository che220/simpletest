#include <string>
#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>
#include <opencv2/opencv.hpp>
#include "TesseractTester.h"

using std::string;

TesseractTester::TesseractTester() {
	// TODO Auto-generated constructor stub

}

TesseractTester::~TesseractTester() {
	// TODO Auto-generated destructor stub
}

int main1(int argc, char* argv[])
{
    string outText;
    string imPath = argv[1];

    // Create Tesseract object
    tesseract::TessBaseAPI *ocr = new tesseract::TessBaseAPI();

    // Initialize tesseract to use English (eng) and the LSTM OCR engine.
    ocr->Init(NULL, "eng", tesseract::OEM_LSTM_ONLY);

    // Set Page segmentation mode to PSM_AUTO (3)
    ocr->SetPageSegMode(tesseract::PSM_AUTO);

    // Open input image using OpenCV
    Mat im = cv::imread(imPath, IMREAD_COLOR);

    // Set image data
    ocr->SetImage(im.data, im.cols, im.rows, 3, im.step);

    // Run Tesseract OCR on image
    outText = string(ocr->GetUTF8Text());

    // print recognized text
    cout << outText << endl; // Destroy used object and release memory ocr->End();

    return EXIT_SUCCESS;
}
