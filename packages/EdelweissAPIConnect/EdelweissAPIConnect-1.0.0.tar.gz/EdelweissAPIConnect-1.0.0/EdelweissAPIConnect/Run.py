import EdelweissAPIConnect


class Run:
    def __init__(self):
        # api = EdelAPI.EdelAPI("TESTVENDOR06", "Tv@6vnd$", "376136de4e97d1f8")
        # api = EdelweissAPIConnect.EdelweissAPIConnect("BJORN", "abc123", "326665db755329aa", False)
        # print(api.instruments[0])
        EdelweissAPIConnect.Feed(["-29", "-101"], "60000019", "60000019", self.somecb, False)
        print("hello world")

    def somecb(self, message):
        print(message)
