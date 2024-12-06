import socket
import threading
import re
from kernal.poker import Card

class Client:
    def __init__(self, host, port):
        self.host = host
        self.client=None
        
        
    def connect_to_server(self,host,nickname):
        """连接服务器"""
        port=12345
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        try:   
            self.client.connect((host,port))
            self.client.sendall(nickname.encode())
        
        except Exception as e:
            print("连接失败：",e)
            
    def send_request(self,request):
        """发送请求"""
        try:
            self.client.sendall(request.encode())
        except Exception as e:
            print("发送请求失败：",e)
            
    def receive_response(self):
        """接收响应"""
        while True:
            try:
                response = self.client.recv(1024).decode()
                if not response:

                    break
                self.handle_response(response)  # 处理服务器响应
            except Exception as e:

                break
        self.client.close()
    
    def handle_response(self,response):
        """处理响应"""
        if response.startswith("座位信息:"):
            self.handle_seat_info(response)
        elif response.startswith("手牌信息:"):
            self.handle_hand_info(response)
        elif response.startswith("公共牌信息:"):
            self.handle_community_cards(response)
        elif response.startswith("底池总额:"):
            self.handle_pot_total(response)
        elif response.startswith("当前筹码数额为："):
            self.handle_chips_info(response)
        else:
            self.ui.display_message(f"未知的响应类型: {response}")
    
    def handle_seat_info(self, response):
        """处理座位信息"""
        seat_number, role = response.split(",")[1].split(":")  
        self.ui.display_seat_info(seat_number, role)

    def handle_hand_info(self, response):
        """处理手牌信息"""
        try:
            match = re.search(r"您的手牌为：(.*?)(?=\。|$)", response)
            if not match:
                print("未找到手牌信息")
                return []
    
            hand_str = match.group(1).strip()
            cards = []
    
            for card_str in hand_str.split("|"):
                parts = card_str.strip().split(" ")
                if len(parts) == 2:
                    rank, suit = parts
                    suit_map = {"♠": "spade", "♣": "club", "♥": "heart", "♦": "diamond"}
                    suit = suit_map.get(suit, suit)  # 使用映射，确保兼容性
                    cards.append(Card(suit=suit, rank=rank))
                else:
                    print(f"无法解析的手牌格式：{card_str}")
            return cards
        except Exception as e:
            print(f"解析手牌信息时出错: {e}")
            return []

    def handle_community_cards(self, response):
        """处理公共牌信息"""
        community_cards = response.split(":")[1]  
        self.ui.display_community_cards(community_cards)

    def handle_pot_total(self, response):
        """处理底池总额信息"""
        pot_total = int(response.split(":")[1])  
        self.ui.update_pot_display(pot_total)

    def handle_chips_info(self, response):
        """处理筹码信息"""
        try:
            match = re.search(r"当前筹码数额为：(\d+)", response)
            if match:
                return int(match.group(1))
        except Exception as e:
            print(f"解析筹码信息时出错: {e}")