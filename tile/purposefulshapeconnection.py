class PurposefulShapeConnection:

    def __init__(self, name, t, amount):
        '''
        :param name:
        :param t:
        :param category:
        :param form: form of the shape, currently a dict
        {type: string, min: tuple(int), max: tuple(int), horizontalswap: bool}
        '''
        self.name = name
        self.type = t
        self.amount = amount
