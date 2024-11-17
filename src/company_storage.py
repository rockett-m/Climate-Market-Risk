class Company:
    def __init__(self):
        self.fullname = None
        self.ticker = None
        self.rank = None
        self.revenue = None
        self.climate_score = None

    def update(self, climate_score: float):
        self.climate_score = climate_score


class Companies:
    def __init__(self):
        self.companies = []
