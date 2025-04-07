from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class MenuItem:
    id: str
    parent_id: Optional[str]
    title: str
    text: str
    children: List['MenuItem'] = None

    def __post_init__(self):
        self.children = self.children or []
        self.is_root = not bool(self.parent_id)

class MenuManager:
    def __init__(self, items_data: List[List[str]]):
        self.items: Dict[str, MenuItem] = {}
        self.root_items: List[MenuItem] = []
        self._build_menu(items_data)

    def _build_menu(self, data: List[List[str]]) -> None:
        # Создаем все элементы
        for row in data:
            if len(row) < 4:  # ID, Parent_ID, Title, Text
                continue
                
            item = MenuItem(
                id=row[0],
                parent_id=row[1] if row[1] else None,
                title=row[2],
                text=row[3] if len(row) > 3 else ""
            )
            self.items[item.id] = item
            
            if item.is_root:
                self.root_items.append(item)
        
        # Строим иерархию
        for item in self.items.values():
            if item.parent_id and item.parent_id in self.items:
                self.items[item.parent_id].children.append(item)

    def get_item(self, item_id: str) -> Optional[MenuItem]:
        return self.items.get(item_id)

    def get_parent(self, item_id: str) -> Optional[MenuItem]:
        item = self.get_item(item_id)
        return self.get_item(item.parent_id) if item and item.parent_id else None