import pymysql

class DataManager:

    def __init__(self, db_name):
        self.db = self.connect_to_db(db_name)

    def connect_to_db(self, db_name):
        db = pymysql.connect(host='localhost', user='joseph', password='123456', port=3306, db=db_name)
        return db

    def close_db(self):
        self.db.close()

    def trans_to_shopdata(self, data):        # 向表单插入爬取的数据
        cursor = self.db.cursor()
        sql3 = 'INSERT INTO milktea_shop(shopid, title,areaname, backCateName, avgprice, avgscore, latitude, longitude, comments, historyCouponCount, city) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        try:
            cursor.execute(sql3, (data['shop_id'], data['title'], data['areaname'], data['backCateName'], data['avgprice'], data['avgscore'], data['latitude'], data['longitude'], data['comments'], data['historyCouponCount'], data['city']))
            self.db.commit()
            print('insert ok')
        except Exception as e:
            self.db.rollback()
            print(e)

    def trans_to_gooddata(self, data):
        cursor = self.db.cursor()
        sql3 = 'INSERT INTO milktea_good(goodID, shopid, title, price, value) values(%s, %s, %s, %s, %s)'
        try:
            cursor.execute(sql3, (data['good_id'], data['shop_id'], data['title'], data['price'], data['value']))
            self.db.commit()
        except:
            self.db.rollback()


