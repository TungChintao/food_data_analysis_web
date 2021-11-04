from pyasn1.compat.octets import null

from database_execute import DataManager

def main():
    dbManager = DataManager('milktea_data')
    goods=[
              {
                "id": 648080682,
                "title": "泷珠奶茶1杯",
                "subtitleA": null,
                "subtitleB": null,
                "subtitleC": null,
                "price": 7.6,
                "value": 10,
                "sales": 0,
                "iUrl": "",
                "stid": null,
                "trace": null,
                "tag": {
                  "promotion": [
                    "立减0.4"
                  ]
                }
              },
              {
                "id": 648076411,
                "title": "杨枝甘露1杯",
                "subtitleA": null,
                "subtitleB": null,
                "subtitleC": null,
                "price": 12,
                "value": 15,
                "sales": 0,
                "iUrl": "",
                "stid": null,
                "trace": null,
                "tag": {
                  "promotion": []
                }
              },
              {
                "id": 671113040,
                "title": "益杯烧仙草1杯",
                "subtitleA": null,
                "subtitleB": null,
                "subtitleC": null,
                "price": 8.8,
                "value": 11,
                "sales": 0,
                "iUrl": "",
                "stid": null,
                "trace": null,
                "tag": {
                  "promotion": []
                }
              },
              {
                "id": 645877926,
                "title": "金桔柠檬1杯",
                "subtitleA": null,
                "subtitleB": null,
                "subtitleC": null,
                "price": 6.8,
                "value": 9,
                "sales": 0,
                "iUrl": "",
                "stid": null,
                "trace": null,
                "tag": {
                  "promotion": []
                }
              },
              {
                "id": 725831099,
                "title": "栗上茉香1杯",
                "subtitleA": null,
                "subtitleB": null,
                "subtitleC": null,
                "price": 9,
                "value": 11,
                "sales": 0,
                "iUrl": "",
                "stid": null,
                "trace": null,
                "tag": {
                  "promotion": []
                }
              },
              {
                "id": 725846480,
                "title": "栗上奶香1杯",
                "subtitleA": null,
                "subtitleB": null,
                "subtitleC": null,
                "price": 11,
                "value": 13,
                "sales": 0,
                "iUrl": "",
                "stid": null,
                "trace": null,
                "tag": {
                  "promotion": []
                }
              },
              {
                "id": 668145211,
                "title": "冰暴葡萄1杯",
                "subtitleA": null,
                "subtitleB": null,
                "subtitleC": null,
                "price": 13,
                "value": 15,
                "sales": 0,
                "iUrl": "",
                "stid": null,
                "trace": null,
                "tag": {
                  "promotion": []
                }
              },
              {
                "id": 720487530,
                "title": "冰暴芝芝葡萄1杯",
                "subtitleA": null,
                "subtitleB": null,
                "subtitleC": null,
                "price": 15,
                "value": 17,
                "sales": 0,
                "iUrl": "",
                "stid": null,
                "trace": null,
                "tag": {
                  "promotion": []
                }
              },
              {
                "id": 730043519,
                "title": "桃桃乌龙1杯",
                "subtitleA": null,
                "subtitleB": null,
                "subtitleC": null,
                "price": 10,
                "value": 12,
                "sales": 0,
                "iUrl": "",
                "stid": null,
                "trace": null,
                "tag": {
                  "promotion": []
                }
              },
              {
                "id": 730040247,
                "title": "古法红糖珍珠牛奶1杯",
                "subtitleA": null,
                "subtitleB": null,
                "subtitleC": null,
                "price": 11.8,
                "value": 14,
                "sales": 0,
                "iUrl": "",
                "stid": null,
                "trace": null,
                "tag": {
                  "promotion": []
                }
              }
            ]
    names = ['title', 'price', 'value']

    for i in range(len(goods)):
        print(i)
        good = {}
        good['shop_id'] = 1
        for key in names:
            good[key] = goods[i][key]
        dbManager.trans_to_gooddata(good)
    dbManager.close_db()

if __name__ == '__main__':
    main()
