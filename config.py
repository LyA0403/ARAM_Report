# config.py

# 視窗設置
WINDOW_TITLE = "League of Legends"
WINDOW_WIDTH = 250
WINDOW_HEIGHT = 300

# 屏幕分辨率設置
BASE_WIDTH = 1600
BASE_HEIGHT = 900

# 點擊設置
CLICK_INTERVAL = 50 / 1000  # 50毫秒
DEFAULT_LOOP_COUNT = 1

# 延遲設置
AUTO_START_DELAY = 1800  # 毫秒

# 開始座標及其延遲
START_COORDINATE = (148, 134)
START_DELAY = 800  # 毫秒

# 特定座標及其延遲設置
SPECIAL_COORDINATES = {
    (650, 850): 200,  # 200毫秒延遲
    (804, 732): 100,  # 100毫秒延遲
    (658, 847): 0     # 自動開始座標
}

# 自動開始座標
AUTO_START_COORDINATE = (658, 847)