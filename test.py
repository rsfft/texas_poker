import tkinter as tk

root = tk.Tk()
root.geometry("400x300")

# 创建一个 Frame 容器
frame = tk.Frame(root, width=300, height=200, bg="lightblue")
frame.pack()  # 将 Frame 添加到主窗口

root.mainloop()
