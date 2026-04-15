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
            title = item.get('title', '无标题')
            # 既然真实链接抓不到，我们直接生成一个搜索链接
            # 搜索范围限制在 waytoagi 的飞书站点内
            search_url = f"https://www.google.com/search?q=site:waytoagi.feishu.cn+{title.replace(' ', '+')}"
            
            summary += f"🔹 **{title}**\n🔗 [搜索并直达文章]({search_url})\n\n"
    
        return summary
    except Exception as e:
        return f"解析过程发生技术错误: {str(e)}"

if __name__ == "__main__":
    content = extract_summary()
    with open('waytoagi_summary.txt', 'w', encoding='utf-8') as f:
        f.write(content + "\n")
