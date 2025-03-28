from typing import List, Union
class OrderPizza:
    def __init__(self):
        self.menu = [
            {"name": "Margherita", "price": 8.5},
            {"name": "Pepperoni", "price": 9.5},
            {"name": "Mushroom", "price": 9.0}
        ]
        self.cart = []
        self.next_pizza_id = 1

    def get_pizza_menu(self):
        print("Done getting pizza menu")

    def add_pizza_to_cart(self, size, toppings, quantity=1, specialInstructions=""):
        pizza = {
            "id": self.next_pizza_id,
            "size": size,
            "toppings": toppings,
            "quantity": quantity,
            "specialInstructions": specialInstructions
        }
        self.cart.append(pizza)
        self.next_pizza_id += 1
        print("Added pizza to cart")
        

    def remove_pizza_from_cart(self, pizzaId):
        self.cart = [pizza for pizza in self.cart if pizza["id"] != pizzaId]
        print("Done removed pizza from cart")
        return self.cart

    def get_pizza_from_cart(self, pizzaId):
        for pizza in self.cart:
            if pizza["id"] == pizzaId:
                return pizza
        print("Done get pizza from cart")
        return None

    def get_cart(self):
        total_price = sum(pizza["quantity"] * self._get_pizza_price(pizza) for pizza in self.cart)
        print("Done get cart")
        return {"items": self.cart, "total_price": total_price}

    def checkout(self):
        total_price = sum(pizza["quantity"] * self._get_pizza_price(pizza) for pizza in self.cart)
        self.cart = []
        self.next_pizza_id = 1
        print("Done checkout")
        return {"status": "Order placed", "total_price": total_price}

    def _get_pizza_price(self, pizza):
        base_price = next(item["price"] for item in self.menu if item["name"] in pizza["toppings"])
        size_multiplier = {"Small": 1, "Medium": 1.5, "Large": 2}
        return base_price * size_multiplier[pizza["size"]]

class GetBettingReport:
    def __init__(self):
        self.menu = [
            {"name": "Margherita", "price": 8.5},
            {"name": "Pepperoni", "price": 9.5},
            {"name": "Mushroom", "price": 9.0}
        ]

    def get_winlost_detail_report(self, from_date: str, to_date: str, product: str = "All", product_detail: str = "All", level: str = "All", user: Union[str, List[str], None] = None):
        print("Done winlost_detail_report")