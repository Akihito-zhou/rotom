# router_intent.py
def route_query(intent_data: dict, query_funcs: dict) -> str:
    target = intent_data.get("target")
    target_type = intent_data.get("target_type")

    if target_type == "宝可梦":
        return query_funcs['pokemon'](target)
    elif target_type == "技能":
        return query_funcs['move'](target)
    elif target_type == "特性":
        return query_funcs['ability'](target)
    else:
        return f"⚠️ 无法识别类型 {target_type}，无法完成查询。"
    