def print_transactions(transactions: list, label: str) -> None:
    print(label, "*" * (50 - len(label)))

    for item in transactions:
        print(item)

    print("=" * 50)


# Menge, Preis; sorted by date ascending
sells = [
    (0.13541820, 35),     # 29.58
    (0.11454640, 25),     # 22.68
    (0.13420283, 30),     # 25.89
    (0.36125077, 88.09),  # 80.48
]     # Total Profits: EUR 158.63

buys = [
    (0.18586880, 7.44),
    (0.08721041, 3.49),
    (0.27289865, 11.71),
    (0.27456618, 11.22),
]

# sells = [
#     (3.0, 100),
#     (1.0, 50),
#     (2.0, 120),
#     (2.0, 150),
# ]
#
# buys = [
#     (1.0, 10),
#     (2.0, 25),
#     (2.0, 45),
#     (3.0, 60),
# ]

# Profit: 80
# Profit: 27.5
# Profit: 98.75
# Profit: 110