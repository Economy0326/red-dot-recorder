import cv2 as cv
import os
# 현재 날짜와 시간
from datetime import datetime

# path에 해당하는 폴더 없으면 자동으로 path 폴더 생성
def ensure_output_dir(path="outputs"):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

# video writer 생성 함수
def create_writer(frame_width, frame_height, fps, output_dir="outputs"):
    # mp4 저장 시 운영체제/코덱 환경에 따라 avc1이 안 될 수 있어서 mp4v 사용
    fourcc = cv.VideoWriter_fourcc(*"mp4v")
    # 현재 시간 기반으로 파일 이름 만들고
    filename = datetime.now().strftime("record_%Y%m%d_%H%M%S.mp4")
    # 그 파일 이름으로 outputs 폴더에 저장할 경로 만들기
    filepath = os.path.join(output_dir, filename)

    # writer = 동영상 파일 저장 객체
    writer = cv.VideoWriter(
        filepath, # 경로
        fourcc,   # 코덱
        fps,      # 프레임 속도
        (frame_width, frame_height) # 프레임 크기
    )
    return writer, filepath


# 밝기와 대비 조절 함수
def apply_brightness_contrast(frame, brightness=0, contrast=1.0):
    # new pixel = alpha(대비) * old_pixel + beta(밝기)
    # convertScaleAbs는 결과값을 0~255 범위로 자동 처리
    return cv.convertScaleAbs(frame, alpha=contrast, beta=brightness)

