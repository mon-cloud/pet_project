import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import time
import threading
import random
import ctypes
import google.generativeai as genai
import os  
from dotenv import load_dotenv

# Load các biến từ .env
load_dotenv()
key = os.getenv("API_KEY")

# ==== KÍCH THƯỚC MÀN HÌNH ====
user32 = ctypes.windll.user32
man_hinh_rong = user32.GetSystemMetrics(0)
man_hinh_cao = user32.GetSystemMetrics(1)

# ==== CỬA SỔ ====
cua_so = tk.Tk()
y = cua_so.winfo_screenheight() / 250
y2 = cua_so.winfo_screenwidth() / 300

height = cua_so.winfo_screenheight() / y
width = cua_so.winfo_screenwidth() / y2

rong_cua_so = int(width)
cao_cua_so = int(height)
cua_so.overrideredirect(True)
cua_so.wm_attributes('-transparentcolor', 'black')
cua_so.geometry(f"{rong_cua_so}x{cao_cua_so}+{man_hinh_rong - rong_cua_so}+{man_hinh_cao - cao_cua_so - 40}")
cua_so.config(bg='black')

# ==== LOAD ANIMATION ====
def load_gif(path, size=(80, 80)):
    img = Image.open(path)
    frames = []
    for frame in ImageSequence.Iterator(img):
        frame = frame.convert('RGBA')
        frame = frame.resize(size, Image.Resampling.LANCZOS)
        frames.append(ImageTk.PhotoImage(frame))
    return frames

# ==== LOAD PET ====
anh_ngoi = load_gif("./animation/ngoi.gif", size=(100, 100))
anh_dung = load_gif("./animation/dung.gif", size=(100, 100))
anh_di_trai = load_gif("./animation/di_trai.gif", size=(100, 100))
anh_di_phai = load_gif("./animation/di_phai.gif", size=(100, 100))

# ==== KHỞI TẠO PET ====
vi_tri_x = 120
vi_tri_y = 140
vi_tri_ban_dau = vi_tri_x

khung_hinh = tk.Label(cua_so, bg='black', bd=0)
khung_hinh.place(x=vi_tri_x, y=vi_tri_y)

# ==== TRẠNG THÁI ====
trang_thai = "ngoi"
frame_index = 0
trang_thai_truoc_do = "ngoi"
da_ngoi_xong = False
da_dung_xong = False

# ================================================================
# =================== CHAT AI ====================================
# ================================================================
CHAT_OFFSET_X = -100
CHAT_OFFSET_Y = -150
chat_visible = False

# ==== Cấu hình Gemini ====
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-1.5-flash")

# ==== Khung chat ====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
o_chat_path = os.path.join(BASE_DIR, "animation", "O_chat.png")
o_chat_bg_img = Image.open(o_chat_path).resize((250, 150))
o_chat_bg = ImageTk.PhotoImage(o_chat_bg_img)
khung_chat = tk.Label(cua_so, image=o_chat_bg, bg="black", bd=0)
khung_chat.place_forget()

# ==== Ô nhập ====
entry_text = tk.StringVar()
o_nhap = tk.Entry(cua_so, textvariable=entry_text, width=25, font=("Arial", 10))
o_nhap.place_forget()

# ==== Nút Clear ====
def clear_chat():
    entry_text.set("")
    lbl_kq.config(text="")
    cap_nhat_khung_chat_theo_text()  

btn_clear = tk.Button(cua_so, text="X", font=("Arial", 9, "bold"),
                      command=clear_chat, bg="red", fg="white", relief="flat", cursor="hand2")
btn_clear.place_forget()

# ==== Nhãn hiển thị kết quả (auto resize) ====
lbl_kq = tk.Message(cua_so, text="", width=230, font=("Arial", 9),
                    bg="white", anchor="w", justify="left")
lbl_kq.place_forget()

