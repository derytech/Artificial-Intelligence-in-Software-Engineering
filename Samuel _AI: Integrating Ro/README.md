# Integrating Robust Error Handling in OOP

## Objective
Enhance the Product Inventory Manager by implementing robust data validation using Python `@property` decorators and a custom exception.

## Files
- original_inventory.py – The original inventory manager provided for the task.
- refactored_inventory.py – The enhanced version with validation and exception handling.

## Improvements Made
- Added a custom exception class: `InvalidProductDataError`
- Implemented `@property` getters and setters for `price` and `quantity`
- Prevented negative prices and quantities
- Validated data types for `price` and `quantity`
- Improved encapsulation and data integrity

## Test Performed
The following test was used to verify the validation:

```python
print("\n--- Testing Invalid Input ---")
try:
    manager.inventory[0].quantity = -5
except Exception as e:
    print(f"Test result: {e}")
```

### Output

```
--- Testing Invalid Input ---
Test result: Invalid quantity '-5': Quantity cannot be negative.
```

## Conclusion

Using `@property` setters and a custom exception ensures that invalid data cannot be stored in Product objects. This improves encapsulation, maintains data integrity, and makes the application more reliable.