# 현재 상태를 화면에 표시하는 함수
def draw_status(frame, is_recording, fps, flip_enabled, gray_enabled, brightness, contrast):
    h, w = frame.shape[:2]

    mode_text = "RECORD" if is_recording else "PREVIEW"
    color = (0, 0, 255) if is_recording else (0, 255, 0)

    # 현재 모드 표시
    # outline text를 위해 먼저 검은색 테두리를 두껍게 그리고,
    # 그 위에 실제 색상의 글씨를 다시 그린다.
    cv.putText(
        frame,                          # 글씨를 그릴 대상 이미지
        f"Mode: {mode_text}",           # 표시할 문자열
        (20, 30),                       # 시작 위치 (x, y)
        cv.FONT_HERSHEY_SIMPLEX,        # 글꼴
        0.8,                            # 글자 크기
        (0, 0, 0),                      # 테두리 색(검정)
        4                               # 테두리 두께
    )
    cv.putText(
        frame,                          # 글씨를 그릴 대상 이미지
        f"Mode: {mode_text}",           # 표시할 문자열
        (20, 30),                       # 시작 위치 (x, y)
        cv.FONT_HERSHEY_SIMPLEX,        # 글꼴
        0.8,                            # 글자 크기
        color,                          # 글자 색
        2                               # 글자 두께
    )

    if is_recording:
        cv.circle(
            frame,                      # 원을 그릴 대상 이미지
            (w - 30, 30),               # 원 중심 좌표
            10,                         # 반지름
            (0, 0, 255),                # 색상(BGR) -> 빨강
            -1                          # -1이면 내부를 채운 원
        )

    # 현재 프레임 속도
    cv.putText(frame, f"FPS: {fps}", (20, 65),
              cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
    cv.putText(frame, f"FPS: {fps}", (20, 65),
              cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # 좌우 반전 기능 on/off
    cv.putText(frame, f"Flip: {'ON' if flip_enabled else 'OFF'}", (20, 95),
              cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
    cv.putText(frame, f"Flip: {'ON' if flip_enabled else 'OFF'}", (20, 95),
              cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # 흑백 필터 on/off
    cv.putText(frame, f"Gray: {'ON' if gray_enabled else 'OFF'}", (20, 125),
              cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
    cv.putText(frame, f"Gray: {'ON' if gray_enabled else 'OFF'}", (20, 125),
              cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # 밝기 값 표시
    cv.putText(frame, f"Brightness: {brightness}", (20, 155),
              cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
    cv.putText(frame, f"Brightness: {brightness}", (20, 155),
              cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # 대비 값 표시
    cv.putText(frame, f"Contrast: {contrast:.1f}", (20, 185),
              cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
    cv.putText(frame, f"Contrast: {contrast:.1f}", (20, 185),
              cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # 조작 방법 안내
    cv.putText(frame, "SPACE: Toggle Preview/Record | ESC: Exit", (20, h - 70),
              cv.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 4)
    cv.putText(frame, "SPACE: Toggle Preview/Record | ESC: Exit", (20, h - 70),
              cv.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

    cv.putText(frame, "[ / ]: FPS Down/Up | f: Flip | g: Gray Filter", (20, h - 45),
              cv.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 4)
    cv.putText(frame, "[ / ]: FPS Down/Up | f: Flip | g: Gray Filter", (20, h - 45),
              cv.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

    cv.putText(frame, "b: Brightness Up | c: Contrast Up", (20, h - 20),
              cv.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 4)
    cv.putText(frame, "b: Brightness Up | c: Contrast Up", (20, h - 20),
              cv.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)


def main():
    output_dir = ensure_output_dir("outputs")

    # 입력 소스
    # 웹캠 사용 시
    source = 0 
    # rtsp 스트림 사용 시 
    # source = "rtsp://아이디:비밀번호@192.168.0.10:554/stream"

    # 카메라 연결
    cap = cv.VideoCapture(source)

    if not cap.isOpened():
        print("입력 영상을 열 수 없습니다.")
        return

    # 첫 프레임을 먼저 읽어서 실제 크기 확인
    ret, frame = cap.read()
    if not ret:
        print("첫 프레임을 읽을 수 없습니다.")
        cap.release()
        return

    # 실제 프레임 크기 가져오기
    frame_height, frame_width = frame.shape[:2]

    # 기본 FPS
    fps = 20

    writer = None
    output_path = None
    is_recording = False

    flip_enabled = False
    gray_enabled = False
    brightness = 0
    contrast = 1.0

    print("프로그램 시작")
    print("SPACE: Preview/Record 전환")
    print("ESC: 종료")
    print("[ / ]: FPS 감소/증가")
    print("f: 좌우 반전")
    print("g: 흑백 필터")
    print("b: 밝기 증가")
    print("c: 대비 증가")

    # 메인 반복문 시작
    while True:
      # 프레임 읽기
      ret, frame = cap.read()
      if not ret:
        print("프레임을 읽을 수 없습니다.")
        break
        
      # 좌우 반전 적용
      if flip_enabled:
          frame = cv.flip(frame, 1)

      # 밝기/대비 조절을 적용한 결과를 processed에 저장
      processed = apply_brightness_contrast(
          frame,
          brightness=brightness,
          contrast=contrast
      )

      # 흑백 필터 적용
      if gray_enabled:
          # 먼저 BGR -> GRAY로 변환한 다음, 다시 GRAY -> BGR로 변환해서 processed에 저장
          gray = cv.cvtColor(processed, cv.COLOR_BGR2GRAY)
          processed = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)

      # 상태 UI 표시
      draw_status(processed, is_recording, fps, flip_enabled, gray_enabled, brightness, contrast)

      # 화면 출력
      cv.imshow("Red Dot Recorder", processed)

      # 현재 녹화 중이고 writer가 정상적으로 열려 있다면
      # processed 프레임을 비디오로 저장
      if is_recording and writer is not None:
          writer.write(processed)

      # 키 입력을 1ms 동안 기다리고, 입력이 있으면 key에 저장
      # 입력이 없을 경우 key는 -1 비슷한 값이 됨
      key = cv.waitKey(1) & 0xFF

      if key == 27:  # ESC의 ASCII 코드
          break

      elif key == 32:  # SPACE의 ASCII 코드
          is_recording = not is_recording

          # RECORD 모드로 전환될 때 = 녹화 시작
          if is_recording:
              writer, output_path = create_writer(frame_width, frame_height, fps, output_dir)
              if writer.isOpened():
                  print(f"[RECORD START] {output_path}")
              else:
                  print("VideoWriter를 열 수 없습니다. 녹화를 취소합니다.")
                  is_recording = False
                  writer = None
          # PREVIEW 모드로 전환될 때 = 녹화 종료
          else:
              # writer가 None이 아니면, 즉 녹화가 정상적으로 시작된 상태라면 writer를 닫고 저장 완료 메시지 출력
              if writer is not None:
                  writer.release()
                  writer = None
              print(f"[RECORD STOP] 저장 완료: {output_path}")

      elif key == ord('f'):
          flip_enabled = not flip_enabled

      elif key == ord('g'):
          gray_enabled = not gray_enabled

      elif key == ord('b'):
          brightness = min(brightness + 10, 100)

      elif key == ord('c'):
          contrast = min(contrast + 0.1, 3.0)

      elif key == ord('['):
          fps = max(5, fps - 5)
          print(f"FPS 변경: {fps}")

      elif key == ord(']'):
          fps = min(60, fps + 5)
          print(f"FPS 변경: {fps}")

    # 반복문 종료 후 자원 해제
    cap.release()
    if writer is not None:
        writer.release()
    cv.destroyAllWindows()
    print("프로그램 종료")

if __name__ == "__main__":
    main()