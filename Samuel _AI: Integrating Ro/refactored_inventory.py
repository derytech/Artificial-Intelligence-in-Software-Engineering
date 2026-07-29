class InvalidProductDataError(Exception):
    """Custom exception raised when product data validation fails."""
    pass


class Product:
    """Represents a product with a name, price, and quantity."""

    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        # Assigning through property setters ensures validation runs during __init__
        self.price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Getter for product price."""
        return self._price

    @price.setter
    def price(self, value):
        """Setter for product price with type and non-negative validation."""
        # Check if price is a valid numeric type (bool is a subclass of int, so we exclude it)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise InvalidProductDataError(
                f"Invalid price '{value}': Price must be a number (int or float)."
            )
        # Ensure price is not negative
        if value < 0:
            raise InvalidProductDataError(
                f"Invalid price '{value}': Price cannot be negative."
            )
        
        self._price = float(value)

    @property
    def quantity(self) -> int:
        """Getter for product quantity."""
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        """Setter for product quantity with integer type and non-negative validation."""
        # Ensure quantity is strictly an integer (exclude booleans)
        if isinstance(value, bool) or not isinstance(value, int):
            raise InvalidProductDataError(
                f"Invalid quantity '{value}': Quantity must be an integer."
            )
        # Ensure quantity is not negative
        if value < 0:
            raise InvalidProductDataError(
                f"Invalid quantity '{value}': Quantity cannot be negative."
            )
        
        self._quantity = value


class InventoryManager:
    """Manages the collection of products and provides inventory operations."""

    def __init__(self, inventory=None):
        self.inventory = inventory if inventory is not None else []

    def add_product(self, product):
        """Adds a product object to the inventory list."""
        self.inventory.append(product)

    def update_quantity(self, name, new_quantity):
        """Updates the quantity of a product by name."""
        for product in self.inventory:
            if product.name == name:
                product.quantity = new_quantity
                break

    def calculate_total_value(self):
        """Calculates the total monetary value of all inventory."""
        total = 0
        for product in self.inventory:
            total += product.price * product.quantity
        return total

    def display_inventory(self):
        """Prints the current inventory list."""
        for product in self.inventory:
            print(f"{product.name} - ${product.price:.2f} x {product.quantity}")


# --- Demo Usage ---

if __name__ == "__main__":
    manager = InventoryManager()

    # 1. Valid Initialization & Operations
    try:
        laptop = Product("Laptop", 1200.00, 5)
        mouse = Product("Mouse", 25.00, 20)
        
        manager.add_product(laptop)
        manager.add_product(mouse)
        
        # Valid quantity update via setter validation
        manager.update_quantity("Mouse", 18)

        print("Current Inventory:")
        manager.display_inventory()
        print(f"\nTotal Inventory Value: ${manager.calculate_total_value():.2f}\n")

    except InvalidProductDataError as e:
        print(f"Validation Error: {e}")

    # 2. Demonstrating Custom Validation Exception Handling
    print("--- Demonstrating Validation Rules ---")
    
    # Test A: Negative Price
    try:
        bad_price = Product("Monitor", -150.00, 2)
    except InvalidProductDataError as e:
        print(f"Caught expected error: {e}")

    # Test B: Invalid Quantity Type
    try:
        bad_quantity = Product("Keyboard", 50.00, "ten")
    except InvalidProductDataError as e:
        print(f"Caught expected error: {e}")

    # Test C: Invalid Update via InventoryManager
    try:
        manager.update_quantity("Laptop", -3)
    except InvalidProductDataError as e:
        print(f"Caught expected error during update: {e}")
