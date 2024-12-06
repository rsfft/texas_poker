import socket
import threading
import netifaces 
from kernal.player import Player

class Server:
    def __init__(self,host='0.0.0.0', port=12345):
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.bind((host,port))
        self.players=[]
        self.max_players=0
        self.ready_players=0
        self.initial_chips=0
        self.big_blind=0
        self.small_blind=0
        
    def get_local_ip(self):
        """尝试获取本地的 IPv4 地址"""
        try:
            interfaces = netifaces.interfaces()  # 获取所有网络接口
            potential_ips = []
            for interface in interfaces:
                if_addresses = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in if_addresses:
                    ipv4_addresses = if_addresses[netifaces.AF_INET]
                    for address_info in ipv4_addresses:
                        ip_address = address_info.get('addr')
                        potential_ips.append(ip_address)

            # 过滤并选择局域网的 IP 地址
            for ip in potential_ips:
                if ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('172.'):
                    return ip

            # 如果没有匹配的局域网 IP，返回回环地址
            return '127.0.0.1'

        except Exception as e:
            print(f"获取本地 IP 地址时发生错误: {e}")
            return '127.0.0.1'
    
    def start(self):
        """启动服务器"""
        self.socket.listen()
        self.socket.ip=self.get_local_ip()
        
    def accept_connections(self):
        """接受连接"""
        while True:
            
            socket,addr=self.socket.accept()
            player=Player(socket,self.initial_chips)
            self.players.append(player)
            
            if(len(self.players)==self.max_players):
                #满了就不接受连接
                self.start_game()

    def start_game(self):
        """开始游戏"""
        for player in self.players:
            while True:
                try:
                    response=player.socket.recv(1024).decode().strip().lower()
                    
                    if response=="yes":
                        self.ready_players+=1
                        player.socket.sendall("准备成功,等待其他玩家准备".encode())
                        break
                except Exception as e:
                    print(f"玩家 {player.name} 连接断开: {e}")
                    self.players.remove(player)
                    self.accept_connections()
                    break
            
        if self.ready_players==self.max_players:
            print("游戏开始")
            ##运行
        
    def handle_request(self,player):
        """处理请求"""
        request=player.socket.recv(1024).decode().strip.lower()
        
        if "筹码"in request:
            response=f"您的筹码为：{player.chips}"
            self.socket.sendall(response.encode())
            
        if ""in request:
            response=""
        
            
        

        

