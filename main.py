import re

def is_excluded_message(msg):
    # 若訊息包含 [貼圖] [影片] [照片] 則直接忽略該整則訊息
    exclude_keywords = ["[貼圖]", "[影片]", "[照片]"]
    for kw in exclude_keywords:
        if kw in msg:
            return True
    return False

def remove_non_chinese(text):
    # 只保留中文字元，其他全部移除
    # \u4e00-\u9fff為常用中文字元範圍
    return re.sub(r"[^\u4e00-\u9fff]", "", text)

def main():
    filename = "line.txt"
    user_word_count = {}

    time_pattern = r"((上|下)午\d{1,2}:\d{2})"
    
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # 檢查此行是否包含時間（即是一則訊息的行）
            match = re.search(time_pattern, line)
            if match:
                # 擷取時間字串
                time_str = match.group(1)
                # 將時間從行中拆分，取得後半段 (使用者與訊息)
                parts = line.split(time_str, maxsplit=1)
                if len(parts) < 2:
                    continue
                after_time = parts[1].strip()
                
                # 使用正則盡量以 "至少兩個空白" 或 tab 做區隔，確保取得使用者與訊息兩部分
                # 或者嘗試只分一次：
                split_line = re.split(r"\s+", after_time, maxsplit=1)
                if len(split_line) < 2:
                    # 若無法正常分出使用者與訊息，跳過
                    continue
                user_name = split_line[0].strip()
                msg = split_line[1].strip()

                # 檢查是否排除該訊息
                if is_excluded_message(msg):
                    continue

                # 移除非中文字元（不計算標點、英文、數字）
                clean_msg = remove_non_chinese(msg)
                count = len(clean_msg)

                if user_name not in user_word_count:
                    user_word_count[user_name] = 0
                user_word_count[user_name] += count

    # 輸出結果
    for user, count in user_word_count.items():
        print(f"{user} 的總字數: {count}")

if __name__ == "__main__":
    main()
