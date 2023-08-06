import time

import pymysql  # PyMySQL==0.10.0
import numpy as np  # numpy==1.18.5
import pandas as pd  # pandas==1.1.0
import sys
import matplotlib.pyplot as plt  # matplotlib==3.3.0
import scipy.io as sio  # scipy==1.4.1
import sklearn  # sklearn==0.0

pd.set_option('display.max_columns', 10000, 'display.width', 10000, 'max_rows', 50,
              'display.unicode.east_asian_width', True)


class mysqlOperator:
	"""
    【执行流程与参数说明】 \n
    ①实例化对象
        e.g:
                obj = objectMySQL(databaseName='bearing_pad_temper') \n
                print(obj)
        param:
                databaseName，数据库名称，str，必要参数，形如“bearing_pad_temper” \n
                tableName，数据表名称，str，必要参数，形如“轴承瓦温20200320_20200327_原始数据” \n
                host，数据库名称，int，默认值“localhost” \n
                port，数据库名称，int，默认值3306 \n
                userID，数据库名称，str，默认值“root” \n
                password，数据库名称，str，默认值“000000” \n
    """

	def __init__(self, **kwargs):
		self.dataBaseName = kwargs['databaseName']
		self.tableName = kwargs['tableName']
		host = kwargs['host'] if 'host' in kwargs.keys() else 'localhost'
		port = kwargs['port'] if 'port' in kwargs.keys() else 3306
		userID = kwargs['userID'] if 'userID' in kwargs.keys() else 'root'
		password = kwargs['password'] if 'password' in kwargs.keys() else '000000'
		self.__con__ = pymysql.connect(host=host, port=port, db=self.dataBaseName, user=userID, passwd=password,
		                               charset='utf8mb4')
		self.__cur__ = self.__con__.cursor()

	def createTable(self, **kwargs):
		'''
        :param kwargs: tableName：表单名；columns：列名+数据类型+缺省控制，字符串形如'test01 float null'
        :return: None
        '''
		self.__cur__.execute('create table if not exists ' + kwargs['tableName'] + '(' + kwargs['columns'] + ')')
		self.__cur__.close()
		self.__con__.close()

	def addColumn(self, **kwargs):
		'''
        :param kwargs: tableName：表单名；column：初始列名、数据类型、缺省值，字符串形如'test02 float null'
        :return: None
        '''
		self.__cur__.execute(
			'alter table ' + self.dataBaseName + '.' + kwargs['tableName'] + ' add column ' + kwargs['column'])
		self.__cur__.close()
		self.__con__.close()

	def insertRow(self, **kwargs):
		'''
        :param kwargs: tableName：表单名；values：新增值，字符串形如'510, 512'
        :return: None
        '''
		self.__cur__.execute('insert into ' + kwargs['tableName'] + ' value ' + '(' + kwargs['values'] + ')')
		self.__cur__.close()
		self.__con__.close()

	def updateValue(self, **kwargs):
		'''
        :param kwargs: tableName：表单名；targetColumn：更新列名，字符串形如'test02'；value：更新值，字符串形如'110'
        :return: None
        '''
		com = 'update ' + self.dataBaseName + '.' + kwargs['tableName'] + ' set ' + kwargs['targetColumn'] + '=' + \
		      kwargs['value']
		self.__cur__.execute(com)
		self.__cur__.close()
		self.__con__.close()

	def selectData(self, **kwargs):
		"""
            content: 需要调用的列名，str，默认为查询数据的样本数"count(*)"，形如”'汽机润滑油冷油器出口总管油温1,发电机励端轴瓦温度'“  \n
            condition: 调用数据的条件，str，默认为全部数据，形如“'(时间戳>=\'2020-03-20 16:18:03\') and (时间戳<=\'2020-03-20 16:18:11\')'”  \n
            return: 调取的数据，df
            【执行流程与参数说明】 \n
            e.g:
                obj = objectMySQL(databaseName='bearing_pad_temper', tableName='轴承瓦温20200320_20200327_原始数据') \n
                data = obj.selectData(content=content, condition=condition) \n
                print(data) \n
        """
		condition = kwargs['condition'] if 'condition' in kwargs.keys() else False
		content = kwargs['content'] if 'content' in kwargs.keys() else 'count(*)'
		if condition:
			com = 'select ' + content + ' from ' + self.dataBaseName + '.' + self.tableName + ' where ' + kwargs[
				'condition']
		else:
			com = 'select ' + content + ' from ' + self.dataBaseName + '.' + self.tableName
		self.__cur__.execute(com)
		res = self.__cur__.fetchall()
		self.__cur__.close()
		self.__con__.close()
		if content != 'count(*)':
			res = pd.DataFrame(res, columns=content.split(","))
		else:
			res = pd.DataFrame({'inspectedDataSize': [res[0][0]]})
		return res


