#! /user/bin/python3

#  Copyright (c) 2024. All rights reserved.
#  This source code is licensed under the CC BY-NC-SA
#  (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
#  This software is protected by copyright law. Reproduction, distribution, or use for commercial
#  purposes is prohibited without the author's permission. If you have any questions or require
#  permission, please contact the author: 2207150234@st.sziit.edu.cn

# -------------------------<edocsitahw>----------------------------
# 传建时间: 2024/5/9 上午9:10
# 当前项目名: pyAndWeb
# 编码模式: utf-8
# 注释: comment style is reStructuredText
# -------------------------<edocsitahw>----------------------------
from typing import Literal, final, overload, Self, Generic, LiteralString
from datetime import time, datetime, timedelta
from functools import cached_property, singledispatchmethod
from abc import ABC, abstractmethod, abstractproperty
from warnings import warn
from deprecated import deprecated
from atexit import register
from time import time as now
from debuger import debuger
from inspect import currentframe
from dataclasses import dataclass
from collections import OrderedDict

NOW = now()


@register
def pargramEnd(): print(f"程序结束,运行时长: '{now() - NOW:.2f}'")


@dataclass
class duration:
    """
    封装了时长单位

    Example::
        >>> d = duration(seconds=3600)
        >>> print(d.seconds)
        3600
        >>> print(d.minutes)
        60
        >>> print(d.hours)
        1

    Attributes:
        :ivar _seconds: 秒
        :ivar _minutes: 分
        :ivar _hours: 小时

    Methods::
        :meth:`calcTimeDuration`: 计算两个时间差的时长
    """

    def __init__(self, *, seconds: int | float = None, minutes: int | float = None, hours: int | float = None):
        """
        初始化时长单位

        :keyword seconds: 秒
        :keyword minutes: 分
        :keyword hours: 小时
        :raises ValueError: 不能设置多个时间单位
        """
        if len(list(f := filter(bool, [seconds, minutes, hours]))) > 1:
            raise ValueError(
                f"只能设置一个时间单位!")

        self._seconds = seconds if seconds else minutes * 60 if minutes else hours * 3600
        self._minutes = round(minutes if minutes else seconds / 60 if seconds else hours * 60, 4)
        self._hours = round(hours if hours else seconds / 3600 if seconds else minutes / 60, 4)

    @property
    def seconds(self): return self._seconds

    @property
    def minutes(self): return self._minutes

    @property
    def hours(self): return self._hours

    def __add__(self, other: Self | int | float):
        return duration(seconds=self.seconds + (other.seconds if isinstance(other, duration) else other))

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other: Self | int | float):
        return duration(seconds=self.seconds - (other.seconds if isinstance(other, duration) else other))

    def __rsub__(self, other):
        return duration(seconds=(other.seconds if isinstance(other, duration) else other) - self.seconds)

    def __mul__(self, other: int):
        return duration(seconds=self.seconds * other)

    def __rmul__(self, other: int):
        return self.__mul__(other)

    def __truediv__(self, other):
        return duration(seconds=self.seconds / other)

    def __rtruediv__(self, other):
        return duration(seconds=other / self.seconds)

    def __floordiv__(self, other):
        return duration(seconds=self.seconds // other)

    def __rfloordiv__(self, other):
        return duration(seconds=other // self.seconds)

    def __eq__(self, other):
        return self.seconds == (other.seconds if isinstance(other, duration) else other)

    def __lt__(self, other):
        return self.seconds < (other.seconds if isinstance(other, duration) else other)

    def __le__(self, other):
        return self.seconds <= (other.seconds if isinstance(other, duration) else other)

    def __gt__(self, other):
        return self.seconds > (other.seconds if isinstance(other, duration) else other)

    def __ge__(self, other):
        return self.seconds >= (other.seconds if isinstance(other, duration) else other)

    def __repr__(self):
        return f"<duration: {self.seconds:_.4f}s>"

    @staticmethod
    @debuger('log', group="duration", note="计算时间差时出现异常!")
    def calcTimeDuration(start: time, end: time) -> 'duration':
        """
        计算两个time对象的时间差

        :param start: 开始时间
        :type start: time
        :param end: 结束时间
        :type end: time
        :return: 时长对象
        :rtype: duration
        """
        return duration(seconds=(datetime.combine(datetime.today(), end) - datetime.combine(datetime.today(),
                                                                                            start)).total_seconds())


WEEK_DAYS = ["Mon", "Tue", "Wen", "Thu", "Fri", "Sat", "Sun"]


class Task(ABC):
    """
    任务基类

    Attributes:
        :ivar name: 任务名称
        :ivar _start: 开始时间
        :ivar _end: 结束时间
        :ivar _day: 星期
    """

    def __init__(self, name: str, day: Literal["Mon", "Tue", "Wen", "Thu", "Fri", "Sat", "Sun"] | str = None,
                 start: time = None, end: time = None):
        self.name = name
        self._start = start
        self._end = end
        self._day = day

    @property
    def start(self):
        if hasattr(self, "_start"):
            return self._start

        warn(
            f"在引用该私有属性前,请先设置开始时间!")

    @property
    def end(self):
        if hasattr(self, "_end"):
            return self._end

        warn(
            f"在引用该私有属性前,请先设置结束时间!")

    @final
    @property
    def day(self):
        if hasattr(self, "_day"):
            return self._day

        warn(
            f"在引用该私有属性前,请先设置星期!")

    @day.setter
    def day(self, value: str):
        self._day = value

    @final
    @property
    def duration(self):
        return duration.calcTimeDuration(self.start, self.end)

    @final
    @cached_property
    def uuid(self):
        return str(id(self))

    @abstractmethod
    @cached_property
    def type(self):
        raise NotImplemented(
            f"请在子类中实现该方法!")

    @final
    def __repr__(self):
        return f"<{self.name}[{self.type}]:" + (
            "auto" if self.type.lower() == "v" else f"{self.start.strftime('%H.%M')}-{self.end.strftime('%H.%M')}") + ">"


class varTask(Task):
    def __init__(self, name: str, *, weight: float = None):
        super().__init__(name)
        self._start = None
        self._end = None
        self._day = None
        self._weigth = weight

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value: time):
        self._start = value

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value: time):
        self._end = value

    @cached_property
    def type(self):
        return "V"


