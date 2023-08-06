from __future__ import print_function, division, absolute_import

from Qt.QtCore import Qt, Signal, QSize, QEvent
from Qt.QtWidgets import QWidget, QDockWidget, QLabel, QLineEdit, QToolButton, QGroupBox

from tpDcc.managers import resources
from tpDcc.libs.qt.widgets import layouts


class DockWidget(QDockWidget, object):
    closed = Signal(object)

    def __init__(self, name, parent=None):
        super(DockWidget, self).__init__(parent=parent)

        self.setWindowTitle(name)
        self.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.setAllowedAreas(
            Qt.BottomDockWidgetArea | Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea | Qt.TopDockWidgetArea)
        self.setObjectName(name)
        self.setTitleBarWidget(DockTitleBar(self))
        self.setFloating(False)

    def closeEvent(self, event):
        self.closed.emit(self)
        event.accept()

    def add_button(self, button):
        self.titleBarWidget().add_button(button)


class DockTitleBar(QWidget, object):
    def __init__(self, dock_widget, renamable=False):
        super(DockTitleBar, self).__init__(dock_widget)

        self._renamable = renamable

        main_layout = layouts.HorizontalLayout(spacing=1, margins=(0, 0, 0, 1))
        self.setLayout(main_layout)

        self._buttons_box = QGroupBox('')
        self._buttons_box.setObjectName('Docked')
        self._buttons_layout = layouts.HorizontalLayout(spacing=0, margins=(0, 0, 0, 0))
        self._buttons_layout.setSpacing(1)
        self._buttons_layout.setMargin(2)
        self._buttons_box.setLayout(self._buttons_layout)
        main_layout.addWidget(self._buttons_box)

        self._title_label = QLabel(self)
        self._title_label.setStyleSheet('background: transparent')
        self._title_edit = QLineEdit(self)
        self._title_edit.setVisible(False)

        self._button_size = QSize(15, 15)

        self._dock_btn = QToolButton(self)
        self._dock_btn.setIcon(resources.icon('restore_window', theme='color'))
        self._dock_btn.setMaximumSize(self._button_size)
        self._dock_btn.setAutoRaise(True)
        self._close_btn = QToolButton(self)
        self._close_btn.setIcon(resources.icon('close_window', theme='color'))
        self._close_btn.setMaximumSize(self._button_size)
        self._close_btn.setAutoRaise(True)

        self._buttons_layout.addSpacing(2)
        self._buttons_layout.addWidget(self._title_label)
        self._buttons_layout.addWidget(self._title_edit)
        self._buttons_layout.addStretch()
        self._buttons_layout.addSpacing(5)
        self._buttons_layout.addWidget(self._dock_btn)
        self._buttons_layout.addWidget(self._close_btn)

        self._buttons_box.mouseDoubleClickEvent = self.mouseDoubleClickEvent
        self._buttons_box.mousePressEvent = self.mousePressEvent
        self._buttons_box.mouseMoveEvent = self.mouseMoveEvent
        self._buttons_box.mouseReleaseEvent = self.mouseReleaseEvent

        dock_widget.featuresChanged.connect(self._on_dock_features_changed)
        self._title_edit.editingFinished.connect(self._on_finish_edit)
        self._dock_btn.clicked.connect(self._on_dock_btn_clicked)
        self._close_btn.clicked.connect(self._on_close_btn_clicked)

        self._on_dock_features_changed(dock_widget.features())
        self.set_title(dock_widget.windowTitle())
        dock_widget.installEventFilter(self)
        dock_widget.topLevelChanged.connect(self._on_change_floating_style)

    @property
    def renamable(self):
        return self._renamable

    @renamable.setter
    def renamable(self, flag):
        self._renamable = flag

    def eventFilter(self, obj, event):
        try:
            if event.type() == QEvent.WindowTitleChange:
                self.set_title(obj.windowTitle())
            return super(DockTitleBar, self).eventFilter(obj, event)
        except Exception as exc:
            event.accept()
            return True

    def mouseMoveEvent(self, event):
        event.ignore()

    def mousePressEvent(self, event):
        event.ignore()

    def mouseReleaseEvent(self, event):
        event.ignore()

    def mouseDoubleClickEvent(self, event):
        if event.pos().x() <= self._title_label.width() and self._renamable:
            self._start_edit()
        else:
            super(DockTitleBar, self).mouseDoubleClickEvent(event)

    def update(self, *args, **kwargs):
        self._on_change_floating_style(self.parent().isFloating())
        super(DockTitleBar, self).update(*args, **kwargs)

    def set_title(self, title):
        self._title_label.setText(title)
        self._title_edit.setText(title)

    def add_button(self, button):
        button.setAutoRaise(True)
        button.setMaximumSize(self._button_size)
        self._buttons_layout.insertWidget(5, button)

    def _start_edit(self):
        self._title_label.hide()
        self._title_edit.show()
        self._title_edit.setFocus()

    def _finish_edit(self):
        self._title_edit.hide()
        self._title_label.show()
        self.parent().setWindowTitle(self._title_edit.text())

    def _on_dock_features_changed(self, features):
        if not features & QDockWidget.DockWidgetVerticalTitleBar:
            self._close_btn.setVisible(features & QDockWidget.DockWidgetClosable)
            self._dock_btn.setVisible(features & QDockWidget.DockWidgetFloatable)
        else:
            raise ValueError('Vertical title bar is not supported!')

    def _on_finish_edit(self):
        self._finish_edit()

    def _on_dock_btn_clicked(self):
        self.parent().setFloating(not self.parent().isFloating())

    def _on_close_btn_clicked(self):
        self.parent().toggleViewAction().setChecked(False)
        self.parent().close()

    def _on_change_floating_style(self, state):
        pass
