import json
import os
import re

def extract_summary():
    file_path = 'data/waytoagi-7d.json'
    
    if not os.path.exists(file_path):
        return "今日 WaytoAGI 暂无更新记录。"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        # 统一转化为列表处理
        items_list = []
        if isinstance(raw_data, list):
            items_list = raw_data
        elif isinstance(raw_data, dict):
            # 兼容不同项目可能使用的键名
            items_list = raw_data.get('items', raw_data.get('data', []))
        
        # 核心逻辑：只筛选出真正含有“标题”的条目，自动过滤掉元数据和空项
        valid_items = [
            i for i in items_list 
            if isinstance(i, dict) and (i.get('title') or i.get('name'))
        ]
        
        if not valid_items:
            return "WaytoAGI 列表中未发现有效文章内容。"

        # 取前 3 条最新的
        top_news = valid_items[:3]

        summary = "📢 **WaytoAGI 最近更新摘要：**\n\n"
        for item in top_news:
            # 兼容 title 或 name 字段
            title = item.get('title') or item.get('name') or "无标题"
            # 兼容 description, content 或 summary 字段
            desc = item.get('description') or item.get('content') or item.get('summary') or ""
            
            # 清洗 HTML 标签
            clean_desc = re.sub(r'<[^>]+>', '', str(desc))
            clean_desc = clean_desc.replace('\n', ' ').strip()
            
            # 截取长度
            if len(clean_desc) > 100:
                clean_desc = clean_desc[:100] + "..."
            elif not clean_desc:
                clean_desc = "点击链接查看详细内容"
                
            summary += f"🔹 **{title}**\n{clean_desc}\n\n"
        
        return summary
    except Exception as e:
        return f"解析过程发生技术错误: {str(e)}"

if __name__ == "__main__":
    content = extract_summary()
    with open('waytoagi_summary.txt', 'w', encoding='utf-8') as f:
        f.write(content + "\n")
