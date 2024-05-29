def find_user(list_of_dicts, field_value):
    for item in list_of_dicts:
        if item.id == field_value:
            username = item.username or ""
            first_name = item.first_name or ""
            last_name = item.last_name or ""
            return {
                "username": username.strip(),
                "fullname": f"{first_name} {last_name}".strip()
            }
    return {}