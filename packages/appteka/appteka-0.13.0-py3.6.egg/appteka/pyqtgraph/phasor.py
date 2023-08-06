# appteka - helpers collection

# Copyright (C) 2018-2021 Aleksandr Popov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.

# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Implementation of the phasor diagram."""

from math import degrees
from warnings import warn
import cmath
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets


DEFAULT_WIDGET_SIZE = QtCore.QSize(500, 500)

CIRCLES_NUM = 6
DEFAULT_COLOR = (255, 255, 255)
DEFAULT_WIDTH = 1


class PhasorDiagram(pg.PlotWidget):
    """Widget for plotting phasor diagram.

    Parameters
    ----------
    parent: object
        Parent object
    """

    def __init__(self, parent=None, size=None, end=None):
        super().__init__(parent)

        if size is not None:
            warn("size arg is deprecated and ignored", FutureWarning)

        if end is not None:
            warn("end arg is deprecated and ignored", FutureWarning)

        self.setAspectLocked(True)
        self.addLine(x=0, pen=0.2)
        self.addLine(y=0, pen=0.2)
        self.showAxis('bottom', False)
        self.showAxis('left', False)

        policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Preferred,
        )
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)

        self.__build_grid()
        self.__build_labels()

        self.set_range(1)

        self.setMouseEnabled(x=False, y=False)
        self.disableAutoRange()
        self.plotItem.setMenuEnabled(False)
        self.hideButtons()

        self.__legend = None
        self.__phasors = {}
        self.__items = {}
        self.__names = {}

    def set_range(self, value):
        """Set range of diagram."""
        self.__range = value
        self.__update_grid()
        self.__update_labels()

    def add_phasor(self, key, amp=0, phi=0,
                   color=DEFAULT_COLOR, width=DEFAULT_WIDTH,
                   name=None):

        """Add phasor to the diagram."""

        line = self.plot(
            pen=pg.mkPen(color, width=width),
        )

        arr = pg.ArrowItem(
            tailLen=0,
            tailWidth=1,
            pen=pg.mkPen(color, width=width),
            headLen=width+4,
            brush=None,
        )
        self.addItem(arr)

        self.__items[key] = {'line': line, 'arr': arr}
        self.__names[key] = name

        self.update_phasor(key, amp, phi)

    def set_phasor_visible(self, key, value=True):
        """Hide or show phasor."""
        if key not in self.__items:
            return

        for item in self.__items[key]:
            self.__items[key][item].setVisible(value)

    def update_phasor(self, key, amp, phi):
        """Change phasor value."""
        self.__phasors[key] = (amp, phi)
        self.__update()

    def remove_phasors(self):
        """Remove phasors and legend."""

        for key in self.__items:
            for subkey in self.__items[key]:
                self.removeItem(self.__items[key][subkey])

        self.__items = {}
        self.__names = {}
        self.__phasors = {}

        if self.__legend is not None:
            self.__legend.clear()
            self.removeItem(self.__legend)

        self.__legend = None

    def show_legend(self):
        """Show legend."""

        if self.__legend:
            return

        self.__legend = self.plotItem.addLegend()
        for key in self.__items:
            name = self.__names[key]
            if name:
                self.plotItem.legend.addItem(
                    self.__items[key]['line'], name)
            else:
                self.plotItem.legend.addItem(
                    self.__items[key]['line'], key)

    def __update(self):
        for key in self.__phasors:
            phasor = self.__phasors[key]
            compl = cmath.rect(*phasor)
            x = compl.real
            y = compl.imag

            items = self.__items[key]

            items['line'].setData([0, x], [0, y])

            arr = items['arr']
            arr.setStyle(angle=180 - degrees(phasor[1]))
            arr.setPos(x, y)

    def __build_grid(self):
        self.circles = []
        for _ in range(CIRCLES_NUM):
            circle = pg.QtGui.QGraphicsEllipseItem()
            circle.setPen(pg.mkPen(0.2))
            self.circles.append(circle)
            self.addItem(circle)

    def __update_grid(self):
        for i in range(CIRCLES_NUM):
            rad = (i + 1) * self.__range / CIRCLES_NUM
            self.circles[i].setRect(-rad, -rad, rad*2, rad*2)

        self.setRange(QtCore.QRectF(-rad, rad, 2*rad, -2*rad))

    def __build_labels(self):
        self.labels = []
        for _ in range(2):
            label = pg.TextItem()
            self.labels.append(label)
            self.addItem(label)

    def __update_labels(self):
        self.labels[0].setText("{}".format(self.__range / 2))
        self.labels[0].setPos(0, self.__range / 2)
        self.labels[1].setText("{}".format(self.__range))
        self.labels[1].setPos(0, self.__range)

    def sizeHint(self):
        # pylint: disable=invalid-name,no-self-use,missing-docstring
        return DEFAULT_WIDGET_SIZE

    def heightForWidth(self, width):
        # pylint: disable=invalid-name,no-self-use,missing-docstring
        return width
