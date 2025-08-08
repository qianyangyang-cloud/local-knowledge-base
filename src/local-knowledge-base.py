import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import json
import threading
import requests
from pathlib import Path
import time

# 尝试导入Word文档读取库
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import win32com.client
    DOC_AVAILABLE = True
except ImportError:
    DOC_AVAILABLE = False

class LocalKnowledgeBase:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("本地知识库 - Local Knowledge Base v1.0")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # 数据存储
        self.api_key = ""
        self.selected_model = "deepseek"
        self.files_content = {}
        self.chat_messages = []
        
        # 支持的文件格式
        self.supported_extensions = {
            '.txt', '.md', '.json', '.js', '.py', '.java', 
            '.cpp', '.c', '.html', '.css', '.xml', '.yaml', 
            '.yml', '.ini', '.cfg', '.log', '.doc', '.docx'
        }
        
        self.setup_ui()
        self.update_status()
        
    def setup_ui(self):
        # 创建主容器
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧面板
        left_frame = ttk.Frame(main_container, width=350)
        main_container.add(left_frame, weight=0)
        
        # 右侧面板
        right_frame = ttk.Frame(main_container)
        main_container.add(right_frame, weight=1)
        
        self.setup_left_panel(left_frame)
        self.setup_right_panel(right_frame)
        
    def setup_left_panel(self, parent):
        # 标题
        title_label = ttk.Label(parent, text="🤖 本地知识库", font=("Arial", 16, "bold"))
        title_label.pack(pady=(10, 20))
        
        # 连接状态
        self.status_frame = ttk.Frame(parent)
        self.status_frame.pack(fill=tk.X, padx=10, pady=(0, 20))
        
        self.status_label = ttk.Label(self.status_frame, text="❌ 请配置API Key和文件", 
                                     foreground="red", font=("Arial", 10, "bold"))
        self.status_label.pack()
        
        # AI模型配置区
        model_frame = ttk.LabelFrame(parent, text="🔧 AI模型配置", padding=15)
        model_frame.pack(fill=tk.X, padx=10, pady=(0, 15))
        
        ttk.Label(model_frame, text="选择模型:").pack(anchor=tk.W)
        self.model_var = tk.StringVar(value="deepseek")
        model_combo = ttk.Combobox(model_frame, textvariable=self.model_var, 
                                  values=["deepseek"], state="readonly")
        model_combo.pack(fill=tk.X, pady=(5, 10))
        model_combo.bind("<<ComboboxSelected>>", self.on_model_change)
        
        ttk.Label(model_frame, text="API Key:").pack(anchor=tk.W)
        self.api_key_var = tk.StringVar()
        api_entry = ttk.Entry(model_frame, textvariable=self.api_key_var, show="*")
        api_entry.pack(fill=tk.X, pady=(5, 10))
        api_entry.bind("<KeyRelease>", self.on_api_key_change)
        
        ttk.Label(model_frame, text="DeepSeek API: https://platform.deepseek.com/", 
                 font=("Arial", 8), foreground="gray").pack(anchor=tk.W)
        
        # 文件管理区
        file_frame = ttk.LabelFrame(parent, text="📁 文件管理", padding=15)
        file_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # 文件操作按钮
        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        select_folder_btn = ttk.Button(btn_frame, text="📂 选择文件夹", 
                                      command=self.select_folder)
        select_folder_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        browse_folder_btn = ttk.Button(btn_frame, text="🔍 浏览文件夹", 
                                      command=self.browse_folder)
        browse_folder_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        select_files_btn = ttk.Button(btn_frame, text="📄 选择文件", 
                                     command=self.select_files)
        select_files_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_btn = ttk.Button(btn_frame, text="🗑️ 清空", command=self.clear_files)
        clear_btn.pack(side=tk.RIGHT)
        
        # 当前路径显示
        self.path_label = ttk.Label(file_frame, text="未选择路径", 
                                   font=("Arial", 9), foreground="gray")
        self.path_label.pack(anchor=tk.W, pady=(0, 5))
        
        # 文件列表
        ttk.Label(file_frame, text="已加载文件:").pack(anchor=tk.W)
        
        # 创建Treeview来显示文件
        self.file_tree = ttk.Treeview(file_frame, height=8)
        self.file_tree.heading('#0', text='文件名', anchor=tk.W)
        self.file_tree.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # 滚动条
        scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=scrollbar.set)
        
    def setup_right_panel(self, parent):
        # 标题栏
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        ttk.Label(header_frame, text="💬 AI助手对话", font=("Arial", 14, "bold")).pack(anchor=tk.W)
        ttk.Label(header_frame, text="基于您的文档内容进行智能问答", 
                 font=("Arial", 10), foreground="gray").pack(anchor=tk.W)
        
        # 聊天区域
        chat_frame = ttk.Frame(parent)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
        self.chat_area = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, state=tk.DISABLED,
                                                  font=("Arial", 10), bg="#f8f9fa")
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        
        # 显示欢迎消息
        self.display_welcome_message()
        
        # 输入区域
        input_frame = ttk.Frame(parent)
        input_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # 输入框和发送按钮
        input_container = ttk.Frame(input_frame)
        input_container.pack(fill=tk.X, pady=(5, 0))
        
        self.input_text = tk.Text(input_container, height=3, wrap=tk.WORD, font=("Arial", 10))
        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.send_button = ttk.Button(input_container, text="发送", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)
        
        # 绑定Enter键发送
        self.input_text.bind("<KeyPress-Return>", self.on_enter_key)
        
        # 初始状态禁用发送按钮
        self.send_button.config(state=tk.DISABLED)
        
    def display_welcome_message(self):
        welcome_text = """👋 欢迎使用本地知识库！

📋 使用步骤：
1. 在左侧配置DeepSeek API Key
2. 选择文件夹或文件加载文档
3. 在下方输入问题开始对话

💡 建议的问题：
• 这些文件的主要内容是什么？
• 帮我总结关键信息
• 解释一下代码逻辑
• 有什么重要概念？

🔒 隐私保护：所有文件都在本地处理，不会上传到服务器
"""
        
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, welcome_text)
        self.chat_area.config(state=tk.DISABLED)
        
    def read_file_content(self, file_path):
        """读取文件内容，支持多种格式包括Word文档"""
        file_path = Path(file_path)
        file_ext = file_path.suffix.lower()
        
        try:
            # Word文档处理
            if file_ext == '.docx':
                if DOCX_AVAILABLE:
                    doc = Document(file_path)
                    content = []
                    for paragraph in doc.paragraphs:
                        if paragraph.text.strip():
                            content.append(paragraph.text.strip())
                    return '\n'.join(content)
                else:
                    return f"[需要安装python-docx库来读取.docx文件]\n文件路径: {file_path}"
                    
            elif file_ext == '.doc':
                if DOC_AVAILABLE:
                    word = win32com.client.Dispatch("Word.Application")
                    word.Visible = False
                    doc = word.Documents.Open(str(file_path))
                    content = doc.Content.Text
                    doc.Close()
                    word.Quit()
                    return content
                else:
                    return f"[需要安装pywin32库或Microsoft Word来读取.doc文件]\n文件路径: {file_path}"
                    
            # 普通文本文件
            else:
                return file_path.read_text(encoding='utf-8', errors='ignore')
                
        except Exception as e:
            return f"[读取失败: {str(e)}]\n文件路径: {file_path}"
        
    def select_folder(self):
        folder_path = filedialog.askdirectory(title="选择文件夹")
        if folder_path:
            self.load_folder_files(folder_path)
            
    def select_files(self):
        file_types = [
            ("Word文档", "*.doc;*.docx"),
            ("文本文件", "*.txt"),
            ("Markdown文件", "*.md"),
            ("代码文件", "*.js;*.py;*.java;*.cpp;*.c"),
            ("配置文件", "*.json;*.xml;*.yaml;*.yml"),
            ("所有支持的文件", "*.txt;*.md;*.js;*.py;*.java;*.cpp;*.c;*.json;*.xml;*.doc;*.docx"),
            ("所有文件", "*.*")
        ]
        
        files = filedialog.askopenfilenames(title="选择文件", filetypes=file_types)
        if files:
            self.load_selected_files(files)
            
    def load_folder_files(self, folder_path):
        try:
            self.files_content.clear()
            self.path_label.config(text=f"路径: {folder_path}")
            
            # 遍历文件夹
            folder = Path(folder_path)
            loaded_files = []
            
            for file_path in folder.rglob("*"):
                if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                    try:
                        content = self.read_file_content(file_path)
                        self.files_content[str(file_path)] = content
                        loaded_files.append(file_path.name)
                    except Exception as e:
                        print(f"读取文件失败 {file_path}: {e}")
                        
            self.update_file_display(loaded_files)
            self.update_status()
            
            if loaded_files:
                messagebox.showinfo("成功", f"成功加载 {len(loaded_files)} 个文件")
            else:
                messagebox.showwarning("警告", "该文件夹中没有找到支持的文件类型")
                
        except Exception as e:
            messagebox.showerror("错误", f"加载文件夹失败: {str(e)}")
            
    def load_selected_files(self, file_paths):
        try:
            self.files_content.clear()
            loaded_files = []
            
            for file_path in file_paths:
                try:
                    content = self.read_file_content(file_path)
                    self.files_content[file_path] = content
                    loaded_files.append(Path(file_path).name)
                except Exception as e:
                    print(f"读取文件失败 {file_path}: {e}")
                    
            if file_paths:
                self.path_label.config(text=f"已选择 {len(file_paths)} 个文件")
                
            self.update_file_display(loaded_files)
            self.update_status()
            
            if loaded_files:
                messagebox.showinfo("成功", f"成功加载 {len(loaded_files)} 个文件")
                
        except Exception as e:
            messagebox.showerror("错误", f"加载文件失败: {str(e)}")
            
    def update_file_display(self, file_names):
        # 清空现有项
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
            
        # 添加文件项
        for i, filename in enumerate(file_names):
            self.file_tree.insert('', 'end', text=f"📄 {filename}")
            
    def clear_files(self):
        self.files_content.clear()
        self.path_label.config(text="未选择路径")
        self.update_file_display([])
        self.update_status()
        
    def on_model_change(self, event):
        self.selected_model = self.model_var.get()
        self.update_status()
        
    def on_api_key_change(self, event):
        self.api_key = self.api_key_var.get()
        self.update_status()
        
    def update_status(self):
        has_api_key = bool(self.api_key.strip())
        has_files = bool(self.files_content)
        
        if has_api_key and has_files:
            self.status_label.config(text="✅ 已就绪，可以开始对话", foreground="green")
            self.send_button.config(state=tk.NORMAL)
        else:
            missing = []
            if not has_api_key:
                missing.append("API Key")
            if not has_files:
                missing.append("文件")
            
            self.status_label.config(text=f"❌ 请配置: {', '.join(missing)}", foreground="red")
            self.send_button.config(state=tk.DISABLED)
            
    def on_enter_key(self, event):
        if event.state & 0x1:  # Shift+Enter
            return  # 允许换行
        else:  # 仅Enter
            self.send_message()
            return "break"  # 阻止默认行为
            
    def send_message(self):
        message = self.input_text.get("1.0", tk.END).strip()
        if not message:
            return
            
        # 清空输入框
        self.input_text.delete("1.0", tk.END)
        
        # 显示用户消息
        self.add_message("user", message)
        
        # 禁用发送按钮
        self.send_button.config(state=tk.DISABLED, text="发送中...")
        
        # 在后台线程发送请求
        threading.Thread(target=self.send_api_request, args=(message,), daemon=True).start()
        
    def add_message(self, sender, message):
        self.chat_area.config(state=tk.NORMAL)
        
        timestamp = time.strftime("%H:%M:%S")
        
        if sender == "user":
            self.chat_area.insert(tk.END, f"\n👤 您 ({timestamp})\n", "user_name")
            self.chat_area.insert(tk.END, f"{message}\n", "user_msg")
        else:
            self.chat_area.insert(tk.END, f"\n🤖 AI助手 ({timestamp})\n", "ai_name")
            self.chat_area.insert(tk.END, f"{message}\n", "ai_msg")
            
        # 配置文本样式
        self.chat_area.tag_config("user_name", foreground="#0066cc", font=("Arial", 10, "bold"))
        self.chat_area.tag_config("user_msg", foreground="#333333")
        self.chat_area.tag_config("ai_name", foreground="#009900", font=("Arial", 10, "bold"))
        self.chat_area.tag_config("ai_msg", foreground="#333333")
        
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
        
    def send_api_request(self, message):
        try:
            # 准备上下文
            context = ""
            if self.files_content:
                context = "\n\n以下是用户提供的文档内容：\n"
                for file_path, content in self.files_content.items():
                    filename = Path(file_path).name
                    context += f"\n=== {filename} ===\n{content[:5000]}\n"
                    
            system_prompt = f"你是一个专业的AI助手，专门帮助用户分析和理解文档内容。{context}\n\n请基于提供的文档内容回答用户问题。"
            
            # API请求
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                reply = result["choices"][0]["message"]["content"]
                
                # 在主线程更新UI
                self.root.after(0, lambda: self.add_message("assistant", reply))
            else:
                error_msg = f"API请求失败 ({response.status_code})"
                if response.status_code == 401:
                    error_msg += "\n请检查API Key是否正确"
                elif response.status_code == 429:
                    error_msg += "\n请求过于频繁，请稍后再试"
                    
                self.root.after(0, lambda: self.add_message("assistant", f"❌ {error_msg}"))
                
        except requests.exceptions.Timeout:
            self.root.after(0, lambda: self.add_message("assistant", "❌ 请求超时，请检查网络连接"))
        except requests.exceptions.RequestException as e:
            self.root.after(0, lambda: self.add_message("assistant", f"❌ 网络错误: {str(e)}"))
        except Exception as e:
            self.root.after(0, lambda: self.add_message("assistant", f"❌ 发生错误: {str(e)}"))
        finally:
            # 重新启用发送按钮
            self.root.after(0, lambda: self.send_button.config(state=tk.NORMAL, text="发送"))
            self.root.after(0, self.update_status)
            
    def browse_folder(self):
        """打开文件浏览器"""
        # 优先从桌面开始，如果桌面不存在则用用户主目录
        desktop = Path.home() / "Desktop"
        if desktop.exists():
            initial_dir = desktop
        else:
            initial_dir = Path.home()
        self.show_file_browser(initial_dir)
            
    def show_file_selection_dialog(self, available_files, folder_path):
        """显示文件选择对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"选择文件 - {Path(folder_path).name}")
        dialog.geometry("600x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 顶部说明
        info_frame = ttk.Frame(dialog)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(info_frame, text=f"找到 {len(available_files)} 个支持的文件，请选择要加载的文件:", 
                 font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        # 文件列表框
        list_frame = ttk.Frame(dialog)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # 创建列表框和滚动条
        listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED, font=("Arial", 9))
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)
        
        # 填充文件列表
        for file_path in available_files:
            try:
                file_size = file_path.stat().st_size
                if file_size < 1024:
                    size_str = f"{file_size}B"
                elif file_size < 1024 * 1024:
                    size_str = f"{file_size/1024:.1f}KB"
                else:
                    size_str = f"{file_size/(1024*1024):.1f}MB"
                    
                # 显示相对路径和文件大小
                relative_path = file_path.relative_to(Path(folder_path))
                display_text = f"{relative_path} ({size_str})"
                listbox.insert(tk.END, display_text)
            except:
                listbox.insert(tk.END, str(file_path.name))
        
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 底部按钮
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        def select_all():
            listbox.select_set(0, tk.END)
            
        def load_selected():
            selected_indices = listbox.curselection()
            if not selected_indices:
                messagebox.showwarning("提示", "请至少选择一个文件")
                return
                
            selected_files = [available_files[i] for i in selected_indices]
            dialog.destroy()
            
            # 加载选中的文件
            self.load_selected_files([str(f) for f in selected_files])
            
        ttk.Button(button_frame, text="全选", command=select_all).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="加载选中文件", command=load_selected).pack(side=tk.RIGHT, padx=(0, 5))
        
        # 添加提示
        tip_label = ttk.Label(button_frame, text="提示: 按住Ctrl键可多选文件", 
                             font=("Arial", 8), foreground="gray")
        tip_label.pack(side=tk.LEFT, padx=(20, 0))
        
    def show_file_browser(self, initial_dir):
        """显示类似Windows资源管理器的文件浏览器"""
        browser = tk.Toplevel(self.root)
        browser.title("文件浏览器 - 选择文件和文件夹")
        browser.geometry("900x650")
        browser.transient(self.root)
        browser.grab_set()
        
        self.current_path = Path(initial_dir)
        self.selected_files = {}
        
        # 创建主框架
        main_frame = ttk.Frame(browser)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 顶部导航栏
        nav_frame = ttk.Frame(main_frame)
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(nav_frame, text="⬅️ 上级", command=lambda: self.navigate_up(browser)).pack(side=tk.LEFT)
        ttk.Button(nav_frame, text="🏠 桌面", command=lambda: self.navigate_to_desktop(browser)).pack(side=tk.LEFT, padx=(5, 0))
        ttk.Button(nav_frame, text="📁 我的文档", command=lambda: self.navigate_to_documents(browser)).pack(side=tk.LEFT, padx=(5, 0))
        
        # 路径显示
        self.path_var = tk.StringVar(value=str(self.current_path))
        path_entry = ttk.Entry(nav_frame, textvariable=self.path_var, state="readonly")
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        # 中间文件列表区域
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 创建树形视图显示文件和文件夹
        columns = ("type", "size", "modified")
        self.browser_tree = ttk.Treeview(list_frame, columns=columns, show="tree headings", height=18)
        
        # 设置列标题
        self.browser_tree.heading("#0", text="名称", anchor=tk.W)
        self.browser_tree.heading("type", text="类型", anchor=tk.W)
        self.browser_tree.heading("size", text="大小", anchor=tk.E)
        self.browser_tree.heading("modified", text="修改时间", anchor=tk.W)
        
        # 设置列宽度
        self.browser_tree.column("#0", width=350, minwidth=200)
        self.browser_tree.column("type", width=100, minwidth=80)
        self.browser_tree.column("size", width=100, minwidth=80)
        self.browser_tree.column("modified", width=150, minwidth=100)
        
        # 滚动条
        tree_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.browser_tree.yview)
        self.browser_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.browser_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定事件
        self.browser_tree.bind("<Double-1>", lambda e: self.on_item_double_click(e, browser))
        self.browser_tree.bind("<Button-1>", lambda e: self.on_item_click(e))
        
        # 底部状态和按钮区
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X)
        
        # 状态信息
        self.browser_status_var = tk.StringVar(value="准备就绪")
        status_label = ttk.Label(bottom_frame, textvariable=self.browser_status_var)
        status_label.pack(side=tk.LEFT)
        
        # 按钮
        button_frame = ttk.Frame(bottom_frame)
        button_frame.pack(side=tk.RIGHT)
        
        ttk.Button(button_frame, text="全选支持的文件", command=self.select_all_supported_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="取消", command=browser.destroy).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="加载选中文件", command=lambda: self.load_selected_from_browser(browser)).pack(side=tk.LEFT)
        
        # 初始化显示
        self.refresh_browser_view(browser)
        
    def navigate_up(self, browser):
        """导航到上级目录"""
        parent = self.current_path.parent
        if parent != self.current_path:
            self.current_path = parent
            self.refresh_browser_view(browser)
            
    def navigate_to_desktop(self, browser):
        """导航到桌面"""
        # 尝试多种桌面路径
        possible_desktop_paths = [
            Path.home() / "Desktop",
            Path.home() / "桌面",
            Path("C:/Users") / Path.home().name / "Desktop",
            Path("C:/Users") / Path.home().name / "桌面"
        ]
        
        desktop = None
        for path in possible_desktop_paths:
            if path.exists():
                desktop = path
                break
                
        if desktop:
            self.current_path = desktop
        else:
            self.current_path = Path.home()
            
        self.refresh_browser_view(browser)
        
    def navigate_to_documents(self, browser):
        """导航到文档文件夹"""
        docs = Path.home() / "Documents"
        if docs.exists():
            self.current_path = docs
        else:
            self.current_path = Path.home()
        self.refresh_browser_view(browser)
        
    def refresh_browser_view(self, browser):
        """刷新浏览器视图"""
        # 清空现有内容
        for item in self.browser_tree.get_children():
            self.browser_tree.delete(item)
            
        # 更新路径显示
        self.path_var.set(str(self.current_path))
        
        try:
            items = []
            
            # 获取文件夹和文件
            for item in self.current_path.iterdir():
                try:
                    if item.is_dir() and not item.name.startswith('.'):
                        # 文件夹
                        modified = time.strftime("%Y-%m-%d %H:%M", time.localtime(item.stat().st_mtime))
                        items.append(("📁", item.name, "文件夹", "", modified, item, "folder"))
                        
                    elif item.is_file():
                        # 文件
                        file_ext = item.suffix.lower()
                        is_supported = file_ext in self.supported_extensions
                        
                        # 获取文件信息
                        stat = item.stat()
                        size = stat.st_size
                        if size < 1024:
                            size_str = f"{size}B"
                        elif size < 1024 * 1024:
                            size_str = f"{size/1024:.1f}KB"
                        else:
                            size_str = f"{size/(1024*1024):.1f}MB"
                            
                        modified = time.strftime("%Y-%m-%d %H:%M", time.localtime(stat.st_mtime))
                        
                        # 根据文件类型选择图标
                        if is_supported:
                            if file_ext in ['.doc', '.docx']:
                                icon = "📝"
                            elif file_ext in ['.txt', '.md']:
                                icon = "📄"
                            elif file_ext in ['.js', '.py', '.java', '.cpp', '.c', '.html', '.css']:
                                icon = "💻"
                            elif file_ext in ['.json', '.xml', '.yaml', '.yml']:
                                icon = "⚙️"
                            else:
                                icon = "📄"
                        else:
                            icon = "📄"
                            
                        file_type = f"{file_ext.upper()[1:]}文件" if file_ext else "文件"
                        items.append((icon, item.name, file_type, size_str, modified, item, "file"))
                        
                except (OSError, PermissionError):
                    continue
            
            # 排序：文件夹在前，然后是文件，都按名称排序
            folders = sorted([item for item in items if item[6] == "folder"], key=lambda x: x[1].lower())
            files = sorted([item for item in items if item[6] == "file"], key=lambda x: x[1].lower())
            
            # 插入到树形视图
            for icon, name, type_, size, modified, path_obj, item_type in folders + files:
                is_supported = item_type == "file" and path_obj.suffix.lower() in self.supported_extensions
                
                item_id = self.browser_tree.insert("", "end", 
                    text=f"{icon} {name}", 
                    values=(type_, size, modified),
                    tags=("supported" if is_supported else "normal",))
                    
                # 存储路径信息
                self.browser_tree.set(item_id, "path", str(path_obj))
                self.browser_tree.set(item_id, "item_type", item_type)
                self.browser_tree.set(item_id, "is_supported", str(is_supported))
            
            # 配置标签样式
            self.browser_tree.tag_configure("supported", background="#e8f5e8")
            self.browser_tree.tag_configure("normal", background="white")
            
            # 更新状态
            supported_count = len([item for item in files if item[5].suffix.lower() in self.supported_extensions])
            total_files = len(files)
            word_count = len([item for item in files if item[5].suffix.lower() in ['.doc', '.docx']])
            
            status_text = f"共 {total_files} 个文件，{supported_count} 个支持格式"
            if word_count > 0:
                status_text += f"，{word_count} 个Word文档"
            status_text += f"，已选择 {len(self.selected_files)} 个"
            
            self.browser_status_var.set(status_text)
            
        except PermissionError:
            messagebox.showerror("错误", f"没有权限访问文件夹: {self.current_path}")
        except Exception as e:
            messagebox.showerror("错误", f"读取文件夹失败: {str(e)}")
            
    def on_item_double_click(self, event, browser):
        """双击事件：进入文件夹或选择文件"""
        selection = self.browser_tree.selection()
        if not selection:
            return
            
        item = selection[0]
        item_type = self.browser_tree.set(item, "item_type")
        path_str = self.browser_tree.set(item, "path")
        
        if item_type == "folder":
            # 进入文件夹
            self.current_path = Path(path_str)
            self.refresh_browser_view(browser)
        elif item_type == "file":
            # 切换文件选择状态
            self.toggle_file_selection(item)
            
    def on_item_click(self, event):
        """单击事件：选择文件"""
        selection = self.browser_tree.selection()
        if not selection:
            return
            
        item = selection[0]
        item_type = self.browser_tree.set(item, "item_type")
        
        if item_type == "file":
            self.toggle_file_selection(item)
            
    def toggle_file_selection(self, item):
        """切换文件选择状态"""
        path_str = self.browser_tree.set(item, "path")
        is_supported = self.browser_tree.set(item, "is_supported") == "True"
        
        if not is_supported:
            messagebox.showinfo("提示", "此文件类型不受支持")
            return
            
        current_text = self.browser_tree.item(item, "text")
        
        if path_str in self.selected_files:
            # 取消选择
            del self.selected_files[path_str]
            # 移除复选标记
            new_text = current_text.replace("✅ ", "")
            self.browser_tree.item(item, text=new_text)
        else:
            # 选择文件
            self.selected_files[path_str] = True
            # 添加复选标记
            if not current_text.startswith("✅ "):
                new_text = "✅ " + current_text
                self.browser_tree.item(item, text=new_text)
                
        # 更新状态显示
        supported_files = sum(1 for child in self.browser_tree.get_children() 
                            if self.browser_tree.set(child, "is_supported") == "True")
        total_files = sum(1 for child in self.browser_tree.get_children() 
                         if self.browser_tree.set(child, "item_type") == "file")
        word_files = sum(1 for child in self.browser_tree.get_children() 
                        if self.browser_tree.set(child, "item_type") == "file" and 
                        Path(self.browser_tree.set(child, "path")).suffix.lower() in ['.doc', '.docx'])
        
        status_text = f"共 {total_files} 个文件，{supported_files} 个支持格式"
        if word_files > 0:
            status_text += f"，{word_files} 个Word文档"
        status_text += f"，已选择 {len(self.selected_files)} 个"
        
        self.browser_status_var.set(status_text)
        
    def select_all_supported_files(self):
        """选择所有支持的文件"""
        for item in self.browser_tree.get_children():
            item_type = self.browser_tree.set(item, "item_type")
            is_supported = self.browser_tree.set(item, "is_supported") == "True"
            
            if item_type == "file" and is_supported:
                path_str = self.browser_tree.set(item, "path")
                if path_str not in self.selected_files:
                    self.selected_files[path_str] = True
                    current_text = self.browser_tree.item(item, "text")
                    if not current_text.startswith("✅ "):
                        self.browser_tree.item(item, text="✅ " + current_text)
                        
        # 更新状态
        supported_files = sum(1 for child in self.browser_tree.get_children() 
                            if self.browser_tree.set(child, "is_supported") == "True")
        total_files = sum(1 for child in self.browser_tree.get_children() 
                         if self.browser_tree.set(child, "item_type") == "file")
        word_files = sum(1 for child in self.browser_tree.get_children() 
                        if self.browser_tree.set(child, "item_type") == "file" and 
                        Path(self.browser_tree.set(child, "path")).suffix.lower() in ['.doc', '.docx'])
        
        status_text = f"共 {total_files} 个文件，{supported_files} 个支持格式"
        if word_files > 0:
            status_text += f"，{word_files} 个Word文档"
        status_text += f"，已选择 {len(self.selected_files)} 个"
        
        self.browser_status_var.set(status_text)
        
    def load_selected_from_browser(self, browser):
        """从浏览器加载选中的文件"""
        if not self.selected_files:
            messagebox.showwarning("提示", "请先选择要加载的文件")
            return
            
        file_paths = list(self.selected_files.keys())
        browser.destroy()
        self.load_selected_files(file_paths)
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LocalKnowledgeBase()
    app.run()