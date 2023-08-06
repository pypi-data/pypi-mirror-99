import time

import pandas as pd
import numpy as np


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
		checkStr01 = "待检编码中有重复项 X " if isinstance(_kksCode, list) and len(np.unique(_kksCode)) != len(_kksCode) else "待检编码中没有重复项 √ "
		checkStr02 = "编码中没有重复项 √ " if len_kksCodes == len_kksCodes_unique else "编码中有重复项 X "
		checkStr03 = "名称中没有重复项 √ " if len_dictNames == len_dictNames_unique else "名称中有重复项 (允许) "
		print("#"*2*(2+max([len(checkStr01), len(checkStr02), len(checkStr03)])))
		print('\t', checkStr01, '\n\t', checkStr02, '\n\t', checkStr03)
		print("#"*2*(2+max([len(checkStr01), len(checkStr02), len(checkStr03)])))
	# 字典以中文名称为依据，升序排列
	_dict = pd.DataFrame({'kksCodes': _kksCodes, 'dictNames': _dictNames}).sort_values(by=['dictNames'])
	# 查询
	_kksName = []
	if isinstance(_kksCode, list):
		for eachCode_toReplace in _kksCode:
			res = _dict.query("kksCodes.str.contains(\'" + eachCode_toReplace + "\')", engine='python')['dictNames'].values
			_kksName = _kksName + res.tolist()
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