# ==== Hàm resize ô chat dựa trên text ====
def cap_nhat_khung_chat_theo_text():
    lbl_kq.update_idletasks()
    req_w = lbl_kq.winfo_reqwidth() + 40   
    req_h = lbl_kq.winfo_reqheight() + 90 

    # Giới hạn tối thiểu để không quá bé
    req_w = max(150, req_w)
    req_h = max(120, req_h)

    # Resize ảnh nền
    img_resized = Image.open(o_chat_path).resize((req_w, req_h))
    o_chat_bg_resized = ImageTk.PhotoImage(img_resized)

    # Cập nhật lại khung chat
    khung_chat.config(image=o_chat_bg_resized)
    khung_chat.image = o_chat_bg_resized

    # Cập nhật lại vị trí
    update_chat_position()

def update_chat_position():
    if not chat_visible:
        return
    x = vi_tri_x + CHAT_OFFSET_X
    y = vi_tri_y + CHAT_OFFSET_Y
    khung_chat.place_configure(x=x, y=y)
    o_nhap.place_configure(x=x + 20, y=y + 40)
    lbl_kq.place_configure(x=x + 20, y=y + 70)
    btn_clear.place_configure(x=x + 200, y=y + 40)

def hien_chat(event=None):
    global chat_visible
    chat_visible = True
    update_chat_position()
    khung_chat.place()
    o_nhap.place()
    lbl_kq.place()
    btn_clear.place()
    o_nhap.focus_set()

def tat_chat(event=None):
    global chat_visible
    chat_visible = False
    entry_text.set("")
    lbl_kq.config(text="")
    khung_chat.place_forget()
    o_nhap.place_forget()
    lbl_kq.place_forget()
    btn_clear.place_forget()
def hien_text_tu_tu(text, delay=30):
    """Hiệu ứng chữ hiện dần trong lbl_kq"""
    lbl_kq.config(text="")
    def go_tiep(i=0):
        if i <= len(text):
            lbl_kq.config(text=text[:i])
            cap_nhat_khung_chat_theo_text()
            cua_so.after(delay, lambda: go_tiep(i+1))
    go_tiep()

def gui_ai(event=None):
    user_msg = entry_text.get().strip()
    if not user_msg:
        return
    lbl_kq.config(text="Đang xử lý...")
    cap_nhat_khung_chat_theo_text()
    cua_so.update_idletasks()

    def call_ai():
        try:
            prompt = user_msg + ". Tóm tắt câu trả lời trong 120 kí tự và chỉ trả lời ý chính."
            response = model.generate_content(prompt)
            ket_qua = response.text.strip()
        except Exception as e:
            ket_qua = f"Lỗi: {e}"
        cua_so.after(0, lambda: hien_text_tu_tu(ket_qua))

    threading.Thread(target=call_ai, daemon=True).start()

# ==== Gắn sự kiện ====
khung_hinh.bind("<Button-1>", hien_chat)
o_nhap.bind("<Return>", gui_ai)
cua_so.bind("<F10>", tat_chat)

# ================================================================
# =================== ANIMATION PET ==============================
# ================================================================
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
            vi_tri_x = min(man_hinh_rong - 50, vi_tri_x + 3)  # chạy full màn
        case _:
            frame = anh_ngoi[0]

    khung_hinh.config(image=frame)
    khung_hinh.image = frame
    khung_hinh.place(x=vi_tri_x, y=vi_tri_y)

    update_chat_position()
    cua_so.after(100, cap_nhat_anh)

# ==== DI CHUYỂN ====
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
            time.sleep(random.randint(5, 30))
            hoat_dong = random.choice(["trai", "phai", "cả_hai"])
            global vi_tri_x
            if hoat_dong == "trai":
                di_chuyen("trai", random.randint(40, 80))
            elif hoat_dong == "phai":
                di_chuyen("phai", random.randint(40, 80))
            else:
                vi_tri_ban_dau = vi_tri_x
                buoc = random.randint(30, 60)
                di_chuyen("phai", buoc)
                di_chuyen("trai", buoc)
                vi_tri_x = max(0, min(man_hinh_rong - 50, vi_tri_ban_dau))
    threading.Thread(target=bat_dau, daemon=True).start()

# ==== PHÍM TẮT ====
def tat_pet(event=None):
    cua_so.destroy()
cua_so.bind("<F9>", tat_pet)

# ==== CHẠY ====
cap_nhat_anh()
tu_dong_di_lai()
cua_so.mainloop()
