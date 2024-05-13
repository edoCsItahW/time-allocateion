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
# 注释: 
# -------------------------<edocsitahw>----------------------------
from typing import Literal, final, overload
from datetime import time, datetime, timedelta
from functools import cached_property
from abc import ABC, abstractmethod, abstractproperty
from warnings import warn
from deprecated import deprecated
from atexit import register


@register
def end(): print("程序结束")


class duration:
    def __init__(self, *, seconds: int | float = None, minutes: int | float = None, hours: int | float = None):
        if len(list(f := filter(bool, [seconds, minutes, hours]))) > 1:
            raise ValueError(
                f"只能设置一个时间单位!")

        self._seconds = seconds if seconds else minutes * 60 if minutes else hours * 3600
        self._minutes = minutes if minutes else seconds / 60 if seconds else hours * 60
        self._hours = hours if hours else seconds / 3600 if seconds else minutes / 60

    @property
    def seconds(self): return self._seconds

    @property
    def minutes(self): return self._minutes

    @property
    def hours(self): return self._hours

    @staticmethod
    def calcTimeDuration(start: time, end: time) -> 'duration':
        return duration(seconds=(datetime.combine(datetime.today(), end) - datetime.combine(datetime.today(), start)).total_seconds())


weekTotalSecond = duration(seconds=timedelta(weeks=1).total_seconds())


class task(ABC):
    def __init__(self, name: str, day: Literal["Mon", "Tue", "Wen", "Thu", "Fri", "Sat", "Sun"] | datetime = None, start: time = None, end: time = None, *, weight: float = None):
        self._name = name
        self._start = start
        self._end = end
        self._weight = weight
        self._day = day

    @final
    @property
    def name(self):
        return self._name

    @property
    def start(self):
        if hasattr(self, "_start"):
            return self._start

        warn(
            f"在引用该私有属性前,请先设置开始时间!")

    @start.setter
    def start(self, value: time):
        self._start = value

    @property
    def end(self):
        if hasattr(self, "_end"):
            return self._end

        warn(
            f"在引用该私有属性前,请先设置结束时间!")

    @end.setter
    def end(self, value: time):
        self._end = value

    @final
    @property
    def weight(self):
        return self._weight

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
    def duration(self): return duration.calcTimeDuration(self.start, self.end)

    @final
    @cached_property
    def time(self):
        return duration(seconds=self.duration.seconds * self.weight)

    @final
    @cached_property
    def type(self):
        return "C" if self.start and self.end else "V"

    @final
    def __repr__(self):
        return f"<{self.name}[{self.type}]:" + ("auto" if self.type.lower() == "v" else f"{self.start.strftime('%H.%M')}-{self.end.strftime('%H.%M')}") + ">"


class varTask(task):
    def __init__(self, name: str, *, weight: float = None):
        super().__init__(name, weight=weight)


class constTask(task):
    def __init__(self, name: str, day: Literal["Mon", "Tue", "Wen", "Thu", "Fri", "Sat", "Sun"] | datetime, start: time = None, end: time = None):
        super().__init__(name, day, start, end)


class allocation:
    def __init__(self, dayStart: time = time(8, 30), dayEnd: time = time(21, 0)):
        self._keys = ["Mon", "Tue", "Wen", "Thu", "Fri", "Sat", "Sun"]
        self._dayStart = dayStart
        self._dayEnd = dayEnd
        self._dayTable = {k: [constTask(f"{k}FT", k, self.dayStart, self.dayEnd)] for k in self._keys}
        self._allocateList = []

    @property
    def dayTable(self): return self._dayTable

    @dayTable.setter
    def dayTable(self, value): self._dayTable = value

    @property
    def dayStart(self): return self._dayStart

    @property
    def dayEnd(self): return self._dayEnd

    @property
    def dayDuration(self): return duration.calcTimeDuration(self.dayStart, self.dayEnd)

    @property
    def allocateList(self): return self._allocateList

    @allocateList.setter
    def allocateList(self, value): self._allocateList = value

    def addTask(self, name: str, day: Literal["Mon", "Tue", "Wen", "Thu", "Fri", "Sat", "Sun"] = None, start: time = None, end: time = None, *, weight: float = None):
        if day and start and end:
            self.dayTable[day].append(constTask(name, day, start, end, weight=weight))
        else:
            self.allocateList.append(varTask(name, weight=weight))

    def getFreeTask(self, day: Literal["Mon", "Tue", "Wen", "Thu", "Fri", "Sat", "Sun"]):
        return [i for i in self.dayTable[day] if i.name == f"{i}FT"][0]

    def allocate(self):
        for t in self.allocateList:
            t: varTask
            for k, dlist in self.dayTable.items():
                if t.duration.seconds >= self.getFreeTask(k).duration.seconds:
                    pass
                # TODO: 实现分配算法


if __name__ == '__main__':
    a = allocation()
    a.addTask("task1", weight=1.0)
    print(a.dayTable)
