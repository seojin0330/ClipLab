**ClipLab**은 Python과 FFmpeg를 사용하여
영상을 **변환(해상도, 회전, 코덱 등)** 하고
여러 개의 영상을 **하나로 합칠 수 있는 프로그램**입니다.

초보자도 쉽게 사용할 수 있도록 간단한 인터페이스와 자동 명령어 생성을 지원합니다.

---

## 주요 기능

* 여러 개의 영상 파일 선택 가능
* 해상도 변경 (예: 1280×720, 1920×1080)
* 영상 회전 (90°, 180°)
* FPS(프레임 레이트) 변경
* 코덱 변경 (H.264 등)
* 여러 영상 하나로 합치기(무손실 가능)
* 자동 FFmpeg 명령어 생성

---

## 💻 실행 환경

| 항목      | 내용           |
| ------- | ------------ |
| OS      | Windows      |
| 언어      | Python 3.10+ |
| 추가 프로그램 | FFmpeg       |

---

## 📦 설치 방법

설치 및 실행 영상 가이드 : https://youtu.be/ZU6AWa_b14Y
![설치방법](https://github.com/user-attachments/assets/7a8384fb-d0f6-4abc-bc60-8736a17c41a2)
⬆️용량으로 인해 영상이 끊어졌습니다 실행 단계부터는 윗 유튜브 링크로 확인해주세요

### 1️⃣ Python 설치

Python이 없다면 먼저 설치하세요

🔗 [https://www.python.org/downloads/](https://www.python.org/downloads/)

---

### 2️⃣ FFmpeg 설치

1. 아래 사이트에서 FFmpeg 다운로드
   🔗 [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

2. 압축을 푼 뒤 `bin` 폴더 경로를 환경변수(Path)에 추가

또는

1.CMD 또는 PowerShell을 관리자 권한으로 실행

2.명령어 입력: 

```bash
winget install ffmpeg
```
설치 확인:

```bash
ffmpeg -version
```

버전이 나오면 성공

---

### 3️⃣ 프로젝트 다운로드

```bash
git clone https://github.com/seojin0330/ClipLab.git
cd ClipLab
```

또는 ZIP 다운로드 후 압축 해제

---

## ▶️ 실행 방법

### 기본 실행

```bash
python main.py
```

프로그램이 실행되면:

1. **영상 파일 선택**
2. **옵션 설정 (해상도, 회전 등)**
3. **저장 위치 선택**
4. **변환 시작 버튼 클릭**

---

## 📌 사용 예시

1. `video1.mp4`, `video2.mp4` 선택
2. 해상도: 1280×720
3. 회전: 90°
4. 저장 위치: Documents
5. 변환 시작 클릭

결과:

```
video1_converted.mp4
video2_converted.mp4
```

---

## ⚙️ 사용된 기술

* Python
* FFmpeg
* Tkinter (GUI)
* Subprocess (명령어 실행)

---

## ⚠️ 주의 사항

* FFmpeg가 설치되어 있지 않으면 실행되지 않습니다.
* 파일 경로에 한글이 있으면 오류가 날 수 있습니다.
* 큰 파일은 변환 시간이 오래 걸릴 수 있습니다.
