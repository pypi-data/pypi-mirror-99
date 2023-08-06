class URLs:
    def __init__(self, response_format="json"):
        self.base_url = "http://172.105.166.232/"

        # tables
        self.dispatch_price = "dispatch_price/"
        self.dispatch_regionsum = "dispatch_regionsum/"
        self.dispatch_interconnectorres = "dispatch_interconnectorres/"
        self.dispatch_price_historical = "dispatch_price_historical/"
        self.dispatch_regionsum_historical = "dispatch_regionsum_historical/"
        self.dispatch_interconnectorres_historical = "dispatch_interconnectorres_historical/"

        self.trading_price = "trading_price/"
        self.trading_regionsum = "trading_regionsum/"
        self.trading_interconnectorres = "trading_interconnectorres/"
        self.trading_price_historical = "trading_price_historical/"
        self.trading_regionsum_historical = "trading_regionsum_historical/"
        self.trading_interconnectorres_historical = "trading_interconnectorres_historical/"

    def base_url(self):
        return self.base_url

    def dispatch_price_url(self, intervals):
        return self.base_url + self.dispatch_price + intervals

    def dispatch_regionsum_url(self, intervals):
        return self.base_url + self.dispatch_regionsum + intervals

    def dispatch_interconnectorres_url(self, intervals):
        return self.base_url + self.dispatch_interconnectorres + intervals

    def dispatch_price_historical_url(self, start_date, end_date, intervals):
        return self.base_url + self.dispatch_price_historical + '{0}/{1}/{2}'.format(start_date,end_date,intervals)

    def dispatch_regionsum_historical_url(self, start_date, end_date, intervals):
        return self.base_url + self.dispatch_regionsum_historical + '{0}/{1}/{2}'.format(start_date,end_date,intervals)

    def dispatch_interconnectorres_historical_url(self, start_date, end_date, connectorid):
        return self.base_url + self.dispatch_interconnectorres_historical + '{0}/{1}/{2}'.format(start_date,end_date,connectorid)

    def trading_price_url(self, intervals):
        return self.base_url + self.trading_price + intervals

    def trading_regionsum_url(self, intervals):
        return self.base_url + self.trading_regionsum + intervals

    def trading_interconnectorres_url(self, intervals):
        return self.base_url + self.trading_interconnectorres + intervals

    def trading_price_historical_url(self, start_date, end_date, intervals):
        return self.base_url + self.trading_price_historical + '{0}/{1}/{2}'.format(start_date,end_date,intervals)

    def trading_regionsum_historical_url(self, start_date, end_date, intervals):
        return self.base_url + self.trading_regionsum_historical + '{0}/{1}/{2}'.format(start_date,end_date,intervals)

    def trading_interconnectorres_historical_url(self, start_date, end_date, connectorid):
        return self.base_url + self.trading_interconnectorres_historical + '{0}/{1}/{2}'.format(start_date,end_date,connectorid)