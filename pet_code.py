import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import time

# Tạo cửa sổ
cua_so = tk.Tk()
cua_so.title("Animation Con pet")
cua_so.geometry("800x600")
cua_so.configure(bg='black')

# Load animation 
def load_gif(path):
    img = Image.open(path)
    return [ImageTk.PhotoImage(frame.copy().convert('RGBA')) for frame in ImageSequence.Iterator(img)]

anh_ngoi = load_gif("./animation/ngoi.gif")
anh_dung = load_gif("./animation/dung.gif")
anh_di_trai = load_gif("./animation/di_trai.gif")
anh_di_phai = load_gif("./animation/di_phai.gif")

#hiển thị pet
vi_tri_x = 400
vi_tri_y = 300
khung_hinh = tk.Label(cua_so, bg='black')
khung_hinh.place(x=vi_tri_x, y=vi_tri_y)

# Biến đổi trạng thái
thoi_gian_cuoi_input = time.time()
trang_thai = "ngoi"  # "ngoi", "dung", "trai", "phai"
THOI_GIAN_KHONG_THAO_TAC = 1000  

# Cập nhật animation theo trạng thái
frame_index = 0
da_ngoi_xong = False  # kiểm tra đã xong animation ngồi chưa

frame_index = 0
trang_thai_truoc_do = "ngoi"
da_ngoi_xong = False
da_dung_xong = False

def cap_nhat_anh():
    global frame_index, trang_thai_truoc_do, da_ngoi_xong, da_dung_xong

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

    elif trang_thai == "phai":
        frame = anh_di_phai[frame_index % len(anh_di_phai)]
        frame_index += 1

    else:
        frame = anh_ngoi[0]

    khung_hinh.config(image=frame)
    khung_hinh.image = frame

    cua_so.after(100, cap_nhat_anh)


# Xử lý phím
def xu_ly_input(su_kien=None):
    global thoi_gian_cuoi_input, trang_thai, vi_tri_x

    thoi_gian_cuoi_input = time.time()

    if su_kien:
        phim = su_kien.keysym
        if phim == "Left":
            vi_tri_x = max(0, vi_tri_x - 10)
            trang_thai = "trai"
        elif phim == "Right":
            vi_tri_x = min(750, vi_tri_x + 10)
            trang_thai = "phai"
        else:
            trang_thai = "dung"

    khung_hinh.place(x=vi_tri_x, y=vi_tri_y)

# Kiểm tra idle
def kiem_tra_idle():
    global trang_thai

    hien_tai = time.time()
    treo = (hien_tai - thoi_gian_cuoi_input) * 1000

    if treo > THOI_GIAN_KHONG_THAO_TAC and trang_thai != "ngoi":
        trang_thai = "ngoi"

    cua_so.after(500, kiem_tra_idle)

cua_so.bind("<KeyPress>", xu_ly_input)
cua_so.bind("<Motion>", xu_ly_input)
cua_so.bind("<Button>", xu_ly_input)


cap_nhat_anh()
kiem_tra_idle()
cua_so.mainloop()

#123