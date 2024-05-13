#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<Lenovo>----------------------------
# 传建时间: 2024/5/8 下午4:43
# 当前项目名: Python
# 编码模式: utf-8
# 注释: 
# -------------------------<Lenovo>----------------------------
from typing import Literal, Callable
from functools import wraps
from warnings import warn
from traceback import format_exc


__all__ = [
    'debuger'
]


class debuger:
    """
    调试器.

    Example::

        >>> @debuger('log', group='test', info='test info', note='test note')
        >>> def func():
        >>>     print(1 / 0)
        >>> func()
        >>> debuger.raiseErrorGroup()
        >>> #Error...

    Attributes:
        :ivar _option: 调试选项,可选值为'print', 'ignore', 'log', 'warn', 'raise', 'stop'.
        :ivar group: 调试组.
        :ivar info: 调试信息.
        :ivar note: 调试备注.
        :ivar fromError: 引发错误的异常.

    Methods:
        :meth:`__new__`: 单例模式.
        :meth:`__init__`: 初始化调试器.
        :meth:`__call__`: 装饰器,用于装饰函数.
        :meth:`handleError`: 处理错误.
        :meth:`_formatErrorGroup`: 将错误记录字典(dict)递归的组装成嵌套的ExceptionGroup字典.
        :meth:`raiseErrorGroup`: 引发错误组.
    """
    _instance = None

    errorLog = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)

        cls._instance.option = 'log'
        cls._instance.group = 'default'
        cls._instance.info = None
        cls._instance.note = None
        cls._instance.fromError = None

        return cls._instance

    def __init__(self, option: Literal['print', 'ignore', 'log', 'warn', 'raise', 'stop'] = 'log', *, group: str = 'default', info: str | None = None, note: str | None = None, fromError: Exception | type[Exception] | None = None):
        """
        初始化调试器.

        :param option: 调试选项,可选值为'print','ignore','log','warn','raise','stop'.
        :type option: str
        :keyword group: 调试组.
        :type group: str
        :keyword info: 调试信息.
        :type info: str
        :keyword note: 调试备注.
        :type note: str
        :keyword fromError: 引发错误的异常.
        :type fromError: Exception | type[Exception]
        """
        self._option = option
        self.group = group
        self.info = info
        self.note = note
        self.fromError = fromError

    @property
    def option(self) -> str:
        """
        :return: 调试选项,可选值为'print', 'ignore', 'log', 'warn', 'raise', 'stop'.
        """
        return self._option

    @option.setter
    def option(self, value: Literal['print', 'ignore', 'log', 'warn', 'raise']):
        self._option = value

    def __call__(self, func: Callable) -> Callable:
        """
        装饰器,用于装饰函数.

        :param func: 被装饰的函数.
        :type func: Callable
        :return: 装饰后的函数.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except Exception as e:
                self._handleError(e, info=format_exc())

        return wrapper

    def _handleError(self, e: Exception, *, info: str) -> None:
        """
        根据调试选项处理错误.

        :param e: 错误.
        :type e: Exception
        :keyword info: 错误信息.
        :type info: str
        """
        if self.note: e.add_note(self.note)
        info = self.info if self.info else info

        match self.option:
            case 'print':
                print(f"[{self.group}]: {info}")

            case 'ignore':
                pass

            case 'log':
                if self.group in self.errorLog:
                    self.errorLog[self.group].append(e)
                else:
                    self.errorLog[self.group] = [e]

            case 'warn':
                warn(
                    f"[{self.group}]: {info}")

            case 'raise':
                if self.fromError:
                    raise e from self.fromError

                else:
                    raise e

            case 'stop':
                exit(f"不可恢复的错误导致程序退出: \n{info}")

    @classmethod
    def _formatErrorGroup(cls, *, _lastKey: list = None, _result: list = None) -> ExceptionGroup:
        """
        将错误记录字典(dict)递归的组装成嵌套的ExceptionGroup字典.

        :keyword _lastKey: 上一个键
        :type _lastKey: list
        :keyword _result: 结果
        :type _result: list
        :return: 如果_lastKey不为空,则返回ExceptionGroup字典,否则递归的执行_formatErrorGroup函数.
        :rtype: ExceptionGroup | dict
        """
        if _lastKey is not None:
            if len(_lastKey):
                firstKey = _lastKey[0]

                _result = [firstKey, cls.errorLog[firstKey] + [ExceptionGroup(*_result)]]

                return cls._formatErrorGroup(_lastKey=_lastKey[1:], _result=_result)

            else:

                return ExceptionGroup(*_result)

        else:
            if not isinstance(list(cls.errorLog.values())[0], list):
                return ExceptionGroup(
                    "Error", [ValueError(f"[{cls.__name__}内部错误]: 类<{cls.__name__}>的错误记录字典的值必须为列表!")])

            firstKey, _lastKey = (keyList := list(cls.errorLog.keys()))[0], keyList[1:]

            _result = [firstKey, cls.errorLog[firstKey]]

            return cls._formatErrorGroup(_lastKey=_lastKey, _result=_result)

    @classmethod
    def raiseErrorGroup(cls) -> None:
        """
        引发错误组.
        """
        if cls.errorLog:
            raise cls._formatErrorGroup()


if __name__ == '__main__':
    pass
