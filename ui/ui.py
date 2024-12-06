import tkinter as tk
from PIL import Image, ImageTk
import os

class UI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")  # 初始窗口大小
        self.base_path = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件的路径

        # 加载并显示背景
        self.background_image = None
        self.background_label = None

        # 监听窗口尺寸变化
        self.root.bind("<Configure>", self.on_resize)

    def load_background(self):
        """加载背景图片并显示"""
        image_path = os.path.join(self.base_path, "..", "pic", "table", "table.jpg")
        image = Image.open(image_path)

        # 获取窗口当前的宽高
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # 调整背景图片大小以适应窗口
        image = image.resize((width, height), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(image)

        # 如果背景标签已创建，则更新图片，否则创建新标签
        if self.background_label:
            self.background_label.config(image=self.background_image)
        else:
            self.background_label = tk.Label(self.root, image=self.background_image)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def on_resize(self, event):
        """窗口大小变化时更新背景"""
        self.load_background()
        

    def create_label(self, text):
        """创建标签"""
        label = tk.Label(self.root, text=text)
        label.pack()

    def create_button(self, text, command):
        """创建按钮"""
        button = tk.Button(self.root, text=text, command=command)
        button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    ui = UI(root)
    ui.load_background()  # 加载背景图片
    ui.create_label("Hello, World!")
    ui.create_button("Click Me", lambda: print("Button Clicked"))
    root.mainloop()
