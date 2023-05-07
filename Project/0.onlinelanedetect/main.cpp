#include <algorithm>  // std::find
#include <iostream>
#include <fstream>

#include "opencv2/opencv.hpp"
#include "opencv2/core/ocl.hpp"

struct MatPtr
{
    cv::Mat mat;
    uchar* ptr_value;
};


MatPtr RoiProcessImg(const cv::Mat& frame, const cv::Mat& mask, const int offset, const int gab);
cv::Mat FillMaskLidar(const cv::Mat& src);
std::pair<cv::Point2f, cv::Point2f> findPos(const int col_size, uchar* data_value);



int main()
{

    const int gab = 30;
    const int offset = 400;
    const cv::Scalar red(0, 0, 255), green(0, 255, 0),blue(255, 0, 0);

    cv::Mat frame;
    cv::Mat offset_img;
    cv::Mat lidar_mask(480, 640, CV_8UC1, cv::Scalar(0));
    cv::Mat lidar_mask_fillpoly = FillMaskLidar(lidar_mask);

    cv::VideoCapture cap;

    MatPtr result_img;
    cv::Point2f l_c, r_c;

    std::pair<int, int> temp;
    std::vector<std::pair<int, int>> csv_result;
    std::ofstream outfile;

    cap.open("../resources/Sub_project.avi");
    int f_number = 0;		//프레임 탐색을 위한 카운트 정수
    int frame_number_temp;
    bool paused = false;
    std::vector<int> frame_index;
    while (true) {

        cap >> frame;
        if (frame.empty()) break;
        ++f_number;
        frame_number_temp = cap.get(cv::CAP_PROP_POS_FRAMES);
        frame_index.push_back(frame_number_temp);
        result_img = RoiProcessImg(frame, lidar_mask_fillpoly, offset, gab);

        uchar* data = result_img.ptr_value;

        std::pair<cv::Point2f, cv::Point2f> points = findPos(result_img.mat.cols, data);
        l_c = points.first;
        r_c = points.second;

        if (frame_number_temp % 30 == 0) {
            temp = std::make_pair(l_c.x, r_c.x);
            csv_result.push_back(temp);
        }

        cv::Point pt1(0, 400), pt2(640, 400);
        cv::line(frame, pt1, pt2, red, 1, cv::LINE_AA); // LINE_4, LINE_8, LINE_AA 중 지정.
        cv::circle(frame,l_c ,  3 , cv::Scalar(0,255,0),cv::LINE_AA);
        cv::circle(frame, r_c,  3 , cv::Scalar(255,0,0),cv::LINE_AA);
        cv::imshow("frame", frame);
        cv::imshow("result_img", result_img.mat);

        std::stringstream ss, sss;
        ss << "../data/frame" << f_number << ".jpg";
        sss << "../data/thr" << f_number << ".jpg";
        std::string file_name1 = ss.str();
        std::string file_name2 = sss.str();

        char k = cv::waitKey(10 & 0xFF);
        if (k == 27) break;
        else if (k == 's'){
            cv::imwrite(file_name1, frame);
            cv::imwrite(file_name2, frame);

        }
        

    }

    //lpos rpos값을 저장할 csv파일 open
    outfile.open("result1.csv", std::ios::out);

    //csv파일에 저장
    for (int j = 0; j < csv_result.size(); j++)
    {
        outfile << csv_result[j].first <<","<< csv_result[j].second << std::endl;
    }
    outfile.close();


    cap.release();
    cv::destroyAllWindows();
}


MatPtr RoiProcessImg(const cv::Mat& frame, const cv::Mat& mask, const int offset, const int gab) {

    const int max_value = 255;
    const int thr_value = 70;
    cv::Mat gray;
    cv::Mat gray_roi, gray_mean_bright, gray_gaussian, gray_thresh;

    cv::Point roi_start(0, offset - gab);
    cv::Point roi_end(frame.cols,offset + gab);

    // BGR to Gray
    cv::cvtColor(frame, gray, cv::COLOR_BGR2GRAY);
    // lidar 영역 제외
    gray.setTo(max_value, mask);
    // Roi crop
    gray_roi = gray(cv::Rect(roi_start, roi_end));
    // mean brightness correction (speed up : LUT -> 평균 밝기가 계속 바뀌니깐)
    int m = mean(gray_roi)[0];
    gray_mean_bright = gray_roi - (m - max_value / 2);
    // GaussianBlur method
    cv::GaussianBlur(gray_mean_bright, gray_gaussian, cv::Size(), 2);
    // Binarization
    cv::threshold(gray_gaussian, gray_thresh, thr_value, max_value, cv::THRESH_BINARY_INV);

    MatPtr result;
    result.mat = gray_thresh;
    uchar* offset_value = gray_thresh.ptr<uchar>(gab);
    result.ptr_value = offset_value;

    return result;
}


