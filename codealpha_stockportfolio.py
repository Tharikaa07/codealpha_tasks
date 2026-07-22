import random
import csv

def get_stock_prices():
    """Hardcoded dictionary of stock prices (buy price)."""
    return {
        "AAPL": 180,
        "TSLA": 250,
        "GOOGL": 140,
        "AMZN": 175,
        "MSFT": 420
    }

def get_user_portfolio(stock_prices):
    """Ask the user for stock names and quantities."""
    portfolio = {}

    print("Available stocks and prices:")
    for stock, price in stock_prices.items():
        print(f"  {stock}: ${price}")

    print("\nEnter your stock holdings. Type 'done' when finished.\n")

    while True:
        stock_name = input("Stock symbol (e.g. AAPL): ").upper().strip()

        if stock_name == "DONE":
            break

        if stock_name not in stock_prices:
            print("Stock not found in our price list. Please try again.\n")
            continue

        try:
            quantity = int(input(f"Quantity of {stock_name}: "))
            if quantity <= 0:
                print("Quantity must be a positive number.\n")
                continue
        except ValueError:
            print("Please enter a valid whole number.\n")
            continue

        portfolio[stock_name] = portfolio.get(stock_name, 0) + quantity
        print(f"Added {quantity} shares of {stock_name}.\n")

    return portfolio

def simulate_current_prices(stock_prices):
    """Simulate a 'current' market price with a small random change (+/- 5%)."""
    current_prices = {}
    for stock, price in stock_prices.items():
        change_percent = random.uniform(-5, 5)
        current_prices[stock] = round(price * (1 + change_percent / 100), 2)
    return current_prices

def calculate_summary(portfolio, buy_prices, current_prices):
    """Calculate investment value, current value, and gain/loss."""
    breakdown = []
    total_invested = 0
    total_current = 0

    for stock, quantity in portfolio.items():
        buy_price = buy_prices[stock]
        current_price = current_prices[stock]
        invested_value = buy_price * quantity
        current_value = current_price * quantity
        gain_loss = current_value - invested_value
        gain_loss_percent = (gain_loss / invested_value) * 100

        breakdown.append({
            "stock": stock,
            "quantity": quantity,
            "buy_price": buy_price,
            "current_price": current_price,
            "invested_value": invested_value,
            "current_value": current_value,
            "gain_loss": gain_loss,
            "gain_loss_percent": gain_loss_percent
        })

        total_invested += invested_value
        total_current += current_value

    return breakdown, total_invested, total_current

def print_allocation_chart(breakdown, total_invested):
    """Print a simple text-based bar chart showing portfolio allocation."""
    print("\nPortfolio Allocation:")
    for item in breakdown:
        percent = (item["invested_value"] / total_invested) * 100
        bar = "#" * int(percent / 2)
        print(f"  {item['stock']:<6} {bar} {percent:.1f}%")

def save_to_csv(breakdown, total_invested, total_current, filename="portfolio_summary.csv"):
    """Save the portfolio summary to a CSV file."""
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Stock", "Quantity", "Buy Price", "Current Price",
                          "Invested Value", "Current Value", "Gain/Loss", "Gain/Loss %"])
        for item in breakdown:
            writer.writerow([
                item["stock"], item["quantity"], item["buy_price"], item["current_price"],
                round(item["invested_value"], 2), round(item["current_value"], 2),
                round(item["gain_loss"], 2), round(item["gain_loss_percent"], 2)
            ])
        writer.writerow([])
        writer.writerow(["Total Invested", round(total_invested, 2)])
        writer.writerow(["Total Current Value", round(total_current, 2)])
        writer.writerow(["Overall Gain/Loss", round(total_current - total_invested, 2)])
    print(f"Summary saved to {filename}")

def main():
    buy_prices = get_stock_prices()
    portfolio = get_user_portfolio(buy_prices)

    if not portfolio:
        print("No stocks were added. Exiting.")
        return

    current_prices = simulate_current_prices(buy_prices)
    breakdown, total_invested, total_current = calculate_summary(portfolio, buy_prices, current_prices)

    print("\nPortfolio Summary")
    print("=" * 70)
    print(f"{'Stock':<6}{'Qty':<6}{'Buy $':<10}{'Now $':<10}{'Value $':<12}{'Gain/Loss':<15}")
    print("-" * 70)
    for item in breakdown:
        gl_str = f"{item['gain_loss']:+.2f} ({item['gain_loss_percent']:+.1f}%)"
        print(f"{item['stock']:<6}{item['quantity']:<6}{item['buy_price']:<10}"
              f"{item['current_price']:<10}{item['current_value']:<12.2f}{gl_str:<15}")
    print("-" * 70)
    overall_gain_loss = total_current - total_invested
    print(f"Total Invested: ${total_invested:.2f}")
    print(f"Current Value:  ${total_current:.2f}")
    print(f"Overall Gain/Loss: ${overall_gain_loss:+.2f}")

    print_allocation_chart(breakdown, total_invested)

    save_choice = input("\nSave summary to a CSV file? (yes/no): ").lower().strip()
    if save_choice == "yes":
        save_to_csv(breakdown, total_invested, total_current)

if _name_ == "_main_":
    main()
