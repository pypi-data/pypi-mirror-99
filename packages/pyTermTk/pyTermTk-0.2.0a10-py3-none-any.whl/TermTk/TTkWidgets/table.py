#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.color import TTkColor
from TermTk.TTkWidgets.tableview import TTkTableView
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkAbstract.abstractscrollarea import TTkAbstractScrollArea

class TTkTable(TTkAbstractScrollArea):
    __slots__ = ('_tableView', 'activated')
    def __init__(self, *args, **kwargs):
        TTkAbstractScrollArea.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , 'TTkTable' )
        if 'parent' in kwargs: kwargs.pop('parent')
        self._tableView = TTkTableView(*args, **kwargs)
        # Forward the signal
        self.activated = self._tableView.activated

        self.setFocusPolicy(TTkK.ClickFocus)
        self.setViewport(self._tableView)

    def setAlignment(self, *args, **kwargs)   :
        self._tableView.setAlignment(*args, **kwargs)
    def setHeader(self, *args, **kwargs)      :
        self._tableView.setHeader(*args, **kwargs)
    def setColumnSize(self, *args, **kwargs)  :
        self._tableView.setColumnSize(*args, **kwargs)
    def setColumnColors(self, *args, **kwargs):
        self._tableView.setColumnColors(*args, **kwargs)
    def appendItem(self, *args, **kwargs)     :
        self._tableView.appendItem(*args, **kwargs)




