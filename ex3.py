import tkinter as tk
window = tk.Tk()
window.title("Калькулятор")
window.geometry("300x250")
entry1 = tk.Entry(window)
entry1.pack(pady=10)

entry2 = tk.Entry(window)
entry2.pack(pady=10)

label = tk.Label(window, text="Результат: ")
label.pack(pady=10)
def add():
    num1 = int(entry1.get())
    num2 = int(entry2.get())
    result = num1 + num2
    label.config(text="Результат: " + str(result))
button = tk.Button(window, text="Сложить", command=add)
button.pack(pady=10)
window.mainloop()