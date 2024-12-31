# auto_clicker_2.py
import pygetwindow as gw
import pyautogui
import time
import keyboard
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from coordinates import (get_all_coordinates, get_enemy_coordinates, 
                        get_team_coordinates)
from config import *

def convert_coordinates(coordinates, current_width, current_height):
    """
    將基於1600x900解析度的座標轉換為目標視窗解析度的相對座標
    """
    scale_x = current_width / BASE_WIDTH
    scale_y = current_height / BASE_HEIGHT
    
    return [[int(x * scale_x), int(y * scale_y)] for x, y in coordinates]

def click_target(window_title, coordinates, interval, loop_count, auto_start, status_label, progress):
    try:
        status_label.config(text="執行中...")
        progress['maximum'] = len(coordinates)
        
        for i, pos in enumerate(coordinates):
            progress['value'] = i
            root.update_idletasks()

        windows = gw.getWindowsWithTitle(window_title)
        if not windows:
            messagebox.showerror("錯誤", f"找不到視窗：{window_title}")
            return
            
        target_window = windows[0]
        
        if target_window.isMinimized:
            messagebox.showerror("錯誤", "請先打開目標視窗再執行")
            return
            
        target_window.activate()
        time.sleep(0.5)
        
        # 獲取當前視窗的實際大小
        current_width = target_window.width
        current_height = target_window.height
        
        # 轉換座標為目標解析度
        scaled_coordinates = convert_coordinates(coordinates, current_width, current_height)
        
        print(f"視窗大小: {current_width}x{current_height}")
        print("開始執行連點... 按下 'ESC' 鍵以停止。")
        print(f"座標總數: {len(scaled_coordinates)}")

    # 主執行邏輯代碼
        for loop_index in range(loop_count):
            print(f"執行第 {loop_index + 1} 次迴圈")
            for i, pos in enumerate(scaled_coordinates):
                if keyboard.is_pressed('esc'):
                    print("已停止連點。")
                    progress['value'] = 0
                    status_label.config(text="已取消")
                    root.update_idletasks()
                    return

                pyautogui.click(target_window.left + pos[0], target_window.top + pos[1])
                progress['value'] = i + 1
                root.update_idletasks()

                # 檢查是否為開始座標
                original_pos = [pos[0] * BASE_WIDTH / current_width, 
                              pos[1] * BASE_HEIGHT / current_height]
                original_pos = (int(original_pos[0]), int(original_pos[1]))
                
                if original_pos == START_COORDINATE:
                    time.sleep(START_DELAY/1000)
                elif original_pos in SPECIAL_COORDINATES:
                    time.sleep(SPECIAL_COORDINATES[original_pos]/1000)
                else:
                    time.sleep(interval)

        # 自動開始邏輯
        if auto_start.get():
            status_label.config(text="正在執行自動開始點擊...")
            root.update_idletasks()
            time.sleep(AUTO_START_DELAY / 1000)

            auto_start_pos = convert_coordinates([AUTO_START_COORDINATE], current_width, current_height)[0]
            pyautogui.click(target_window.left + auto_start_pos[0], 
                          target_window.top + auto_start_pos[1])
            print("自動開始點擊已完成。")

        status_label.config(text="完成!")  # 更新狀態為完成
        progress['value'] = 0  # 重置進度條
        root.update_idletasks()  # 確保 UI 更新
        
    except Exception as e:
        progress['value'] = 0  # 確保進度條重置
        status_label.config(text="錯誤")  # 顯示錯誤狀態
        root.update_idletasks()  # 更新UI
        messagebox.showerror("錯誤", "請確認目標視窗已打開並在桌面上")
        print(f"錯誤詳情：{str(e)}")


def start_clicking_all(auto_start, status_label, progress):
    coordinates = get_all_coordinates()
    click_target(WINDOW_TITLE, coordinates, CLICK_INTERVAL, DEFAULT_LOOP_COUNT, 
                auto_start, status_label, progress)

def start_clicking_enemy(auto_start, status_label, progress):
    coordinates = get_enemy_coordinates()
    click_target(WINDOW_TITLE, coordinates, CLICK_INTERVAL, DEFAULT_LOOP_COUNT, 
                auto_start, status_label, progress)

def start_clicking_team(auto_start, status_label, progress):
    coordinates = get_team_coordinates()
    click_target(WINDOW_TITLE, coordinates, CLICK_INTERVAL, DEFAULT_LOOP_COUNT, 
                auto_start, status_label, progress)


def gui_main():
    global root
    root = tk.Tk()
    
    # 添加狀態標籤
    status_label = tk.Label(root, text="待機中...")
    status_label.pack(pady=5)
    
    # 添加進度條
    progress = ttk.Progressbar(root, length=200, mode='determinate')
    progress.pack(pady=5)

    root.title("自動檢舉")

    root.geometry("250x300")  # 增加視窗高度以容納新的選項
    
    # 新增自動開始的Checkbutton
    auto_start = tk.BooleanVar()
    auto_start_check = tk.Checkbutton(root, text="檢舉後開始列隊", variable=auto_start)
    auto_start_check.pack(pady=5)
    
    # 修改按鈕，傳入auto_start參數
    all_button = tk.Button(root, text="全部", command=lambda: start_clicking_all(auto_start, status_label, progress), width=10, height=2)
    all_button.pack(pady=5)
    
    enemy_button = tk.Button(root, text="對面", command=lambda: start_clicking_enemy(auto_start, status_label, progress), width=10, height=2, bg='red', fg='white')
    enemy_button.pack(pady=5)
    
    team_button = tk.Button(root, text="隊友", command=lambda: start_clicking_team(auto_start, status_label, progress), width=10, height=2, bg='blue', fg='white')
    team_button.pack(pady=5)
    
    root.mainloop()
    
if __name__ == "__main__":
    gui_main()
