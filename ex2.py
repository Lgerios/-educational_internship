import tkinter as tk
window = tk.Tk()
window.title("Счётчик кликов")
window.geometry("300x250")
count = 0
label = tk.Label(window, text="0", font=("Arial", 20))
label.pack(pady=20)
def on_click():
    global count
    count = count + 1
    label.config(text=str(count))

def on_reset():
    global count
    count = 0
    label.config(text="0")

button1 = tk.Button(window, text="Клик", command=on_click)
button1.pack(pady=10)
button2 = tk.Button(window, text="Сброс", command=on_reset)
button2.pack(pady=10)

window.mainloop()