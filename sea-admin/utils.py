# 导入数据
import datetime
from sqlalchemy import create_engine
import config
import csv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Index, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(config.db_mysql)
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()


# 海洋生物表
class MarineLife(Base):
    __tablename__ = 'marine_life'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)  # 生物名称 scientificname

    originalscientificname = Column(String(255), nullable=False)  # 原学名 2

    species = Column(String(255), nullable=False)  # 种类
    habitat_region = Column(String(255), nullable=False)  # 栖息区域 family
    quantity = Column(Integer, nullable=False)  # 数量

    kingdom = Column(String(255), nullable=True)  # 2  族群
    date_year = Column(Integer, nullable=True)  # 2  年份
    decimallongitude = Column(Float, nullable=False)  # 2  经度
    decimallatitude = Column(Float, nullable=False)  # 2  纬度

    status = Column(Integer, nullable=False)  # 状态
    time = Column(DateTime, nullable=False)

    def __repr__(self):
        return '<MarineLife %r>' % self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'species': self.species,
            'habitat_region': self.habitat_region,
            'quantity': self.quantity,
            'status': self.status,
            'time': self.time,
        }


def import_data():
    try:
        url = 'D:\\vue-project\\obis.csv'
        f = open(url, 'r', encoding='utf-8')
        cf = csv.reader(f)
        i = 0
        for row in cf:
            if i == 0:
                i += 1
                continue
            if i > 50000:
                break

            marinLife = MarineLife(user_id=1, name=row[3], originalscientificname=row[4], species=row[24],
                                   habitat_region=row[22], quantity=0, kingdom=row[18], date_year=row[2] if row[2] else 0,
                                   decimallongitude=row[0], decimallatitude=row[1], status=1, time=datetime.datetime.now())
            session.add(marinLife)
            session.commit()
            session.close()

            i += 1

    except Exception as e:
        print(e)


if __name__ == '__main__':
    import_data()