cv::Mat FillMaskLidar(const cv::Mat& src){

    std::vector<cv::Point> pts(20);
    pts[0] = cv::Point(232, 479); pts[1] = cv::Point(228, 461); pts[2] = cv::Point(227, 448); pts[3] = cv::Point(230, 436); pts[4] = cv::Point(234, 429);
    pts[5] = cv::Point(240, 423); pts[6] = cv::Point(248, 415); pts[7] = cv::Point(258, 409); pts[8] = cv::Point(268, 405); pts[9] = cv::Point(282, 401);
    pts[10] = cv::Point(295, 397); pts[11] = cv::Point(314, 396); pts[12] = cv::Point(336, 397); pts[13] = cv::Point(355, 400); pts[14] = cv::Point(371, 404);
    pts[15] = cv::Point(390, 412); pts[16] = cv::Point(403, 423);  pts[17] = cv::Point(415, 443); pts[18] = cv::Point(417, 458); pts[19] = cv::Point(413, 479);
    fillPoly(src, pts, cv::Scalar(255, 0, 0));

    return src;

}

std::pair<cv::Point2f, cv::Point2f> findPos(const int col_size, uchar* data_value)
{
    cv::Mat src;
    cv::Mat labels;
    cv::Mat stats;
    cv::Mat centroids;

    std::vector<int> lpos_vec;
    std::vector<int> rpos_vec;
    std::vector<int> ptr_data_vector;

    cv::Point2f l_c, r_c;
    l_c.y = 400;
    r_c.y = 400;

    for (int i = 0; i < col_size; ++i) {
        int val = static_cast<int>(data_value[i]);
        ptr_data_vector.push_back(val);
    }

    src = cv::Mat(ptr_data_vector);
    src.convertTo(src,0);

    int num_labels = connectedComponentsWithStats(src, labels, stats, centroids);

    if (centroids.rows > 1) {
        for (int i = 1; i < centroids.rows; i++) {
            cv::Point2d temp_val = centroids.at<cv::Point2d>(i);
            int temp_int = temp_val.y;
            int temp_int_lr_check = temp_val.y - 320;
            if (temp_int_lr_check > 0) {
                rpos_vec.push_back(temp_int);
            } else {
                lpos_vec.push_back(temp_int);
            }
        }
        if (!lpos_vec.empty() && !rpos_vec.empty()) {
            auto lpos_result = std::max_element(lpos_vec.begin(), lpos_vec.end());
            auto rpos_result = std::min_element(rpos_vec.begin(), rpos_vec.end());
            l_c.x = *lpos_result; // *lpos_result 역참조 lpos_vec 이 iterator이기 때문에
            r_c.x = *rpos_result;
        } else if (lpos_vec.empty() || rpos_vec.empty()) {
            if (lpos_vec.empty()) {
                auto rpos_result = std::min_element(rpos_vec.begin(), rpos_vec.end());
                l_c.x = 0; // *lpos_result 역참조 lpos_vec 이 iterator이기 때문에
                r_c.x = *rpos_result;
            } else if (rpos_vec.empty()) {
                auto lpos_result = std::max_element(lpos_vec.begin(), lpos_vec.end());
                l_c.x = *lpos_result; // *lpos_result 역참조 lpos_vec 이 iterator이기 때문에
                r_c.x = 640;
            }
        }
    }
    else {
        l_c.x = 0; // *lpos_result 역참조 lpos_vec 이 iterator이기 때문에
        r_c.x = 640;
    }
    return std::make_pair(l_c, r_c);
}

