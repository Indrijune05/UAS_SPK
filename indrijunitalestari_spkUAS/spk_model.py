from settings import COFFESHOP_SCALE

class BaseMethod():

    def __init__(self, data_dict, **setWeight):

        self.dataDict = data_dict

        # 1-6 (Kriteria)
        self.raw_weight = {
            'coffe_shop': 1,
            'harga_kopi': 2,
            'kualitas_kopi': 3,
            'pelayanan': 4,
            'suasana': 5,
            'jarak': 6
        }

        if setWeight:
            for item in setWeight.items():
                temp1 = setWeight[item[0]] # value int
                temp2 = {v: k for k, v in setWeight.items()}[item[1]] # key str

                setWeight[item[0]] = item[1]
                setWeight[temp2] = temp1

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {c: round(w/total_weight, 2) for c,w in self.raw_weight.items()}

    @property
    def data(self):
        return [{
            'id': coffe_shop['id'],
            'coffe_shop': COFFESHOP_SCALE[coffe_shop['coffee_shop']],
            'harga_kopi': coffe_shop['harga_kopi'],
            'kualitas_kopi': coffe_shop['kualitas_kopi'],
            'pelayanan': coffe_shop['pelayanan'],
            'suasana': coffe_shop['suasana'],
            'jarak': coffe_shop['jarak']
        } for coffe_shop in self.dataDict]

    @property
    def normalized_data(self):
        # x/max [benefit]
        # min/x [cost]

        coffe_shop = [] # max
        harga_kopi = [] # min
        kualitas_kopi = [] # max
        pelayanan = [] # max
        suasana = [] # max
        jarak = [] # min

        for data in self.data:
            coffe_shop.append(data['coffe_shop'])
            harga_kopi.append(data['harga_kopi'])
            kualitas_kopi.append(data['kualitas_kopi'])
            pelayanan.append(data['pelayanan'])
            suasana.append(data['suasana'])
            jarak.append(data['jarak'])

        max_coffe_shop = max(coffe_shop)
        min_harga_kopi = max(harga_kopi)
        max_kualitas_kopi = max(kualitas_kopi)
        max_pelayanan = max(pelayanan)
        max_suasana = max(suasana)
        min_jarak = max(jarak)

        return [{
            'id': data['coffe_shop'],
            'coffe_shop': data['coffe_shop']/max_coffe_shop, # benefit
            'harga_kopi': data['harga_kopi']/min_harga_kopi, # cost
            'kualitas_kopi': data['kualitas_kopi']/max_kualitas_kopi, # benefit
            'pelayanan': data['pelayanan']/max_pelayanan, # benefit
            'suasana': data['suasana']/max_suasana, # benefit
            'jarak': data['jarak']/min_jarak # cost
        } for data in self.data]
 

class WeightedProduct(BaseMethod):
    def __init__(self, dataDict, setWeight:dict):
        super().__init__(data_dict=dataDict, **setWeight)

    @property
    def calculate(self):
        weight = self.weight
        # calculate data and weight[WP]
        result = {row['id']:
            round(
                row['coffe_shop'] ** weight['coffe_shop'] *
                row['harga_kopi'] ** (-weight['harga_kopi'])*
                row['kualitas_kopi'] ** weight['kualitas_kopi'] *
                row['pelayanan'] ** weight['pelayanan'] *
                row['suasana'] ** weight['suasana'] *
                row['jarak'] ** (-weight['jarak'])
                , 2
            )

            for row in self.normalized_data}
        #sorting
        # return result
        return dict(sorted(result.items(), key=lambda x:x[1], reverse=True))
