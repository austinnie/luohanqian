import json
import random
from collections import OrderedDict
import time
import sys
import os
from colorama import init, Fore, Back, Style

# 初始化颜色设置
init(autoreset=True)

class LuohanqianDivination:
    def __init__(self, data_file="luohanqian.json"):
        """初始化签文数据库"""
        self.signs_data = None  # 先设为None
        self.categories = ["总判", "功名", "婚姻", "求财", "疾病", "诉讼", 
                         "行人", "年成", "求嗣", "移居", "失物", "出行", "家宅", 
                         "六甲", "谋望", "自身"]
        self.history = []  # 历史记录
        
        # 先设置颜色方案
        self._setup_colors()
        
        # 然后加载数据
        self.signs_data = self._load_data(data_file)
    
    def _setup_colors(self):
        """配置颜色方案"""
        self.color_scheme = {
            "上上签（大吉）": Fore.GREEN + Style.BRIGHT,
            "上上": Fore.GREEN + Style.BRIGHT,
            "上吉": Fore.CYAN + Style.BRIGHT,
            "中吉": Fore.BLUE,
            "中平": Fore.YELLOW,
            "下下": Fore.RED,
            "title": Fore.MAGENTA + Style.BRIGHT,
            "menu": Fore.CYAN,
            "prompt": Fore.YELLOW,
            "error": Fore.RED + Style.BRIGHT,
            "poem": Fore.GREEN,
            "category": Fore.BLUE,
            "content": Fore.WHITE
        }
    
    def _load_data(self, data_file):
        """安全加载JSON数据"""
        try:
            # 首先检查文件是否存在
            if not os.path.exists(data_file):
                print(self._color_text('error', f'错误：找不到数据文件 {data_file}'))
                print(self._color_text('error', '请确保已运行文本转换脚本生成 luohanqian.json 文件'))
                return OrderedDict()
            
            with open(data_file, "r", encoding="utf-8") as f:
                content = f.read()
                if not content.strip():
                    raise ValueError("数据文件为空")
                
                data = json.loads(content)
                if not data:
                    print(self._color_text('error', '警告：JSON文件为空或格式不正确'))
                    return OrderedDict()
                
                print(self._color_text('menu', f'📊 成功加载 {len(data)} 支签文'))
                return data
            
        except json.JSONDecodeError as e:
            print(self._color_text('error', f'JSON解析错误：{e}'))
            print(self._color_text('error', '请检查 luohanqian.json 文件格式是否正确'))
            return OrderedDict()
        except Exception as e:
            print(self._color_text('error', f'加载数据失败：{e}'))
            return OrderedDict()
    
    def _color_text(self, color_type, text):
        """辅助方法：使用颜色输出文本"""
        color = self.color_scheme.get(color_type, '')
        if color:
            return f"{color}{text}{Style.RESET_ALL}"
        else:
            return text
    
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw_random_sign(self):
        """随机抽签"""
        if not self.signs_data:
            print(self._color_text('error', '签文数据库为空！请检查数据文件。'))
            return None
        
        sign_keys = list(self.signs_data.keys())
        if not sign_keys:
            print(self._color_text('error', '没有可用的签文！'))
            return None
        
        sign_key = random.choice(sign_keys)
        return self.get_sign_info(sign_key)
    
    def get_sign_info(self, sign_num):
        """获取指定签号的信息"""
        return self.signs_data.get(sign_num)
    
    def search_by_category(self, category):
        """按分类查询签文"""
        if category not in self.categories:
            return None
        
        results = []
        for sign_num, sign in self.signs_data.items():
            if category in sign["解析"]:
                results.append((sign_num, sign.get("签题", ""), sign["解析"][category]))
        
        return results
    
    def display_sign(self, sign):
        """显示签文信息"""
        if not sign:
            print(self._color_text('error', '未找到签文信息'))
            return
        
        # 获取签文数据
        sign_num = sign.get("签号", "未知签号")
        sign_title = sign.get("签题", "")
        luck = sign.get("吉凶", "未知吉凶")
        poem = sign.get("签诗", "")
        total_judge = sign.get("总判", "")
        analysis = sign.get("解析", {})
        
        # 获取吉凶颜色
        luck_key = luck
        if "（大吉）" in luck:
            luck_key = "上上签（大吉）"
        luck_color = self.color_scheme.get(luck_key, self.color_scheme.get(luck, Fore.WHITE))
        
        # 显示签文标题
        print(f"\n╔{'═'*60}╗")
        print(f"║ {luck_color}【{sign_num}·{luck}】{Fore.MAGENTA + Style.BRIGHT if 'title' in self.color_scheme else ''}{sign_title:^38}{Style.RESET_ALL} ║")
        print(f"╚{'═'*60}╝")
        
        # 显示签诗
        if poem:
            print(f"\n📜 {Fore.GREEN}签诗：{Style.RESET_ALL}")
            poem_lines = poem.split('\n')
            for poem_line in poem_lines:
                if poem_line.strip():
                    print(f"    {Fore.GREEN}{poem_line.strip()}{Style.RESET_ALL}")
            print()
        
        # 显示总判
        if total_judge:
            print(f"🔮 {Fore.CYAN}总判：{Style.RESET_ALL}{total_judge}")
            print()
        
        # 显示解析内容
        if analysis:
            for category in self.categories:
                if category in analysis:
                    content = analysis[category]
                    category_display = f"{Fore.BLUE}{category:6}{Style.RESET_ALL}"
                    print(f"✨ {category_display} → {content}")
        else:
            print(f"{Fore.YELLOW}⚠️ 未找到详细解析信息{Style.RESET_ALL}")
        
        print(f"\n{'═'*60}\n")
    
    def animate_drawing(self, duration=2):
        """抽签动画效果"""
        print(f"\n🙏 正在诚心求签...")
        symbols = ["🙏", "🕉️", "☸️", "🪷", "🔔", "🌟"]
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for symbol in symbols:
                sys.stdout.write(f"\r{symbol} 签菩萨显灵中... ")
                sys.stdout.flush()
                time.sleep(0.2)
        print("\r" + " "*30 + "\r", end="")
    
    def show_history(self):
        """显示求签历史"""
        if not self.history:
            print(f"{Fore.YELLOW}暂无历史记录{Style.RESET_ALL}")
            return
        
        print(f"\n≡≡ 求签历史 ≡≡")
        print(f"{'═'*40}")
        for idx, record in enumerate(self.history[::-1], 1):
            sign = self.signs_data.get(record['签号'])
            luck = sign.get('吉凶', '未知吉凶') if sign else '未知吉凶'
            luck_display = self._color_text('error' if '下下' in luck else 'menu', luck)
            sign_color = self._color_text('title', '')  # 默认颜色
            
            print(f"{idx}. {record['时间']} {luck_display}{record['签号']}{Style.RESET_ALL} {record.get('签题', '')}")
        print(f"{'═'*40}\n")
    
    def run(self):
        """运行主程序"""
        # 检查数据是否加载成功
        if not self.signs_data:
            print(self._color_text('error', '系统初始化失败！无法加载签文数据。'))
            print("请按以下步骤操作：")
            print("1. 确保 luohanqian.json 文件存在且格式正确")
            print("2. 如果没有，请运行文本转换脚本生成正确的JSON文件")
            print("3. 然后再次运行此占卜系统")
            input("按回车键退出...")
            return
        
        self.clear_screen()
        print(f"\n≡≡≡≡≡≡≡≡≡≡ 罗汉签占卜系统 ≡≡≡≡≡≡≡≡≡≡")
        print(f"{'='*60}")
        print(f"{Fore.MAGENTA}诚心求签，菩萨指点迷津{Style.RESET_ALL}")
        print(f"📊 当前数据库包含 {len(self.signs_data)} 支签文")
        
        while True:
            print(f"\n{Fore.CYAN}1. 🙏 随机求签{Style.RESET_ALL}")
            print(f"{Fore.CYAN}2. 🔍 查询指定签{Style.RESET_ALL}")
            print(f"{Fore.CYAN}3. 📋 按分类查询{Style.RESET_ALL}")
            print(f"{Fore.CYAN}4. 📜 求签历史{Style.RESET_ALL}")
            print(f"{Fore.CYAN}5. 🚪 退出系统{Style.RESET_ALL}")
            
            try:
                choice = input(f"\n{Fore.YELLOW}\n请选择功能(1-5)：{Style.RESET_ALL}").strip()
                
                if choice == "1":
                    self.handle_random_draw()
                elif choice == "2":
                    self.handle_specific_draw()
                elif choice == "3":
                    self.handle_category_search()
                elif choice == "4":
                    self.show_history()
                    input(f"\n{Fore.YELLOW}按回车键返回主菜单...{Style.RESET_ALL}")
                    self.clear_screen()
                elif choice == "5":
                    print(f"\n{Fore.MAGENTA}🙏 感谢使用罗汉签占卜系统！愿菩萨保佑您！{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED}⚠️ 输入无效，请重新选择！{Style.RESET_ALL}")
                
                self.clear_screen()
            
            except KeyboardInterrupt:
                print(f"\n\n{Fore.RED}检测到中断操作，退出系统...{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}发生错误：{e}{Style.RESET_ALL}")
                input("按回车键继续...")
                self.clear_screen()

    def handle_random_draw(self):
        """处理随机抽签"""
        self.animate_drawing()
        sign = self.draw_random_sign()
        
        if sign:
            self.display_sign(sign)
            
            # 添加到历史记录
            self.history.append({
                "签号": sign["签号"],
                "签题": sign.get("签题", ""),
                "时间": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # 保存选项
            save = input(f"\n{Fore.YELLOW}是否保存此签文结果？(y/n): {Style.RESET_ALL}").lower()
            if save == 'y':
                filename = f"罗汉签_{sign['签号']}_{time.strftime('%Y%m%d')}.txt"
                self.save_sign_to_file(sign, filename)
                print(f"{Fore.CYAN}📄 签文已保存到 {filename}{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}按回车键返回主菜单...{Style.RESET_ALL}")
    
    def handle_specific_draw(self):
        """处理指定签号查询"""
        num = input(f"\n{Fore.YELLOW}请输入签号(如：第1签、第2签)：{Style.RESET_ALL}").strip()
        if not num:
            print(f"{Fore.RED}⚠️ 签号不能为空！{Style.RESET_ALL}")
            input("按回车键继续...")
            return
        
        sign = self.get_sign_info(num)
        self.display_sign(sign)
        input(f"\n{Fore.YELLOW}按回车键返回主菜单...{Style.RESET_ALL}")
    
    def handle_category_search(self):
        """处理分类查询"""
        print(f"\n{Fore.CYAN}📋 可选分类：" + " | ".join(self.categories))
        category = input(f"\n{Fore.YELLOW}请输入分类名称：{Style.RESET_ALL}").strip()
        
        if category not in self.categories:
            print(f"{Fore.RED}⚠️ 分类不存在！{Style.RESET_ALL}")
            input("按回车键继续...")
            return
        
        results = self.search_by_category(category)
        if results:
            print(f"\n{Fore.MAGENTA}🔍 【{category}】相关签文：{Style.RESET_ALL}")
            print(f"{'═'*50}")
            for sign_num, title, content in results:
                print(f"\n◎ {Fore.BLUE}第{sign_num}签{Style.RESET_ALL}")
                if title:
                    print(f"   签题：{title}")
                print(f"   {category}：{content}")
            print(f"\n{Fore.CYAN}共找到 {len(results)} 条相关签文{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}该分类下没有找到签文！{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}按回车键返回主菜单...{Style.RESET_ALL}")
    
    def save_sign_to_file(self, sign, filename):
        """保存签文到文件"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"【{sign['签号']}·{sign['吉凶']}】{sign.get('签题', '')}\n")
                f.write(f"📅 求签日期：{time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                if sign.get("签诗"):
                    f.write(f"📜 签诗：\n")
                    poem_lines = sign["签诗"].split('\n')
                    for poem_line in poem_lines:
                        if poem_line.strip():
                            f.write(f"    {poem_line.strip()}\n")
                    f.write("\n")
                
                if sign.get("总判"):
                    f.write(f"🔮 总判：\n{sign['总判']}\n\n")
                
                f.write(f"📊 详细解析：\n")
                for category, content in sign["解析"].items():
                    f.write(f"● {category}：{content}\n")
        except Exception as e:
            print(f"{Fore.RED}保存文件时发生错误：{e}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        app = LuohanqianDivination()
        app.run()
    except Exception as e:
        print(f"{Fore.RED}程序启动失败: {e}{Style.RESET_ALL}")
        sys.exit(1)