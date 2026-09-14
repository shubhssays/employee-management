def get_dynamic_value(columns_text: str) -> str:
    values = columns_text.replace("(", "").replace(")", "")
    values = values.split(",")
    values = ", ".join([f":{value.strip()}" for value in values])
    return f"VALUES ({values})"
