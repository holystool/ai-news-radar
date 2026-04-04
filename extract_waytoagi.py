import json
import os

def extract_summary():
    file_path = 'data/waytoagi-7d.json'
    
    if not os.path.exists(file_path):
        return "今日 WaytoAGI 暂无更新记录。"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        # 核心修正：判断数据结构。如果是字典，取其 'items' 列表
        if isinstance(raw_data, dict) and 'items' in raw_data:
            data = raw_data['items']
        elif isinstance(raw_data, list):
            data = raw_data
        else:
            return "WaytoAGI 数据格式异常，无法解析。"
        
        # 只取前 3 条最新的
        top_news = data[:3]
        
        if not top_news:
            return "WaytoAGI 列表目前为空。"

        summary = "📢 **WaytoAGI 最近更新摘要：**\n\n"
        for item in top_news:
            title = item.get('title', '无标题')
            # 提取描述并简单清理（去除可能的 HTML 标签）
            desc = item.get('description', '暂无简介')
            if desc:
                # 简单截取前 100 个字符
                desc = desc.replace('<br>', '\n').strip()[:100]
            summary += f"🔹 **{title}**\n{desc}...\n\n"
        
        return summary
    except Exception as e:
        # 这里会捕获具体的错误原因，方便排查
        return f"解析 WaytoAGI 内容时出错: {str(e)}"

if __name__ == "__main__":
    content = extract_summary()
    with open('waytoagi_summary.txt', 'w', encoding='utf-8') as f:
        f.write(content + "\n")
