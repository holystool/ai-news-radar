import json
import os
import re

def extract_summary():
    # 路径确保正确
    file_path = 'data/waytoagi-7d.json'
    
    if not os.path.exists(file_path):
        return "今日 WaytoAGI 暂无更新记录。"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        # 兼容性处理：如果 raw_data 是列表，我们需要遍历它
        items_list = raw_data if isinstance(raw_data, list) else []
        
        valid_items = []
        for entry in items_list:
            # 关键修正：你的 JSON 结构中，真正的数据在 entry['item'] 里面
            # 或者是 entry 直接就是数据
            item = entry.get('item', entry) if isinstance(entry, dict) else {}
            
            title = item.get('title') or item.get('name')
            if title:
                valid_items.append(item)
        
        if not valid_items:
            return "WaytoAGI 列表中未发现有效文章内容（解析路径未匹配）。"

        # 取最新的 5 条，因为看你截图今天更新挺多的
        top_news = valid_items[:5]

        summary = "📢 **WaytoAGI 重点内容摘要：**\n\n"
        for item in top_news:
            title = item.get('title') or item.get('name') or "无标题"
            # 提取描述，优先取 description，没有就取 content
            desc = item.get('description') or item.get('content') or ""
            
            # 清理 HTML 标签
            clean_desc = re.sub(r'<[^>]+>', '', str(desc))
            clean_desc = clean_desc.replace('&nbsp;', ' ').strip()
            
            if len(clean_desc) > 120:
                clean_desc = clean_desc[:120] + "..."
            elif not clean_desc:
                clean_desc = "（请点击链接查看详情）"
                
            summary += f"🔹 **{title}**\n{clean_desc}\n\n"
        
        return summary
    except Exception as e:
        return f"解析过程发生技术错误: {str(e)}"

if __name__ == "__main__":
    content = extract_summary()
    with open('waytoagi_summary.txt', 'w', encoding='utf-8') as f:
        f.write(content + "\n")
