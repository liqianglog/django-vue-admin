import _venv
from init_data import *
from dvadmin.system.models import *


def list2tree(data_list, parent_id=None):
    result = []
    for item in data_list:
        data_format = {}
        if item["parent_id"] == parent_id:
            bak = item.copy()
            del bak["parent_id"]
            item_id = bak.pop("id")
            data_format["id"] = item_id
            data_format["data"] = bak
            result.append(data_format)
            childs = [obj for obj in data_list if obj["parent_id"] == item_id]
            children = list2tree(childs, item_id)
            if childs:
                data_format["children"] = children
    return result


print(list2tree(system_config_data))
