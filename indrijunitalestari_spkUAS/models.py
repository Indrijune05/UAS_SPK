import numpy as np
import pandas as pd
from spk_model import WeightedProduct

class Coffeshop():

    def __init__(self) -> None:
        self.coffe_shop = pd.read_csv('data/indrijunitalestari.csv')
        self.coffe_shop_array = np.array(self.coffe_shop)

    @property
    def coffe_shop_data(self):
        data = []
        for coffeShop in self.coffe_shop_array:
            data.append({'id': coffeShop[0], 'nama': coffeShop[1]})
        return data

    @property
    def coffe_shop_data_dict(self):
        data = {}
        for coffeShop in self.coffe_shop_array:
            data[coffeShop[0]] = coffeShop[1] 
        return data

    def get_recs(self, kriteria:dict):
        wp = WeightedProduct(self.coffe_shop.to_dict(orient="records"), kriteria)
        return wp.calculate
