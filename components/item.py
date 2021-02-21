class Item:
    def __init__(self, use_funtion=None, targeting=False, targeting_message=None,**kwargs):
        self.use_funtion = use_funtion
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs