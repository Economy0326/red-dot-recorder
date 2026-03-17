# 🎥 Red Dot Recorder

OpenCV를 이용해 만든 간단한 비디오 레코더입니다.  
실시간 카메라 화면을 미리보기할 수 있고, 녹화 모드로 전환하여 영상을 파일로 저장할 수 있습니다.

---

## 📌 프로젝트 소개

이 프로그램은 OpenCV의 `VideoCapture`와 `VideoWriter`를 사용하여  
웹캠 영상을 화면에 출력하고, 원하는 순간에 녹화를 시작/종료할 수 있도록 만든 비디오 레코더입니다.

필수 기능으로는 Preview / Record 모드 전환, 녹화 상태 표시, 영상 저장 기능을 포함하고 있으며,  
추가 기능으로 FPS 조절, 좌우 반전, 흑백 필터, 밝기/대비 조절 기능을 구현했습니다.

---

## 📌 구현 기능

### 필수 기능

- 현재 카메라 영상 실시간 출력
- 동영상 파일 저장
- Preview / Record 모드 전환
- 녹화 중 빨간 원 표시
- `Space` 키로 모드 전환
- `ESC` 키로 프로그램 종료

### 추가 기능

- FPS 조절
- 좌우 반전(Flip)
- 흑백 필터(Gray Filter)
- 밝기 조절(Brightness)
- 대비 조절(Contrast)
- Outline Text UI로 화면 가독성 개선

---

## 📌 조작 방법

- `SPACE` : Preview / Record 전환
- `ESC` : 프로그램 종료
- `[` : FPS 감소
- `]` : FPS 증가
- `f` : 좌우 반전
- `g` : 흑백 필터 적용/해제
- `b` : 밝기 증가
- `c` : 대비 증가

---

## 📌 실행 방법

### 필요한 라이브러리 설치

- python -m venv .venv
- pip install opencv-python

### 프로그램 실행

- python main.py

### 저장 결과

- 녹화한 영상은 outputs/ 폴더에 저장됩니다.
- 또한 실행 예시용 영상 파일을 demo.mp4로 첨부했습니다.

---

## 📌 결과

### 실행 화면

- Preview 모드는 스크린샷에서 확인할 수 있습니다.
- Record 모드는 `demo.mp4` 파일에서 확인할 수 있습니다.

### 사용 기술

- Python
- OpenCV

### 참고

- 입력 소스로 기본 웹캠(0)을 사용했습니다.
- 녹화 상태가 어떤 배경에서도 잘 보이도록 Outline Text 방식으로 상태 UI를 표시했습니다.
