import matplotlib.pyplot as plt

def priceOverTime(data):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(14, 7))
    plt.plot(data['year'], data['Price'], label='Brent Oil Price')

    plt.xticks(range(min(data['year']), max(data['year']) + 2, 2)) 

    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.title('Brent Oil Price Over Time')
    plt.legend()
    plt.show()