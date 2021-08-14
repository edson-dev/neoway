class Table():
    def __init__(self, string, default=["cpf",
                                        "private",
                                        "incomplete",
                                        "date_last_buy",
                                        "ticket_avg",
                                        "ticket_last_buy",
                                        "store_frequent",
                                        "store_last"]):
        self.fields = default
