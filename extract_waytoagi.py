import json
import os
import urllib.parse

def extract_summary():
    file_path = 'data/waytoagi-7d.json'
    
    if not os.path.exists(file_path):
        return "今日 WaytoAGI 暂无更新记录。"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 定位今日更新列表
        updates = data.get('updates_today', [])
        
        if not updates:
            return "今日 WaytoAGI 暂无文章更新。"

        summary = "📢 WaytoAGI 今日更新摘要：\n\n"
        
        for item in updates:
            title = item.get('title', '无标题')
            
            # 使用 urllib.parse 确保标题中的特殊字符被正确编码，避免链接失效
            encoded_title = urllib.parse.quote(title)
            # 既然直接抓取真实链接不稳，我们采用搜索直达方案
            search_url = f"https://www.google.com/search?q=site:waytoagi.feishu.cn+{encoded_title}"
            
            summary += f"🔹 {title}\n🔗 [点击搜索并直达文章]({search_url})\n\n"
    
        return summary
    except Exception as e:
        return f"解析过程发生技术错误: {str(e)}"

if __name__ == "__main__":
    content = extract_summary()
    # 确保输出目录存在（如果需要）
    with open('waytoagi_summary.txt', 'w', encoding='utf-8') as f:
        f.write(content + "\n")
