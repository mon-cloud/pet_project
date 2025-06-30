import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import time
import threading
import random
import ctypes

# ==== KÍCH THƯỚC MÀN HÌNH ====
user32 = ctypes.windll.user32
man_hinh_rong = user32.GetSystemMetrics(0)
man_hinh_cao = user32.GetSystemMetrics(1)

# ==== CỬA SỔ ====
rong_cua_so = 300
cao_cua_so = 250

cua_so = tk.Tk()
cua_so.overrideredirect(True) 
cua_so.wm_attributes("-topmost", True)  
cua_so.geometry(f"{rong_cua_so}x{cao_cua_so}+{man_hinh_rong - rong_cua_so}+{man_hinh_cao - cao_cua_so - 40}")
cua_so.config(bg='black')

#BạckGround
canvas = tk.Canvas(cua_so, width=rong_cua_so, height=cao_cua_so, highlightthickness=0)
canvas.place(x=0, y=0)
canvas.create_rectangle(0, 0, rong_cua_so, cao_cua_so, fill="#ADD8E6", outline="")
canvas.create_oval(-150, cao_cua_so - 120, rong_cua_so + 150, cao_cua_so + 150, fill="#90EE90", outline="")

#Cây
canvas.create_rectangle(135, 120, 165, 180, fill="#8B4513", outline="")  # thân
canvas.create_oval(110, 80, 190, 140, fill="green", outline="")          # tán

# ==== LOAD ANIMATION ====
def load_gif(path):
    img = Image.open(path)
    return [ImageTk.PhotoImage(frame.copy().convert('RGBA')) for frame in ImageSequence.Iterator(img)]

anh_ngoi = load_gif("./animation/ngoi.gif")
anh_dung = load_gif("./animation/dung.gif")
anh_di_trai = load_gif("./animation/di_trai.gif")
anh_di_phai = load_gif("./animation/di_phai.gif")

# ==== KHỞI TẠO PET ====
vi_tri_x = 120
vi_tri_y = 140  # cao hơn để nằm trên cỏ
vi_tri_ban_dau = vi_tri_x

khung_hinh = tk.Label(cua_so, bg='#000000', bd=0)
khung_hinh.place(x=vi_tri_x, y=vi_tri_y)

# ==== TRẠNG THÁI PET ====
trang_thai = "ngoi"
frame_index = 0
trang_thai_truoc_do = "ngoi"
da_ngoi_xong = False
da_dung_xong = False

def cap_nhat_anh():
    global frame_index, trang_thai_truoc_do, da_ngoi_xong, da_dung_xong, vi_tri_x

    if trang_thai != trang_thai_truoc_do:
        frame_index = 0
        trang_thai_truoc_do = trang_thai
        da_ngoi_xong = False
        da_dung_xong = False

    if trang_thai == "ngoi":
        if not da_ngoi_xong:
            if frame_index < len(anh_ngoi):
                frame = anh_ngoi[frame_index]
                frame_index += 1
            else:
                frame = anh_ngoi[-1]
                da_ngoi_xong = True
        else:
            frame = anh_ngoi[-1]

    elif trang_thai == "dung":
        if not da_dung_xong:
            if frame_index < len(anh_dung):
                frame = anh_dung[frame_index]
                frame_index += 1
            else:
                frame = anh_dung[-1]
                da_dung_xong = True
        else:
            frame = anh_dung[-1]

    elif trang_thai == "trai":
        frame = anh_di_trai[frame_index % len(anh_di_trai)]
        frame_index += 1
        vi_tri_x = max(0, vi_tri_x - 3)

    elif trang_thai == "phai":
        frame = anh_di_phai[frame_index % len(anh_di_phai)]
        frame_index += 1
        vi_tri_x = min(rong_cua_so - 50, vi_tri_x + 3)

    else:
        frame = anh_ngoi[0]

    khung_hinh.config(image=frame)
    khung_hinh.image = frame
    khung_hinh.place(x=vi_tri_x, y=vi_tri_y)

    cua_so.after(100, cap_nhat_anh)

# ==== DI CHUYỂN TỰ ĐỘNG ====
def di_chuyen(huong, buoc=20, toc_do=0.05):
    global trang_thai
    trang_thai = huong
    for _ in range(buoc):
        time.sleep(toc_do)
        cua_so.update_idletasks()
    trang_thai = "dung"
    time.sleep(0.3)
    trang_thai = "ngoi"

def tu_dong_di_lai():
    def bat_dau():
        global vi_tri_x
        while True:
            time.sleep(random.randint(5, 10))  # test nhanh
            vi_tri_ban_dau = vi_tri_x
            di_chuyen("trai", 20, 0.05)
            di_chuyen("phai", 20, 0.05)
            vi_tri_x = vi_tri_ban_dau
            trang_thai = "ngoi"
    threading.Thread(target=bat_dau, daemon=True).start()
# ==== PHÍM TẮT F9 để tắt ====
def tat_pet(event=None):
    cua_so.destroy()

cua_so.bind("<F9>", tat_pet)

# ==== CHẠY ====
cap_nhat_anh()
tu_dong_di_lai()
cua_so.mainloop()

