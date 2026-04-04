import json
import os

def extract_summary():
    file_path = 'data/waytoagi-7d.json'
    
    if not os.path.exists(file_path):
        return "今日 WaytoAGI 暂无更新记录。"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 只取前 3 条最新的，避免邮件太长
        top_news = data[:5]
        
        if not top_news:
            return "WaytoAGI 列表目前为空。"

        summary = "📢 **WaytoAGI 最近更新摘要：**\n\n"
        for item in top_news:
            title = item.get('title', '无标题')
            # 这里的 description 通常是 HTML 格式，我们简单处理一下或直接显示
            desc = item.get('description', '暂无简介').replace('<br>', '\n')[:120]
            summary += f"🔹 **{title}**\n{desc}...\n\n"
        
        return summary
    except Exception as e:
        return f"解析 WaytoAGI 内容时出错: {str(e)}"

if __name__ == "__main__":
    content = extract_summary()
    # 将结果写入临时文件
    with open('waytoagi_summary.txt', 'w', encoding='utf-8') as f:
        f.write(content)
