import matplotlib as mp
import matplotlib.pyplot as plt
from matplotlib import style


style.use('ggplot')


def get_pick_pack_value(ps: int):
    if ps < 72_000:
        result = 5000
    elif 72_000 <= ps < 720_000:
        result = 0.07 * ps
    else:
        result = 50_000
    return result + 500


def main():
    digi_percent = 0.1
    p_factory = 183000
    # lower_range = 600000
    # upper_range = 800000
    lower_range = int(p_factory * 1.1)
    upper_range = int(p_factory * 2.2)

    profits = []
    profit_percents = []
    sale_prices = []
    pick_packs = []
    for p_sell in range(lower_range, upper_range, 500):
        pp = get_pick_pack_value(p_sell)
        # print(round(pp, -2))
        pick_packs.append(pp)
        profit = p_sell - (digi_percent * p_sell) - pp - p_factory
        profit_percent = profit / p_sell * 100
        # print(f'{p_sell:,}: profit: {profit:<6,.0f} | percent: {profit_percent:0.1f}')
        profits.append(profit)
        profit_percents.append(profit_percent)
        sale_prices.append(p_sell)

    fig, ax = plt.subplots()
    ax.plot(sale_prices, profit_percents, label='profit percent')
    # axs.plot(sale_prices, pick_packs)

    ax.set_ylabel('Profit Percents')
    ax.set_xlabel('Sell Price')
    ax.set_title(f'factory price: {p_factory:,}')
    ax.legend(loc='upper left')

    path = f'./plots'
    fig.set_size_inches(19, 11)
    fig.savefig(f'{path}/profits.png', dpi=100)
    plt.show()
    plt.close(fig)


if __name__ == '__main__':
    main()
