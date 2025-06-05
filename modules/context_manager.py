from modules.constants import CATEGORY_FIELDS

class ContextManager:
    def __init__(self):
        self.context = {
            "pokemon": None,
            "move": None,
            "ability": None,
            # 未来可扩展："item": None, "location": None 等
        }

    def update(self, category: str, entity_name: str):
        """更新指定类别的上下文实体"""
        if category in self.context:
            self.context[category] = entity_name
            print(f"[DEBUG] 上下文已更新：{category} ➜ {entity_name}")

    def get(self, category: str) -> str:
        """获取指定类别的当前上下文实体"""
        return self.context.get(category)
    
    def guess_category(fields):
        scores = {}
        for cat in CATEGORY_FIELDS:
            scores[cat] = sum(f in CATEGORY_FIELDS[cat] for f in fields)
        sorted_cats = sorted(scores.items(), key=lambda x: (-x[1], ["pokemon", "move", "ability"].index(x[0])))
        top_cat, top_score = sorted_cats[0]
        return top_cat if top_score > 0 else "pokemon"

    def clear(self, category: str = None):
        """清除指定类别的上下文，若不指定则全部清除"""
        if category:
            if category in self.context:
                self.context[category] = None
                print(f"[DEBUG] 已清除 {category} 上下文")
        else:
            for key in self.context:
                self.context[key] = None
            print("[DEBUG] 所有上下文已清除")

    def __repr__(self):
        return f"当前上下文状态：{self.context}"
    
    def is_new_entity(self, category: str, entity_name: str) -> bool:
        """判断该实体是否与当前上下文不同"""
        return self.context.get(category) != entity_name

