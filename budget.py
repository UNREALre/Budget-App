class Category:

    def __init__(self, name):
        self.ledger = []
        self.name = name
        self.max_print_len = 30
        self.max_label_len = 23

    def __str__(self):
        printable = list()
        printable.append(self.get_print_title())
        total = 0
        for item in self.ledger:
            total += item['amount']
            printable.append(self.generate_print_row(item['description'], item['amount']))

        printable.append(self.generate_print_row('Total: ', total, True))

        return '\n'.join(printable)

    def get_print_title(self):
        stars_number = self.max_print_len - len(self.name)
        start = end = ['*' for i in range(stars_number // 2)]
        title = ''.join(start) + self.name + ''.join(end)

        return title

    def generate_print_row(self, label, value, disable_formatting=False):
        value = '{:.2f}'.format(value)
        label = label[:self.max_label_len]
        if not disable_formatting:
            spaces_num = self.max_print_len - len(label) - len(str(value))
            spaces = [' ' for i in range(spaces_num)]
            value = ''.join(spaces) + str(value)

        return '{}{}'.format(label, value)

    def deposit(self, amount, description=''):
        self.add_to_ledger(amount, description)

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.add_to_ledger(-amount, description)
            return True

        return False

    def get_balance(self):
        balance = 0
        for item in self.ledger:
            balance += item['amount']

        return balance

    def transfer(self, amount, transfer_category):
        if self.check_funds(amount):
            description = 'Transfer to {}'.format(transfer_category.name)
            self.withdraw(amount, description)

            description = 'Transfer from {}'.format(self.name)
            transfer_category.deposit(amount, description)

            return True

        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def add_to_ledger(self, amount, description):
        self.ledger.append({
            'amount': amount,
            'description': description
        })


def create_spend_chart(categories):
    output = list()
    output.append('Percentage spent by category')
    total_spent = 0
    max_len_name = 0
    for category in categories:
        total_spent += count_spent(category.ledger)
        if len(category.name) > max_len_name:
            max_len_name = len(category.name)

    chart_data = [[0 for i in range(11)] for j in range(len(categories))]
    for i in range(len(categories)):
        spent = count_spent(categories[i].ledger)
        percent = round((spent / total_spent) * 100)

        for j in range(0, (percent//10) + 1):
            chart_data[i][j] = 1

    result = {
        100: [],
        90: [],
        80: [],
        70: [],
        60: [],
        50: [],
        40: [],
        30: [],
        20: [],
        10: [],
        0: []
    }
    for i in range(len(categories)):
        for j in range(len(chart_data[i])-1, -1, -1):
            result_index = 10 * j
            chart_val = 'o' if chart_data[i][j] == 1 else ' '
            result[result_index].append(chart_val)

    output = 'Percentage spent by category\n'
    for percent, data in result.items():
        output += '{}| {}  \n'.format(str(percent).rjust(3), '  '.join(data))

    separators = ['---' for i in range(len(categories))]
    output += '    {}-'.format(''.join(separators))

    for i in range(max_len_name):
        row = '\n     '
        for category in categories:
            char = category.name[i] if i < len(category.name) else ' '
            row += char + '  '

        output += row

    return output


def count_spent(ledger):
    spent = 0
    for item in ledger:
        if item['amount'] < 0:
            spent += -item['amount']

    return spent
