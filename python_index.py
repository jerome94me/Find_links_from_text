import customtkinter as ctk
import re
import tkinter as tk
import webbrowser

class URLExtractorApp(ctk.CTk):
    """
    一個使用 CustomTkinter 創建的網址提取器應用程式。
    它從文字中查找並列出所有 URL，並提供複製和打開連結的功能。
    """
    def __init__(self):
        super().__init__()

        # 設定主視窗
        self.title("網址提取器")
        self.geometry("600x600")
        ctk.set_appearance_mode("light") # 設置外觀模式為亮色
        
        # 設定通用字體
        self.default_font = ctk.CTkFont(family="Microsoft JhengHei", size=12)
        self.heading_font = ctk.CTkFont(family="Microsoft JhengHei", size=24, weight="bold")
        self.subheading_font = ctk.CTkFont(family="Microsoft JhengHei", size=18, weight="bold")
        self.button_font = ctk.CTkFont(family="Microsoft JhengHei", size=14, weight="bold")
        self.copy_button_font = ctk.CTkFont(family="Microsoft JhengHei", size=11)

        # 主框架，用於居中和排版
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="white")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(3, weight=1)

        # 標題標籤
        self.title_label = ctk.CTkLabel(self.main_frame, text="網址提取器", font=self.heading_font)
        self.title_label.pack(pady=(20, 10))

        # 說明文字
        self.info_label = ctk.CTkLabel(self.main_frame, text="請將包含網址的文字貼到下方的方塊中，然後點擊按鈕來提取所有網址。", text_color="#6b7280", font=self.default_font)
        self.info_label.pack(pady=(0, 20))

        # 輸入文字區域
        self.text_input = ctk.CTkTextbox(self.main_frame, height=150, corner_radius=10, font=self.default_font)
        self.text_input.pack(fill="x", padx=20, pady=10)
        self.text_input.configure(wrap="word")

        # 按鈕框架
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(pady=(10, 20))
        
        # 提取網址按鈕
        self.extract_button = ctk.CTkButton(
            self.button_frame,
            text="提取網址",
            command=self.extract_urls,
            font=self.button_font,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            corner_radius=10,
            width=150
        )
        self.extract_button.pack(side="left", padx=10)
        
        # 複製所有網址按鈕
        self.copy_all_button = ctk.CTkButton(
            self.button_frame,
            text="複製所有網址",
            command=self.copy_all_urls,
            font=self.button_font,
            fg_color="#e5e7eb",
            text_color="#1f2937",
            hover_color="#d1d5db",
            corner_radius=10,
            width=150
        )
        self.copy_all_button.pack(side="left", padx=10)
        self.copy_all_button.pack_forget() # 預設隱藏

        # 結果標題
        self.result_title = ctk.CTkLabel(self.main_frame, text="提取的網址：", font=self.subheading_font)
        self.result_title.pack(pady=(10, 5))
        self.result_title.pack_forget() # 預設隱藏

        # 網址列表 (可滾動)
        self.url_list_frame = ctk.CTkScrollableFrame(self.main_frame, corner_radius=10, fg_color="#f3f4f6")
        self.url_list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # 訊息標籤
        self.message_box = ctk.CTkLabel(self.main_frame, text="", text_color="#6b7280", font=self.default_font)
        self.message_box.pack(pady=(5, 10))

    def extract_urls(self):
        """從輸入文字中提取所有網址並顯示。"""
        # 清空先前的結果和訊息
        self.clear_results()
        
        text = self.text_input.get("1.0", "end-1c")
        # 正則表達式匹配以 http:// 或 https:// 開頭的網址
        url_regex = r"https?:\/\/[^\s]+"
        urls = re.findall(url_regex, text)

        if urls:
            self.result_title.pack(pady=(10, 5))
            self.copy_all_button.pack(side="left", padx=10)
            
            for url in urls:
                self.add_url_to_list(url)
            
            self.message_box.configure(text=f"成功提取了 {len(urls)} 個網址。")
        else:
            self.message_box.configure(text="沒有找到任何網址。")

    def add_url_to_list(self, url):
        """將提取到的網址添加到可滾動的列表中。"""
        url_frame = ctk.CTkFrame(self.url_list_frame, fg_color="#e5e7eb", corner_radius=8)
        url_frame.pack(fill="x", pady=5, padx=5)
        
        # 容器用於放置連結和按鈕
        content_frame = ctk.CTkFrame(url_frame, fg_color="transparent")
        content_frame.pack(fill="x", expand=True, padx=10, pady=5)
        
        url_label = ctk.CTkLabel(content_frame, text=url, wraplength=400, font=self.default_font, justify="left", text_color="#3b82f6")
        url_label.pack(side="left", fill="x", expand=True)
        
        # 個別複製按鈕
        copy_button = ctk.CTkButton(
            content_frame,
            text="複製",
            command=lambda: self.copy_single_url(url),
            font=self.copy_button_font,
            fg_color="#d1d5db",
            text_color="#1f2937",
            hover_color="#9ca3af",
            corner_radius=8,
            width=60
        )
        copy_button.pack(side="right", padx=(10, 0))

        # 讓連結可被點擊
        url_label.bind("<Button-1>", lambda e, u=url: self.open_url(u))
        url_label.bind("<Enter>", lambda e: self.on_enter(url_label))
        url_label.bind("<Leave>", lambda e: self.on_leave(url_label))

    def open_url(self, url):
        """在預設瀏覽器中打開給定的 URL。"""
        webbrowser.open(url)

    def on_enter(self, widget):
        """滑鼠進入時改變連結樣式。"""
        widget.configure(text_color="#2563eb", font=ctk.CTkFont(family="Microsoft JhengHei", size=12, underline=True))

    def on_leave(self, widget):
        """滑鼠離開時恢復連結樣式。"""
        widget.configure(text_color="#3b82f6", font=ctk.CTkFont(family="Microsoft JhengHei", size=12, underline=False))

    def copy_single_url(self, url):
        """複製單一網址到剪貼簿。"""
        self.clipboard_clear()
        self.clipboard_append(url)
        self.message_box.configure(text="單一網址已複製到剪貼簿！")
        
    def copy_all_urls(self):
        """複製所有提取的網址到剪貼簿。"""
        urls = []
        # 遍歷所有子框架並獲取其中的標籤內容
        for widget in self.url_list_frame.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                # 這裡需要找到包含 URL 文本的標籤
                for sub_widget in widget.winfo_children():
                    for text_widget in sub_widget.winfo_children():
                        if isinstance(text_widget, ctk.CTkLabel):
                            urls.append(text_widget.cget("text"))
        
        if urls:
            self.clipboard_clear()
            self.clipboard_append("\n".join(urls))
            self.message_box.configure(text="所有網址已複製到剪貼簿！")
        else:
            self.message_box.configure(text="沒有網址可以複製。")

    def clear_results(self):
        """清除所有結果顯示。"""
        for widget in self.url_list_frame.winfo_children():
            widget.destroy()
        self.result_title.pack_forget()
        self.copy_all_button.pack_forget()
        self.message_box.configure(text="")

if __name__ == "__main__":
    app = URLExtractorApp()
    app.mainloop()
