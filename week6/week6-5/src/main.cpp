//
// Created by chae on 23. 4. 21.
//
#include <iostream>
#include "opencv2/opencv.hpp"

using namespace std;

cv::Mat histogram_stretching_mod(const cv::Mat& src)
{
    cv::Mat dst;
    int hist[256] = {0, };
    // Todo: src 전체를 스캔하면서 히스토그램을 hist에 저장하세요.
    int img_height = int(src.rows);
    int img_width = int(src.cols);
    int img_ratio = img_height * img_width * 0.01;

    for (int y = 0; y < img_height; y++) {
        for (int x = 0; x < img_width; x++) {
            hist[src.at<uchar>(y, x)]++;
        }
    }


    /* 동영상 / 카메라
    int w = cv::cvRound(cap.get(cv::CAP_PROP_FRAME_WIDTH));
    int h = cv::cvRound(cap.get(cv::CAP_PROP_FRAME_HEIGHT));
    */

    int gmin = 255;
    int gmax = 255;
    int ratio = int(src.cols * src.rows * 0.01);

    for (int i = 0, s = 0; i < 255; i++){
        s += hist[i];
        if (s >= img_ratio){
            gmin = i;
            break;
        }
        // Todo : 히스토그램 누적 합 s가 ratio 보다 커지면,
        // Todo : 해당 인덱스를 gmin에 저장하고 반복문을 빠져나옵니다.
    }

    for (int i = 255, s = 0; i >=0; i--){
        s += hist[i];
        if (s >= img_ratio){
            gmax = i;
            break;
        }
        // Todo : 히스토그램 누적 합 s 가 ratio보다 커지면,
        // Todo : 해당 인덱스를 gmax에 저장하고 반복문을 빠져나옵니다.
    }
    dst = (src - gmin) * 255 / (gmax - gmin);
    return dst;
    // Todo : 히스토그램 스트레칭을 수행하고, 그 결과를 dst에 저장합니다.
}

cv::Mat calcGrayHist(const cv::Mat& img)
{
    CV_Assert(img.type() == CV_8U);

    cv::Mat hist;
    int channels[] = { 0 };
    int dims = 1;
    const int histSize[] = { 256 };
    float graylevel[] = { 0, 256 };
    const float* ranges[] = { graylevel };

    calcHist(&img, 1, channels, cv::noArray(), hist, dims, histSize, ranges, true);

    return hist;
}

cv::Mat getGrayHistImage(const cv::Mat& hist)
{
    CV_Assert(!hist.empty());
    CV_Assert(hist.type() == CV_32F);

    double histMax = 0.;
    minMaxLoc(hist, 0, &histMax);

    cv::Mat imgHist(100, 256, CV_8UC1, cv::Scalar(255));
    for (int i = 0; i < 256; i++) {
        line(imgHist, cv::Point(i, 100),
             cv::Point(i, 100 - cvRound(hist.at<float>(i) * 100 / histMax)), cv::Scalar(0));
    }

    return imgHist;
}

int main()
{
    cv::Mat src = imread("../resources/lenna.bmp", cv::IMREAD_GRAYSCALE);

    if (src.empty()) {
        cerr << "Image load failed!" << endl;
        return -1;
    }

    cv::Mat dst = histogram_stretching_mod(src);



    cv::imshow("src", src);
    cv::imshow("dst", dst);
    cv::imshow("hist_src", getGrayHistImage(calcGrayHist(src)));
    cv::imshow("hist_dst", getGrayHistImage(calcGrayHist(dst)));

    cv::waitKey();
}
