import tkinter as tk
from tkinter import messagebox
import threading
from .server import PokerServer  

class ServerUI:

    def __init__(self, mainwindow):
        self.root = tk.Frame(mainwindow)
        self.root.pack(fill=tk.BOTH, expand=True)
        
         # 服务器实例
        self.server = None 
        
        #判断服务器是否创建成功
        self.success=False

        self.create_UI()


    def create_UI(self):
        """创建服务器界面"""
        # 创建标题
        self.create_label("德州扑克游戏服务器")

        # 创建输入项
        self.create_label("房间支持人数 (推荐2-10人，默认为2):")
        self.max_players_entry = self.create_entry(2)

        self.create_label("每位玩家初始筹码 (200-10000，偶数,默认为1000):")
        self.initial_chips_entry = self.create_entry(1000)

        self.create_label("大盲注数额 (偶数，推荐初始筹码的1/100，默认为10):")
        self.big_blind_entry = self.create_entry(10)

        # 创建启动服务器按钮
        self.start_button = self.create_button("启动服务器", self.start_server)

        # 显示服务器状态区域
        self.create_label("服务器状态:")
        self.server_status = tk.Text(self.root, width=80, height=20, state='disabled')
        self.server_status.pack()

       
    
    def clear_frame(self):
        """清空当前界面"""
        self.root.destroy()

    def create_label(self, text):
        label = tk.Label(self.root, text=text, font=("黑体", 12))
        label.pack()

    def create_entry(self,text=None):
        entry = tk.Entry(self.root, width=30, font=("黑体", 12)) if text is None else tk.Entry(self.root, width=30, font=("黑体", 12), textvariable=tk.StringVar(value=text))
        entry.pack()
        return entry
        
    def create_button(self, text, cmd):
        button = tk.Button(self.root, text=text, command=cmd, font=("黑体", 12))
        button.pack()
        return button    
    
    def add_temp_command(self, additional_command):
        # 临时添加一个新的command，这里会同时执行原始命令和额外命令
        self.start_button.config(command=lambda: [self.start_server(), additional_command()])
    
    def start_server(self):
        try:
            # 获取用户输入
            max_players = int(self.max_players_entry.get()or 2)
            initial_chips = int(self.initial_chips_entry.get()or 1000)
            big_blind = int(self.big_blind_entry.get()or 10)

            # 参数验证
            if not (2 <= max_players <= 10):
                raise ValueError("房间支持人数应在2-10人之间")
            if initial_chips % 2 != 0 or not (200 <= initial_chips <= 10000):
                raise ValueError("每位玩家初始筹码应为200-10000之间的偶数")
            if big_blind % 2 != 0 or not (2 <= big_blind <= initial_chips // 100):
                raise ValueError("大盲注数额应为初始筹码1/100的偶数")

            # 创建并启动服务器
            self.server = PokerServer()
            self.server.max_players = max_players
            self.server.initial_chips = initial_chips
            self.server.big_blind = big_blind
            self.server.small_blind = big_blind // 2

            # 使用线程启动服务器
            self.server_started=False
            if not self.server_started:
                self.success=True
                server_thread = threading.Thread(target=self.server.start, daemon=True)
                server_thread.start() 

            self.update_status(f"服务器启动成功！IP 地址: {self.server.get_local_ip()}\n")
        except ValueError as e:
            messagebox.showerror("参数错误", str(e))
        except Exception as e:
            messagebox.showerror("错误", f"无法启动服务器: {e}")
    
    def show_connection_info(self):
        """显示服务器连接信息"""
        if self.server is None:
            return
    
    
    def update_status(self, message):
        """更新服务器状态显示"""
        self.server_status.config(state='normal')
        self.server_status.insert('end', message + "\n")
        self.server_status.config(state='disabled')
        self.server_status.see('end')


if __name__ == '__main__':
    mainwindow = tk.Tk()
    mainwindow.title("德州扑克游戏")
    mainwindow.geometry("800x600")
    server_ui = ServerUI(mainwindow)
    mainwindow.mainloop()
