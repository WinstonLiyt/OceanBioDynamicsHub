import calendar
import time
from sqlalchemy import create_engine
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('Agg')
matplotlib.rcParams['font.family'] = 'STSong'
import config
import pandas as pd
from trainning import Single_Variable_LSTM


def start(rdata):
    selectType = rdata['selectType']
    startYear = rdata['startYear']
    # endYear = rdata['endYear']
    predictYear = rdata['predictYear']
    selectedOption = rdata['selectedOption']

    engine = create_engine(config.db_mysql)

    df = ''
    if 'kingdom' == selectType:
        sql = """
select 
count(kingdom) as sums,date_year
from marine_life 
where kingdom={} and date_year>{} and `status`=1 
GROUP BY date_year 
ORDER BY date_year
        """
        df = pd.read_sql_query(sql=sql.format('"' + selectedOption + '"', startYear - 1), con=engine)
        print(df)
    elif 'habitat_region' == selectType:
        sql = """
        select 
count(habitat_region) as sums,date_year
from marine_life 
where habitat_region={} and date_year>{} and `status`=1 
GROUP BY date_year 
ORDER BY date_year        
        """
        df = pd.read_sql_query(sql=sql.format('"' + selectedOption + '"', startYear - 1), con=engine)
        print(df)
    elif 'species' == selectType:
        sql = """
        select 
date_year,count(species) as sums
from marine_life 
where species={} and date_year>{} and `status`=1 
GROUP BY date_year 
ORDER BY date_year       
        """
        df = pd.read_sql_query(sql=sql.format('"' + selectedOption + '"', startYear - 1), con=engine)
        print(df)
        # return jsonify({'code': 0, 'msg': '查询成功'})
    elif 'originalscientificname' == selectType:
        sql = """
            select 
count(originalscientificname) as sums,date_year
from marine_life 
where originalscientificname={} and date_year>{} and `status`=1 
GROUP BY date_year 
ORDER BY date_year           
        """
        df = pd.read_sql_query(sql=sql.format('"' + selectedOption + '"', startYear - 1), con=engine)
        print(df)
        # return jsonify({'code': 0, 'msg': '查询成功'})
    else:
        return 1, '类型选择错误'

    return load_data(df, predictYear, selectType, selectedOption)


def load_data(df, predictYear, selectType, selectedOption):
    try:
        predictYear = int(predictYear)
        # print('sums=', df['sums'].values)
        # print('date_year=', df['date_year'].values)
        # prev_days_for_train = int(len(df['sums'])/2)

        xx = df['date_year'].values
        if len(xx) < 3:
            return 1, '此类目下年份数据不足'
        dad = []
        for i in range(1, predictYear + 1):
            da = xx[-1] + i
            dad.append(da)
        xx = np.append(xx, dad)

        prev_days_for_train = 3
        x = df['date_year'].values
        x = x[prev_days_for_train:]
        y = df['sums'].values
        model = Single_Variable_LSTM(y, prev_days_for_train, None)
        y = y[prev_days_for_train:]
        xx = xx[prev_days_for_train:]

        a = model.train()
        b = model.predict(predictYear)[2]
        result = np.concatenate((a, b), axis=0)
        result = result.reshape(1, -1)
        result = np.squeeze(result)

        plt.figure(figsize=(10, 6))
        plt.title(selectType + ' (' + selectedOption + ') ' + str(predictYear) + '年 预测结果', fontsize=14)
        plt.plot(x, y, label='真实数据', color='blue', linewidth=2)
        plt.plot(xx, result, label='预测数据', color='red', linestyle='--', linewidth=2)
        plt.xlabel('年份 (year)', fontsize=12)
        plt.ylabel('数量 (num)', fontsize=12)
        plt.xlim(xx[0], xx[-1])
        plt.ylim(0, max(max(y), max(result)) * 1.1)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        # plt.axvline(x=len(y), color='r', linestyle='--')
        img_str = './static/upload/' + str(calendar.timegm(time.gmtime())) + '.jpg'
        plt.savefig(img_str)
        plt.show()
        plt.clf()

        return 0, img_str
    except Exception as e:
        print(e)
        return 1, '出现错误'


if __name__ == '__main__':
    rdata = {'selectType': 'species', 'startYear': 1990,
             'predictYear': 10, 'selectedOption': 'Favonigobius lateralis'}
    start(rdata)
