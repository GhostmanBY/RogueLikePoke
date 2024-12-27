"""
Gestión de objetos y mejoras
"""

class Inventory:
    def __init__(self):
        self.items = {}
        
    def add_item(self, item, quantity=1):
        """Añade un item al inventario"""
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity
            
    def use_item(self, item):
        """Usa un item del inventario"""
        if item in self.items and self.items[item] > 0:
            self.items[item] -= 1
            return True
        return False
