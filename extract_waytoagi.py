import json
import os

def extract_summary():
    file_path = 'data/waytoagi-7d.json'
    
    if not os.path.exists(file_path):
        return "今日 WaytoAGI 暂无更新记录。"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        # 逻辑：判断是否是列表
        if isinstance(raw_data, list):
            # 观察发现第一条通常是元数据 (metadata)，我们从第二条开始尝试
            # 如果第一条就有 title，说明就是文章；如果没有，就切片 [1:4]
            if len(raw_data) > 0 and 'title' not in raw_data[0]:
                data = raw_data[1:]
            else:
                data = raw_data
        elif isinstance(raw_data, dict) and 'items' in raw_data:
            data = raw_data['items']
        else:
            return "WaytoAGI 数据格式不符合预期，请检查 JSON 内容。"
        
        # 取前 3 条
        top_news = data[:3]
        
        if not top_news:
            return "WaytoAGI 列表目前为空。"

        summary = "📢 **WaytoAGI 最近更新摘要：**\n\n"
        for item in top_news:
            title = item.get('title', '无标题')
            desc = item.get('description', '') or item.get('content', '暂无简介')
            
            # 清洗描述：去除 HTML 标签和多余空格
            if desc:
                import re
                desc = re.sub('<[^<]+?>', '', desc) # 正则去掉所有 HTML 标签
                desc = desc.replace('\n', ' ').strip()[:100]
                
            summary += f"🔹 **{title}**\n{desc}...\n\n"
        
        return summary
    except Exception as e:
        return f"解析出错: {str(e)}"

if __name__ == "__main__":
    content = extract_summary()
    with open('waytoagi_summary.txt', 'w', encoding='utf-8') as f:
        f.write(content + "\n")
