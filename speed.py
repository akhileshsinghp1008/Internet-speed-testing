import tkinter as tk
import speedtest
import threading
from PIL import Image, ImageTk, ImageDraw

# ---------------- ROUND IMAGE FUNCTION ----------------
def make_circle_image(path, size):
    """Return PhotoImage with circular mask"""
    img = Image.open(path).resize(size).convert("RGBA")
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    img.putalpha(mask)
    return ImageTk.PhotoImage(img)

# ---------------- SPEED TEST FUNCTION ----------------
def speed_test():
    try:
        result_speed.config(text="Testing...", fg="white")

        st = speedtest.Speedtest(secure=True)
        st.get_best_server()

        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        ping = st.results.ping

        overall = (download + upload) / 2

        # update values
        download_val.config(text=f"{download:.2f} Mbps")
        upload_val.config(text=f"{upload:.2f} Mbps")
        ping_val.config(text=f"{ping:.2f} ms")
        result_speed.config(text=f"{overall:.2f} Mbps")

    except Exception as e:
        result_speed.config(text="Error", fg="red")

# ---------------- BUTTON CLICK ----------------
def start_test():
    info_label.pack_forget()  # hide the info text
    threading.Thread(target=speed_test, daemon=True).start()

# ---------------- UI ----------------
root = tk.Tk()
root.title("Internet Speed Test")
root.geometry("360x520")
root.resizable(False, False)
root.configure(bg="#1a212d")

# Title
tk.Label(
    root,
    text="Internet Speed Test",
    font=("Arial", 18, "bold"),
    bg="#1a212d",
    fg="white"
).pack(pady=10)

# ---------------- TOP STATS ----------------
top_frame = tk.Frame(root, bg="#1a212d")
top_frame.pack(pady=10)

def stat_block(frame, img_path, label_text):
    """Create circular image + label + value"""
    photo = make_circle_image(img_path, (50,50))  # 50x50 px circular

    f = tk.Frame(frame, bg="#1a212d")
    f.pack(side="left", padx=15)

    lbl_img = tk.Label(f, image=photo, bg="#1a212d")
    lbl_img.image = photo
    lbl_img.pack()

    lbl_text = tk.Label(f, text=label_text, fg="white", bg="#1a212d", font=("Arial", 10))
    lbl_text.pack()

    lbl_val = tk.Label(f, text="--", fg="white", bg="#1a212d", font=("Arial", 11, "bold"))
    lbl_val.pack()

    return lbl_val

download_val = stat_block(top_frame, "d.png", "Download")
upload_val   = stat_block(top_frame, "d.png", "Upload")
ping_val     = stat_block(top_frame, "d.png", "Ping")

# ---------------- CENTER SPEED ----------------
center_frame = tk.Frame(root, bg="#1a212d")
center_frame.pack(pady=20)

tk.Label(
    center_frame,
    text="Current Speed",
    fg="white",
    bg="#1a212d",
    font=("Arial", 14)
).pack()

result_speed = tk.Label(
    center_frame,
    text="0 Mbps",
    fg="lime",
    bg="#1a212d",
    font=("Arial", 28, "bold")
)
result_speed.pack()

# ---------------- GO BUTTON ----------------
photo_btn = make_circle_image("speed.png", (90,90))  # circular GO button

btn = tk.Button(
    root,
    image=photo_btn,
    bg="#1a212d",
    borderwidth=0,
    activebackground="#1a212d",
    command=start_test
)
btn.image = photo_btn
btn.pack(pady=20)

# ---------------- INFO LABEL ----------------
info_label = tk.Label(
    root,
    text="Click To Check Your Internet Speed",
    fg="white",
    bg="#1a212d",
    font=("Arial", 13, "bold")
)
info_label.pack(pady=10)

root.mainloop()
