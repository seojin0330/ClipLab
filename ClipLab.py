import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

# ffmpeg 명령어 실행 함수
def run_ffmpeg(cmd):
    print(cmd)
    subprocess.run(cmd, shell=True)

def convert():
    # 파일 선택하기
    files = filedialog.askopenfilenames(title="영상 선택")
    if not files:
        return

    # 저장할 폴더 선택
    save_folder = filedialog.askdirectory(title="저장할 폴더")
    if not save_folder:
        return

    # 선택한 옵션 가져오기
    r = rotate_var.get()
    s = size_var.get()
    f_fps = fps_var.get()
    c = codec_var.get()

    for file in files:
        # 파일 이름이랑 경로 분리
        filename = os.path.basename(file)
        name, ext = os.path.splitext(filename)
        
        # 저장할 경로 만들기
        output_file = os.path.join(save_folder, name + "_new.mp4")

        # 필터 만들기
        filter_list = []

        # 회전 옵션
        if r == "90도 시계방향":
            filter_list.append("transpose=1")
        elif r == "90도 반시계방향":
            filter_list.append("transpose=2")
        elif r == "180도 회전":
            filter_list.append("transpose=1,transpose=1")

        # 해상도 변경
        if s != "변경 안함":
            w, h = s.split("x")
            filter_list.append(f"scale={w}:{h}")

        # FPS 변경
        if f_fps != "변경 안함":
            filter_list.append(f"fps={f_fps}")

        # 필터 합치기
        if len(filter_list) > 0:
            vf = "-vf " + ",".join(filter_list)
        else:
            vf = ""

        # 코덱 설정
        if c == "H.264":
            codec = "-c:v libx264 -crf 18"
        elif c == "HEVC":
            codec = "-c:v libx265 -crf 23"
        else:
            codec = "-c:v libx264 -crf 18"

        # 명령어 만들기
        cmd = f'ffmpeg -i "{file}" {vf} {codec} -c:a copy "{output_file}"'
        
        # 실행
        run_ffmpeg(cmd)

    messagebox.showinfo("알림", "변환이 완료되었습니다!")

def merge():
    files = filedialog.askopenfilenames(title="합칠 영상 선택")
    if not files:
        return

    # 리스트 파일 만들기
    f = open("list.txt", "w", encoding="utf-8")
    for file in files:
        path = file.replace("\\", "/")
        f.write(f"file '{path}'\n")
    f.close()

    # 저장할 이름
    save_name = filedialog.asksaveasfilename(title="저장할 이름", defaultextension=".mp4")
    if not save_name:
        return

    # 합치기 명령어
    cmd = f'ffmpeg -f concat -safe 0 -i list.txt -c copy "{save_name}"'
    run_ffmpeg(cmd)

    # 리스트 파일 삭제
    os.remove("list.txt")
    messagebox.showinfo("알림", "합치기 완료!")

# GUI
root = tk.Tk()
root.title("클립랩(ClipLab) V1.2")
root.geometry("350x450")

tk.Label(root, text="클립랩(ClipLab)", font=("맑은 고딕", 15)).pack(pady=10)

# 회전 옵션
tk.Label(root, text="회전 설정").pack()
rotate_var = tk.StringVar()
rotate_combo = ttk.Combobox(root, textvariable=rotate_var, values=["없음", "90도 시계방향", "90도 반시계방향", "180도 회전"])
rotate_combo.set("없음")
rotate_combo.pack()

# 해상도 옵션
tk.Label(root, text="해상도 설정").pack()
size_var = tk.StringVar()
size_combo = ttk.Combobox(root, textvariable=size_var, values=["변경 안함", "1920x1080", "1280x720"])
size_combo.set("변경 안함")
size_combo.pack()

# FPS 옵션
tk.Label(root, text="FPS 설정").pack()
fps_var = tk.StringVar()
fps_combo = ttk.Combobox(root, textvariable=fps_var, values=["변경 안함", "60", "30"])
fps_combo.set("변경 안함")
fps_combo.pack()

# 코덱 옵션
tk.Label(root, text="코덱 설정").pack()
codec_var = tk.StringVar()
codec_combo = ttk.Combobox(root, textvariable=codec_var, values=["H.264", "HEVC"])
codec_combo.set("H.264")
codec_combo.pack()

# 버튼
tk.Button(root, text="변환하기", command=convert, width=20, height=2).pack(pady=20)
tk.Button(root, text="영상 합치기", command=merge, width=20, height=2).pack()

root.mainloop()