def code2Name(_kksCodes: list, _dictNames: list, _kksCode: list, _verbose=True):
	"""
	:param _kksCodes: 编码的字典 list
	:param _dictNames: 名称的字典 list
	:param _kksCode: 需要转译的编码 list
	:param _verbose: 是否显示对输入字典和待转译编码的检查结果 Boolean
	:return: 转译完成的名称 list
	【执行流程与参数说明】 \n
	e.g:
		a = code2Name(kksCode, dictName, ['ED009HP2MUB01UU008AA01J3DG006EA01'])
		print(a)
	"""
	# 检查输入的清单是否符合基本要求
	len_kksCodes = len(_kksCodes)
	len_kksCodes_unique = len(pd.unique(_kksCodes))
	len_dictNames = len(_dictNames)
	len_dictNames_unique = len(pd.unique(_dictNames))
	if _verbose:
		checkStr01 = "待检编码中有重复项 X " if isinstance(_kksCode, list) and len(np.unique(_kksCode)) != len(
			_kksCode) else "待检编码中没有重复项 √ "
		checkStr02 = "编码中没有重复项 √ " if len_kksCodes == len_kksCodes_unique else "编码中有重复项 X "
		checkStr03 = "名称中没有重复项 √ " if len_dictNames == len_dictNames_unique else "名称中有重复项 (允许) "
		print("#" * 2 * (2 + max([len(checkStr01), len(checkStr02), len(checkStr03)])))
		print('\t', checkStr01, '\n\t', checkStr02, '\n\t', checkStr03)
		print("#" * 2 * (2 + max([len(checkStr01), len(checkStr02), len(checkStr03)])))
	# 字典以中文名称为依据，升序排列
	_dict = pd.DataFrame({'kksCodes': _kksCodes, 'dictNames': _dictNames}).sort_values(by=['dictNames'])
	# 查询
	_kksName = []
	if isinstance(_kksCode, list):
		for eachCode_toReplace in _kksCode:
			queryRes = _dict.query("kksCodes.str.contains(\'" + eachCode_toReplace + "\')", engine='python')
			res = queryRes['dictNames'].values
			if np.shape(res)[0] == 0:
				print(">>> 注意：对象kksCode未找到kksName，此kksCode是 %s" % (eachCode_toReplace))
			elif np.shape(res)[0] >= 2:
				print(">>> 错误: 单个kksCode对应了多个kksName，这些kksCode是%s，这些kksName是%s" % (
					queryRes['kksCodes'].values, queryRes['dictNames'].values))
			if res:
				_kksName = _kksName + res.tolist()
			else:
				_kksName.append(eachCode_toReplace)
		return _kksName


class timeTrans:
	"""
	【执行流程与参数说明】 \n
	①实例化对象
	    e.g:
	            timestamp = [1617159398000, 1617259398000, 1617359398000, 1617359398] \n
				obj = timeTrans(unixTime=timestamp, format='%Y/%m/%d %H:%M:%S') \n
				print(obj.timeStr) \n
	    param:
	            unixTime:秒级或毫秒级时间，int or list，形如1616059398000或[1617159398000, 1617259398000, 1617359398000, 1617359398] \n
	            format:字符串型时间，str or None，形如“%Y/%m/%d %H:%M:%S” \n
	"""

	def __init__(self, **kwargs):
		def unixTime2strTime(_unixTime, _format):
			unixTimeLength = len(str(_unixTime))
			second = _unixTime if unixTimeLength == 10 else _unixTime / 1000
			_strTime = time.strftime(_format, time.localtime(second))
			return _strTime

		self.unixTime = kwargs['unixTime']
		self.format = kwargs['format'] if 'format' in kwargs.keys() else "%Y-%m-%d %H:%M:%S"
		isInt = isinstance(self.unixTime, int)
		isTuple = isinstance(self.unixTime, list)
		if isInt:
			self.timeStr = unixTime2strTime(self.unixTime, self.format)
		elif isTuple:
			timeStr = []
			for item in self.unixTime:
				_timeStr = unixTime2strTime(item, self.format)
				timeStr.append(_timeStr)
			self.timeStr = timeStr
		else:
			self.timeStr = None
