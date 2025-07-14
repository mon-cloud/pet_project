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
cua_so.wm_attributes('-transparentcolor', 'black')
cua_so.geometry(f"{rong_cua_so}x{cao_cua_so}+{man_hinh_rong - rong_cua_so}+{man_hinh_cao - cao_cua_so - 40}")
cua_so.config(bg='black')

# ==== LOAD ANIMATION + RESIZE ====
def load_gif(path, size=(80, 80)):
    img = Image.open(path)
    frames = []
    for frame in ImageSequence.Iterator(img):
        frame = frame.convert('RGBA')
        frame = frame.resize(size, Image.Resampling.LANCZOS)
        frames.append(ImageTk.PhotoImage(frame))
    return frames

# ==== LOAD ẢNH PET ====
anh_ngoi = load_gif("./animation/ngoi.gif", size=(80, 80))
anh_dung = load_gif("./animation/dung.gif", size=(80, 80))
anh_di_trai = load_gif("./animation/di_trai.gif", size=(80, 80))
anh_di_phai = load_gif("./animation/di_phai.gif", size=(80, 80))

# ==== KHỞI TẠO PET ====
vi_tri_x = 120
vi_tri_y = 140
vi_tri_ban_dau = vi_tri_x

khung_hinh = tk.Label(cua_so, bg='black', bd=0)
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
    frame = None

    match trang_thai:
        case "ngoi":
            if not da_ngoi_xong:
                if frame_index < len(anh_ngoi):
                    frame = anh_ngoi[frame_index]
                    frame_index += 1
                else:
                    frame = anh_ngoi[-1]
                    da_ngoi_xong = True
            else:
                frame = anh_ngoi[-1]
        case "dung":
            if not da_dung_xong:
                if frame_index < len(anh_dung):
                    frame = anh_dung[frame_index]
                    frame_index += 1
                else:
                    frame = anh_dung[-1]
                    da_dung_xong = True
            else:
                frame = anh_dung[-1]
        case "trai":
            frame = anh_di_trai[frame_index % len(anh_di_trai)]
            frame_index += 1
            vi_tri_x = max(0, vi_tri_x - 3)
        case "phai":
            frame = anh_di_phai[frame_index % len(anh_di_phai)]
            frame_index += 1
            vi_tri_x = min(rong_cua_so - 50, vi_tri_x + 3)
        case default:
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
        while True:
            time.sleep(random.randint(5, 30))  #

            hoat_dong = random.choice(["trai", "phai", "cả_hai"])  
            global vi_tri_x
            if hoat_dong == "trai":
                di_chuyen("trai", random.randint(40, 80))
            elif hoat_dong == "phai":
                di_chuyen("phai", random.randint(40, 80))
            else:  # cả_hai
                vi_tri_ban_dau = vi_tri_x
                buoc = random.randint(30, 60)
                di_chuyen("phai", buoc)
                di_chuyen("trai", buoc)
                vi_tri_x = max(0, min(rong_cua_so - 50, vi_tri_ban_dau))  
    threading.Thread(target=bat_dau, daemon=True).start()

# ==== PHÍM TẮT F9 để tắt ====
def tat_pet(event=None):
    cua_so.destroy()
cua_so.bind("<F9>", tat_pet)

# ==== CHẠY ====
cap_nhat_anh()
tu_dong_di_lai()
cua_so.mainloop()