class fixTask(Task):
    def __init__(self, name: str, day: Literal["Mon", "Tue", "Wen", "Thu", "Fri", "Sat", "Sun"] | str,
                 start: time = None, end: time = None):
        super().__init__(name, day, start, end)

    @cached_property
    def type(self):
        return "F"


class weekTable:
    def __init__(self, dayStart: time = None, dayEnd: time = None):
        """
        初始化一周的表格

        :param dayStart: 一天的开始时间
        :type dayStart: time
        :param dayEnd: 一天的结束时间
        :type dayEnd: time
        """
        self._dayStart = dayStart if dayStart else time(7, 30)
        self._dayEnd = dayEnd if dayEnd else time(11, 30)
        self._table = {k: {"task": OrderedDict(), "free": self.dayDuration} for k in WEEK_DAYS}
        self._allocList = []

    @property
    def dayStart(self):
        """每天的开始时间(作息)"""
        return self._dayStart

    @property
    def dayEnd(self):
        """每天的结束时间(作息)"""
        return self._dayEnd

    @property
    def table(self):
        """
        一周的表格

        tableFrame::
            {
                "星期": {
                    "task": {
                        "UUID": task
                    },
                    "free": duration
                }
            }
        """
        return self._table

    @property
    def allocList(self):
        return self._allocList

    @cached_property
    def dayDuration(self):
        return duration.calcTimeDuration(self.dayStart, self.dayEnd)

    @singledispatchmethod
    def addTask(self, _task: Task):
        raise TypeError(
            f"参数类型错误,只能添加任务类型为'varTask'或'fixTask'的对象!")

    @addTask.register(fixTask)
    @debuger('log', group="weekTable", note="添加固定任务时出现异常!")
    def _(self, _task: fixTask):
        if _task.duration > self.dayDuration:
            raise ValueError(
                f"任务时间超过一天!")

        else:
            self.table[_task.day]["task"][_task.uuid] = _task  # type: ignore

            self.table[_task.day]["free"] -= _task.duration  # type: ignore

    @addTask.register(varTask)
    @debuger('log', group="weekTable", note="添加可变任务时出现异常!")
    def _(self, _task: varTask):
        self._allocList.append(_task)

    @debuger('log', group="weekTable", note="移除任务时出现异常!")
    def removeTask(self, _task: Task):
        if _task.type == "F":
            try:
                del self.table[_task.day]["task"][_task.uuid]  # type: ignore

                self.table[_task.day]["free"] += _task.duration  # type: ignore
            except KeyError:
                warn(
                    f"移除任务失败,失败原因: 索引'{_task.uuid}'不存在!")


class allocation:
    def __init__(self, _weekTable: weekTable):
        self._weekTable = _weekTable
        self._allocList = self._weekTable.allocList

    @property
    def weekTable(self): return self._weekTable

    @property
    def allocList(self): return self._allocList

    def allocate(self):
        """
        分配任务
        """
        for task in range(len(self.allocList)):
            if self.allocList:
                task = self.allocList.pop(0)

                # TODO: 解决在一天中寻找可以用的时间段的问题

    def accumFreeTime(self) -> duration:
        """计算周表的空闲时间"""
        return sum(self.weekTable.table[k]["free"] for k in WEEK_DAYS)  # type: ignore


if __name__ == '__main__':
    # 测试代码
    table = weekTable()
    table.addTask(fixTask("first class", "Mon", time(8, 30), time(11, 50)))
    table.addTask(varTask("finish homework", weight=0.6))
    alloc = allocation(table)
    print(alloc.accumFreeTime())
