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
    b_rate = bitrate_var.get()

    for file in files:
        # 파일 이름이랑 경로 분리
        filename = os.path.basename(file)
        name, ext = os.path.splitext(filename)
        
        # 저장할 경로 만들기
        output_file = os.path.join(save_folder, name + "_converted.mp4")

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
        filter_str = ",".join(filter_list) if filter_list else ""

        # 코덱 설정
        if c == "H.264":
            codec_str = "libx264"
        elif c == "HEVC":
            codec_str = "libx265"
        else:
            codec_str = "libx264"

        # 비트레이트 설정
        bitrate_str = ""
        if b_rate != "변경 안함":
            bitrate_value = b_rate.replace("bps", "").lower()
            bitrate_str = f"-b:v {bitrate_value}"

        # ffmpeg 명령어 만들기
        cmd_parts = [f'ffmpeg -i "{file}"']
        
        if filter_str:
            cmd_parts.append(f'-vf "{filter_str}"')
        
        cmd_parts.append(f'-c:v {codec_str}')
        
        if bitrate_str:
            cmd_parts.append(bitrate_str)
        
        cmd_parts.append(f'-c:a copy "{output_file}"')
        
        cmd = " ".join(cmd_parts)
        
        # 실행
        run_ffmpeg(cmd)

    messagebox.showinfo("알림", "변환이 완료되었습니다!")

def merge():
    # 합치기 UI 윈도우 생성
    merge_window = tk.Toplevel(root)
    merge_window.title("영상 합치기")
    merge_window.geometry("400x500")

    # 파일 리스트 저장용 변수
    merge_files = []

    # 리스트박스 업데이트 함수
    def update_listbox():
        listbox.delete(0, tk.END)
        for file in merge_files:
            listbox.insert(tk.END, os.path.basename(file))

    # 파일 추가 함수
    def add_files():
        files = filedialog.askopenfilenames(title="합칠 영상 선택", filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv")])
        if files:
            for file in files:
                merge_files.append(file)
            update_listbox()

    # 선택 삭제 함수
    def remove_file():
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            del merge_files[index]
            update_listbox()

    # 위로 이동 함수
    def move_up():
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            if index > 0:
                merge_files[index], merge_files[index-1] = merge_files[index-1], merge_files[index]
                update_listbox()
                listbox.selection_set(index-1)

    # 아래로 이동 함수
    def move_down():
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            if index < len(merge_files) - 1:
                merge_files[index], merge_files[index+1] = merge_files[index+1], merge_files[index]
                update_listbox()
                listbox.selection_set(index+1)

    # 합치기 실행 함수
    def run_merge_process():
        if not merge_files:
            messagebox.showwarning("경고", "합칠 영상을 추가해주세요.")
            return

        # 저장할 이름
        save_name = filedialog.asksaveasfilename(title="저장할 이름", defaultextension=".mp4")
        if not save_name:
            return

        # 리스트 파일 만들기
        try:
            with open("list.txt", "w", encoding="utf-8") as f:
                for file in merge_files:
                    path = file.replace("\\", "/")
                    f.write(f"file '{path}'\n")
            
            # 합치기 명령어
            cmd = f'ffmpeg -f concat -safe 0 -i list.txt -c copy "{save_name}"'
            run_ffmpeg(cmd)

            # 리스트 파일 삭제
            if os.path.exists("list.txt"):
                os.remove("list.txt")
            
            messagebox.showinfo("알림", "합치기 완료!")
            merge_window.destroy()
            
        except Exception as e:
            messagebox.showerror("에러", f"오류가 발생했습니다: {str(e)}")

    # UI 구성
    frame_list = tk.Frame(merge_window)
    frame_list.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame_list)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(frame_list, selectmode=tk.SINGLE, yscrollcommand=scrollbar.set)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)

    frame_btns = tk.Frame(merge_window)
    frame_btns.pack(pady=5)

    tk.Button(frame_btns, text="파일 추가", command=add_files).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_btns, text="선택 삭제", command=remove_file).pack(side=tk.LEFT, padx=5)
    
    frame_move = tk.Frame(merge_window)
    frame_move.pack(pady=5)
    
    tk.Button(frame_move, text="▲ 위로", command=move_up).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_move, text="▼ 아래로", command=move_down).pack(side=tk.LEFT, padx=5)

    tk.Button(merge_window, text="합치기 실행", command=run_merge_process, height=2, bg="lightblue").pack(pady=20, fill=tk.X, padx=20)

# GUI
root = tk.Tk()
root.title("클립랩(ClipLab) V1.4")
root.geometry("350x480")

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

# 비트레이트 옵션
tk.Label(root, text="비트레이트 설정").pack()
bitrate_var = tk.StringVar()
bitrate_combo = ttk.Combobox(root, textvariable=bitrate_var, values=["변경 안함", "10Mbps", "5Mbps", "2Mbps", "1Mbps", "500Kbps"])
bitrate_combo.set("변경 안함")
bitrate_combo.pack()

# 버튼
tk.Button(root, text="변환하기", command=convert, width=20, height=2).pack(pady=20)
tk.Button(root, text="영상 합치기", command=merge, width=20, height=2).pack()

root.mainloop()
