from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from .SettingsConstants import ApplicationSettings as aps
from ..widgets.info_label import InfoLabel
from .Constants import StyleSheets as ss

from ez_settings import EZSettings

class NodeView(QGraphicsView):
    def __init__(self, scene, parent):
        super(NodeView, self).__init__(parent)
        if EZSettings().get(aps.chk_high_quality_view, True):
            self.setRenderHint(QPainter.HighQualityAntialiasing)
        self.setObjectName("View")
        self.setScene(scene)

        self.zoom = 5

        self.setDragMode(QGraphicsView.RubberBandDrag)

        self.scale(0.45, 0.45)

        font = QFont()
        font.setPointSize(8)
        font.setItalic(True)
        font.setFamily("sans-serif")
        self.title_label = QLabel("Tangle: a Python node editor")
        self.title_label.setFont(font)
        self.title_label.setScaledContents(True)

        self.info_label = InfoLabel("")

        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(30, 30, 30, 30)
        self.grid_layout.addWidget(self.info_label, 0, 0, 0, 0, Qt.AlignTop | Qt.AlignCenter)
        self.grid_layout.addWidget(self.title_label, 1, 2, 1, 2, Qt.AlignBottom | Qt.AlignRight)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            release_event = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                       Qt.LeftButton, Qt.NoButton, event.modifiers())
            super().mouseReleaseEvent(release_event)
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            fake_event = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                    Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
            super().mousePressEvent(fake_event)
        else:
            event.accept()
            super(NodeView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                    Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())
            super().mouseReleaseEvent(fakeEvent)
            self.setDragMode(QGraphicsView.RubberBandDrag)
        else:
            event.accept()
            super(NodeView, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            if self.zoom < 30:
                self.zoom += 1
                self.scale(1.1, 1.1)
        else:
            if self.zoom > 0.8:
                self.zoom -= 1
                self.scale(0.9, 0.9)



