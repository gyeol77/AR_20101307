# AR_20101307
This project is an AR-based interaction program that displays visual elements (images or a cube) depending on the number of fingers shown in a video.

The code is written in Python(3.10.0) and utilizes OpenCV and Mediapipe to recognize the number of extended fingers and overlay visual elements in real-time on the hand.

1 finger: Cat image  
2 fingers: Dog image  
5 fingers(open hand): 3D-style wireframe cube

The input video is processed using OpenCV's VideoCapture, and hand detection is performed with Mediapipe’s Hand Tracking.  
Finger counting is done by comparing the vertical positions of four landmarks(excluding the thumb).  
For each case, the appropriate PNG image or cube overlay is rendered directly on top of the hand.

---

이 프로젝트는 영상 속 손가락 수에 따라 시각적 요소(이미지 또는 큐브)를 표시하는 AR 기반 상호작용 프로그램입니다.

코드는 Python(3.10.0)으로 작성했고, OpenCV와 Mediaipe를 사용하여 펼쳐진 손가락의 수를 인식하고 시각적 요소를 손에 실시간으로 오버레이합니다.

손가락 한 개: 고양이 이미지
손가락 두 개: 강아지 이미지
손가락 다섯 개(펼쳤을 때): 3D 스타일 와이어프레임 큐브

입력 영상은 OpenCV의 VideoCapture를 사용하여 처리되고, 손 감지는 Mediapipe의 Hand Tracking을 통해 이루어집니다.
손가락 수는 네 개의 랜드마크(엄지 제외) 수직 위치를 비교해 계산됩니다.
각 경우마다 적절한 PNG 이미지 또는 큐브 오버레이가 손 위에 직접 렌더링됩니다.

---

Code: https://drive.google.com/file/d/1nYhSlPmL0klkA7xfLjdmwzOVdQFNj5KE/view?usp=drive_link
Cat image: https://drive.google.com/file/d/10xfUlwshwCn6TvpjpqD4iDs2fKVLid4Q/view?usp=drive_link
Dog image: https://drive.google.com/file/d/1-qhvc_kN-LrnuKSXH-u6Sm-Fo0PnYTWq/view?usp=drive_link
Sample Hand video: https://drive.google.com/file/d/1TwJPmBZ_WYKMKjB4DUJog378f_B5LM_q/view?usp=drive_link
Sample Output video(demo): https://drive.google.com/file/d/1D9lnLvkp_kF5Gles_sLpuUhuSSU2jzcu/view?usp=drive_link
