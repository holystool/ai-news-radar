import json
import os

def extract_summary():
    file_path = 'data/waytoagi-7d.json'
    
    if not os.path.exists(file_path):
        return "今日 WaytoAGI 暂无更新记录。"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 核心修正：直接定位到 updates_today 列表
        updates = data.get('updates_today', [])
        
        if not updates:
            return "今日 WaytoAGI 暂无文章更新。"

        summary = "📢 **WaytoAGI 今日更新摘要：**\n\n"
        
        # 遍历更新列表
        for item in updates:
            title = item.get('title', '无标题内容')
            url = item.get('url', '#')
            
            # 由于标题通常很长且包含了简介，我们直接展示，并做一个长度截断保护
            display_text = title if len(title) <= 200 else title[:200] + "..."
            
            summary += f"🔹 {display_text}\n🔗 [查看原文]({url})\n\n"
        
        return summary
    except Exception as e:
        return f"解析过程发生技术错误: {str(e)}"

if __name__ == "__main__":
    content = extract_summary()
    with open('waytoagi_summary.txt', 'w', encoding='utf-8') as f:
        f.write(content + "\n")
