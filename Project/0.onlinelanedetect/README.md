# 4팀 - A팀 발표자료

**영상처리** 

- `원본 영상 → BGR to Gray → Lidar 영역 마스크 → ROI crop [→ 평균 밝기 필터  → GaussianBlur → Binarization(이진화)]`
- ROI 영역만 영상을  전처리한 이유
   
   adpative threshold 를 이용할 경우에는 이진화가 잘 되지만 100배 정도 느린 속도를 가지고 있다.
   
   ROI 영역 ( y값 370 ~ 430 구간)에 대해서만 이미지 전처리를 수행했다.
   

- Gaussian
   
   평균 필터에서는 필터의 중앙 점을 기준으로 주변 영상의 가중치가 높아지기 때문에 현재 위치의 픽셀 값의 비중은 줄어들고 주변 픽셀들의 영향이 커지는 문제가 나타난다.
   

**포즈찾기**

- `{레이블링 -> 각 컴포넌트의 평균값 저장} -> 왼쪽 오른쪽 구분 -> center에서 가장 가까운 값을 line이라고 지정`
- Code
   1. 레이블링 → 평균값저장 (centroids)
         
         ```cpp
            int num_labels = connectedComponentsWithStats(src, labels, stats, centroids);
         ```
         
   2. 왼쪽 오른쪽 차선 영역 구분
         
         ```cpp
         
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
         
         ```
         
   3. center에서 가까운 값을 차선이라고 지정
         
         ```cpp
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
         ```
         
- Components