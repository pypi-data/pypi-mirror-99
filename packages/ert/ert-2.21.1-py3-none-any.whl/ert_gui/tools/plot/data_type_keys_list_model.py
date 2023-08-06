from qtpy.QtCore import QAbstractItemModel, QModelIndex, Qt
from qtpy.QtGui import QColor

from ert_gui.ertwidgets import resourceIcon


class DataTypeKeysListModel(QAbstractItemModel):
    DEFAULT_DATA_TYPE = QColor(255, 255, 255)
    HAS_OBSERVATIONS = QColor(237, 218, 116)
    GROUP_ITEM = QColor(64, 64, 64)

    def __init__(self, keys):
        """
        @type ert: res.enkf.EnKFMain
        """
        QAbstractItemModel.__init__(self)
        self._keys = keys
        self.__icon = resourceIcon("ide/small/bullet_star")

    def index(self, row, column, parent=None, *args, **kwargs):
        return self.createIndex(row, column)

    def parent(self, index=None):
        return QModelIndex()

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._keys)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return 1

    def data(self, index, role=None):
        assert isinstance(index, QModelIndex)

        if index.isValid():
            items = self._keys
            row = index.row()
            item = items[row]

            if role == Qt.DisplayRole:
                return item["key"]
            elif role == Qt.BackgroundRole:
                if len(item["observations"]) > 0:
                    return self.HAS_OBSERVATIONS

    def itemAt(self, index):
        assert isinstance(index, QModelIndex)

        if index.isValid():
            row = index.row()
            return self._keys[row]

        return None
