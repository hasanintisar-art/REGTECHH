from datetime import datetime

class BudgetItem:
    """Represents a single income or expense item."""
    def __init__(self, amount, category, item_type, date=None, description=""):
        if item_type not in ['income', 'expense']:
            raise ValueError("Item type must be 'income' or 'expense'.")
        if amount <= 0:
            raise ValueError("Amount must be positive.")

        self.amount = amount
        self.category = category
        self.item_type = item_type # 'income' or 'expense'
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")
        self.description = description

    def __repr__(self):
        sign = '+' if self.item_type == 'income' else '-'
        return f"[{self.date}] {self.category.ljust(10)}: {self.description.ljust(20)} {sign}${self.amount:,.2f}"

