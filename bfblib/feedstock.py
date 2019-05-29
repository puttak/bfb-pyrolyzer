import chemics as cm


class Feedstock():

    def __init__(self, params):
        self.dp = params.feedstock['dp']

    def devol_time(self, temp):
        dp = self.dp * 1000
        tv = cm.devol_time(dp, temp)
        return tv
