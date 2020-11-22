import json
from itertools import count

import texttable


def read_config():
    with open('config.json') as f:
        config = json.load(f)

    return config


def infer_mortgage_numbers(body, interest, payment):
    payments = []
    interests_payed = []
    body_per_month = []

    while body > 0:
        interest_to_pay = body * (interest / 100 / 12)
        payment_after_interest = payment - interest_to_pay
        body -= payment_after_interest

        payments.append(payment - interest)
        interests_payed.append(interest_to_pay)
        body_per_month.append(max(body, 0))

    return payments, interests_payed, body_per_month


if __name__ == '__main__':
    config = read_config()
    interest_percentage = config['interest_percentage']
    mortgage_body_initial = config['mortgage_body_initial']
    monthly_payment = config['monthly_payment']

    data = []

    for interest_p in count(interest_percentage, -0.2):
        if interest_p < 5:
            break

        payments, interests_payed, body_per_month = infer_mortgage_numbers(
            body=mortgage_body_initial,
            interest=interest_p,
            payment=monthly_payment,
        )

        duration = len(body_per_month)
        overhead = monthly_payment * (duration - 1) + (body_per_month[-2]) - mortgage_body_initial
        data.append([f'{interest_p:.2f}', duration, f'{int(overhead / 1e3)}'])

    data.insert(0, ["Процент", "Срок кредита", "Переплата, тысячи"])
    data = list(zip(*data))
    table = texttable.Texttable(max_width=240)
    table.set_cols_dtype(['t'] * len(data[0]))
    table.add_rows(data)

    print(f"Сумма кредита: {mortgage_body_initial}")
    print(f"Размер выплат: {monthly_payment}")
    print(table.draw())
