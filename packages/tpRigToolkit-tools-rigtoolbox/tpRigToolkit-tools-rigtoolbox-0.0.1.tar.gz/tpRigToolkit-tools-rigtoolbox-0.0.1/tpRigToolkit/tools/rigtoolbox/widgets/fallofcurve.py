#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains fallof curve widget implementation
"""

from Qt.QtCore import Qt, Signal, QObject, QPoint, QPointF, QRect, QRectF, QLineF
from Qt.QtWidgets import QApplication, QMenuBar, QUndoStack, QUndoCommand, QGraphicsView
from Qt.QtWidgets import QGraphicsItem, QGraphicsPathItem, QGraphicsScene, QGraphicsLineItem, QGraphicsRectItem
from Qt.QtGui import QColor, QPainterPath, QPainter, QPen, QBrush, QRadialGradient, QKeySequence, QKeyEvent

from tpDcc.libs.python import bezier
from tpDcc.libs.resources.core import theme
from tpDcc.libs.qt.core import base
from tpDcc.libs.qt.widgets import layouts, dividers, combobox, checkbox


@theme.mixin
class FallofCurveWidget(base.BaseWidget, object):

    curveUpdated = Signal(list)

    def __init__(self, parent=None):
        self._base_size = 300
        self._bezier_dict = {
            'bezier': [
                QPoint(0, 0), QPoint(75, 0),
                QPoint(225, 300), QPoint(300, 300)],
            'linear': [
                QPointF(0.000000, 0.000000), QPointF(75.000000, 75.000000),
                QPointF(225.000000, 225.000000), QPointF(300.000000, 300.000000)]
        }

        super(FallofCurveWidget, self).__init__(parent=parent)
        self.setObjectName('Falloff Curve')
        self.show()

        self.refresh()

    def ui(self):
        super(FallofCurveWidget, self).ui()

        base_rect = QRect(0, 0, self._base_size, self._base_size)

        self._scene = CurveNodeScene(base_rect)
        self._scene.base_size = self._base_size
        self._view = CurveNodeView(parent=self)
        self._view.setScene(self._scene)
        self._view.setGeometry(base_rect)

        self._menu_bar = QMenuBar(self)
        self._menu_bar.addAction(self._scene.undo_action)
        self._menu_bar.addAction(self._scene.redo_action)

        bottom_layout = layouts.HorizontalLayout(spacing=2, margins=(2, 2, 2, 2))
        self._bezier_type_combo = combobox.BaseComboBox(parent=self)
        self._snap_cbx = checkbox.BaseCheckBox('Snap', parent=self)
        bottom_layout.addWidget(self._bezier_type_combo)
        bottom_layout.addWidget(self._snap_cbx)

        self.main_layout.addWidget(self._menu_bar)
        self.main_layout.addWidget(dividers.Divider(parent=self))
        self.main_layout.addWidget(self._view)
        self.main_layout.addWidget(dividers.Divider(parent=self))
        self.main_layout.addLayout(bottom_layout)

    def setup_signals(self):
        self._bezier_type_combo.currentTextChanged.connect(self._on_change_curve)
        self._snap_cbx.toggled.connect(self._on_change_snap)
        self._scene.curveUpdated.connect(self._on_curve_updated)

    def resizeEvent(self, event):
        super(FallofCurveWidget, self).resizeEvent(event)
        self.update_view()

    def update_view(self):
        self._view.fitInView(self._scene.itemsBoundingRect(), Qt.KeepAspectRatio)

    def refresh(self):
        self.update_view()
        self._bezier_type_combo.clear()
        for key, value in self._bezier_dict.items():
            self._bezier_type_combo.addItem(key)
        self._scene.undo_stack.clear()

    def curve_as_points(self):
        points = self._scene.bezier_curve.points
        points_list = list()
        for point in points:
            points_list.append([point.x(), point.y()])

        return points_list

    def get_division_data(self, divisions=11):
        percentage = 1 / (divisions - 1.0)
        divisions_list = list()
        for i in range(divisions):
            divisions_list.append(i * percentage)

        return self.get_data_on_points(divisions_list)

    def get_data_on_percentage(self, percentage, points_list=None):
        points_list = points_list or self.curve_as_points()
        return bezier.get_data_on_percentage(percentage, points_list)

    def get_data_on_points(self, in_list=None):
        in_list = in_list or [0.0, 0.2, 0.25, 0.5, 0.6, 0.66, 0.8, 1.0]
        percentage_list = list()
        for point in in_list:
            percentage_list.append(self.get_data_on_percentage(point))

        return percentage_list

    def _on_change_curve(self, text):
        curve_points = self._bezier_dict[text]
        self._scene.undo_stack.push(CurveNodeSwitchUndoCommand(self._scene, self._scene.get_points(), curve_points))
        curve_points = self.curve_as_points()
        self.curveUpdated.emit(curve_points)

    def _on_change_snap(self, flag):
        if not flag:
            self._scene.set_snap(False)
        else:
            self._scene.set_snap(250)

    def _on_curve_updated(self):
        curve_points = self.curve_as_points()
        self.curveUpdated.emit(curve_points)


@theme.mixin
class BezierCurveItem(QGraphicsPathItem, object):
    def __init__(self, parent=None):
        super(BezierCurveItem, self).__init__(parent)

        self._pen = QPen(Qt.green, 2, Qt.SolidLine)
        self._rect = QRectF()
        self._bounding_rect = None
        self._points = list()
        # self._theme = None

        self.setZValue(-1)

    @property
    def points(self):
        return tuple(self._points)

    def boundingRect(self):
        return QRectF(self._bounding_rect or self._rect)

    def paint(self, painter, option, widget):
        self._pen.setColor(self.theme().accent_color if self.theme() else Qt.blue)
        painter.setPen(self._pen)
        painter.drawPath(self.path())

    def update_path(self, points):
        self._points = points
        bezier_path = QPainterPath()
        bezier_path.moveTo(points[0])
        bezier_path.cubicTo(*points[1:])
        self._rect = bezier_path.boundingRect()
        self.setPath(bezier_path)


class CurveNodeItemSignals(QObject):

    curveUpdated = Signal()


@theme.mixin
class CurveNodeItem(QGraphicsItem, object):

    curveUpdated = Signal()
    WIDTH = 10

    def __init__(self, rect=None, parent=None):

        self.signals = CurveNodeItemSignals()
        gradient = QRadialGradient(
            self.WIDTH * 0.75, self.WIDTH * 0.75, self.WIDTH * 0.75, self.WIDTH * 0.75, self.WIDTH * 0.75)
        gradient.setColorAt(0, self.theme().accent_color_6 if self.theme() else QColor.fromRgbF(1, 0.5, 0.01, 1))
        gradient.setColorAt(1, self.theme().accent_color_8 if self.theme() else QColor.fromRgbF(1, 0.6, 0.06, 1))
        self._brush = QBrush(gradient)
        self._brush.setStyle(Qt.RadialGradientPattern)
        self._pen = QPen()
        self._pen.setStyle(Qt.SolidLine)
        self._pen.setWidth(2)
        self._pen.setColor(self.theme().accent_color if self.theme() else QColor(104, 104, 104, 255))
        self._selected_pen = QPen()
        self._selected_pen.setStyle(Qt.SolidLine)
        self._selected_pen.setWidth(3)
        self._selected_pen.setColor(self.theme().accent_color_4 if self.theme() else QColor(67, 255, 163, 255))

        super(CurveNodeItem, self).__init__(parent)

        self._lock_x_pos = False
        self._snap = False
        self._current_pos = None
        self._new_pos = None
        self._line = None
        self._is_point1 = False
        self.set_rect(rect if rect else QRect(0, 0, 10, 10))

        self.setFlags(
            QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemSendsScenePositionChanges)

    @property
    def snap(self):
        return self._snap

    @snap.setter
    def snap(self, flag):
        self._snap = bool(flag)

    @property
    def lock_x_pos(self):
        return self._lock_x_pos

    @lock_x_pos.setter
    def lock_x_pos(self, value):
        self._lock_x_pos = value

    def boundingRect(self):
        return QRectF(0, 0, 20, 20)

    def paint(self, painter, option, widget):
        painter.setBrush(self._brush)
        painter.setPen(self._selected_pen if self.isSelected() else self._pen)
        painter.drawEllipse(self._rect)

    def mousePressEvent(self, event):
        self._current_pos = self.pos()
        super(CurveNodeItem, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super(CurveNodeItem, self).mouseMoveEvent(event)
        curve_offset = -self.WIDTH * 0.5
        scale_x = min(max(event.scenePos().x(), curve_offset), self.scene().base_size + curve_offset)
        scale_y = min(max(event.scenePos().y(), curve_offset), self.scene().base_size + curve_offset)
        if self._lock_x_pos:
            scale_x = self._lock_x_pos
        if self._snap is not False:
            scale_x = round((float(scale_x) / self._snap)) * self._snap
            scale_y = round((float(scale_y) / self._snap)) * self._snap
        self._new_pos = QPointF(scale_x, scale_y)
        self.setPos(self._new_pos)
        self.scene().update_curve()
        self.signals.curveUpdated.emit()

    def mouseReleaseEvent(self, event):
        super(CurveNodeItem, self).mouseReleaseEvent(event)

        if not self._new_pos:
            return

        self.scene().undo_stack.push(CurveNodeMoveUndoCommand(self.scene(), self, self._current_pos, self._new_pos))
        self._new_pos = None

    def itemChange(self, change, value):
        if change == self.ItemPositionChange and self.scene():
            new_pos = value
            self._move_line_to_center(new_pos)

        return super(CurveNodeItem, self).itemChange(change, value)

    def set_rect(self, rect):
        self._rect = rect
        self.update()

    def add_line(self, line, is_point1):
        self._line = line
        self._is_point1 = is_point1
        self._move_line_to_center(self.pos())

    def _move_line_to_center(self, new_pos):
        if not self._line:
            return

        x_offset = self._rect.x() - self._rect.width() / 2
        y_offset = self._rect.y() - self._rect.height() / 2
        new_center_pos = QPointF(new_pos.x() - x_offset, new_pos.y() - y_offset)
        p1 = new_center_pos if self._is_point1 else self._line.line().p1()
        p2 = self._line.line().p2() if self._is_point1 else new_center_pos
        self._line.setLine(QLineF(p1, p2))


class CurveNodeScene(QGraphicsScene):

    curveUpdated = Signal()

    def __init__(self, base_rect):
        super(CurveNodeScene, self).__init__()

        self._undo_stack = QUndoStack()
        self._point_objects = list()
        self._control_points = list()
        self._bezier_curve = None
        self._base_size = 300
        self._base_rect = base_rect
        self._theme = None

        self._undo_action = self._undo_stack.createUndoAction(self)
        self._redo_action = self._undo_stack.createRedoAction(self)
        self._undo_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Z))
        self._redo_action.setShortcuts(
            (QKeySequence(Qt.CTRL + Qt.Key_Y),
             QKeySequence(Qt.SHIFT + Qt.Key_Z),
             QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_Z)))

        self.setSceneRect(self._base_rect)
        self._create_grid()
        self._create_grid(10, Qt.black, Qt.DotLine)
        self._create_controls()

    @property
    def bezier_curve(self):
        return self._bezier_curve

    @property
    def undo_stack(self):
        return self._undo_stack

    @property
    def undo_action(self):
        return self._undo_action

    @property
    def redo_action(self):
        return self._redo_action

    @property
    def base_size(self):
        return self._base_size

    @base_size.setter
    def base_size(self, value):
        self._base_size = value

    def keyPressEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        if type(event) == QKeyEvent:
            if modifiers != Qt.ControlModifier:
                return
            if event.key() == Qt.Key_Z:
                self._undo_action.trigger()
            elif event.key() == Qt.Key_Y:
                self._redo_action.trigger()

    def get_points(self):
        points = list()
        for obj in self._point_objects:
            point = QPointF(obj.pos().x() + 5, obj.pos().y() + 5)
            points.append(point)

        return points

    def set_points(self, points):
        self._point_objects = points

    def set_point_positions(self, positions):
        for i, point in enumerate(positions):
            self._point_objects[i].setPos(point - QPoint(5, 5))
        self.update_curve()

    def set_snap(self, value):
        for point in self._control_points:
            point.snap = value

    def update_curve(self):
        points = self.get_points()
        self._bezier_curve.update_path(points)

    def _create_grid(self, divider=4, color=Qt.darkGray, line=Qt.DashLine):
        pos = float(self._base_size) / divider
        for div in range(divider):
            if div == 0:
                continue
            line_item = QGraphicsLineItem(0, pos * div, self._base_size, pos * div)
            line_item.setZValue(-1)
            line_item.setPen(QPen(color, 1, line))
            self.addItem(line_item)

            line_item = QGraphicsLineItem(pos * div, 0, pos * div, self._base_size)
            line_item.setZValue(-1)
            line_item.setPen(QPen(color, 1, line))
            self.addItem(line_item)

        pen = QPen(Qt.black, 1, Qt.SolidLine)
        rect = QGraphicsRectItem(self._base_rect)
        rect.setZValue(-1)
        self.addItem(rect)

    def _create_controls(self):
        self._control_points = list()
        points = [
            QPoint(0, 0),
            QPoint(self._base_size / 4.0, 0),
            QPoint(self._base_size - (self._base_size / 4.0), self._base_size),
            QPoint(self._base_size, self._base_size)]
        for point in points:
            control_point = CurveNodeItem()
            self.addItem(control_point)
            control_point.setPos(point - QPoint(5, 5))
            self._control_points.append(control_point)
            self._point_objects.append(control_point)
            control_point.signals.curveUpdated.connect(self.curveUpdated.emit)

        self._control_points[0].lock_x_pos = -5.0
        self._control_points[-1].lock_x_pos = (self._base_size - 5.0)
        self._bezier_curve = BezierCurveItem()
        self._bezier_curve.update_path(points)
        self.addItem(self._bezier_curve)

        start_connector = self.addLine(
            QLineF(40, 40, 80, 80), QPen(Qt.white, 1, Qt.DashLine))
        start_connector.setZValue(-2)
        end_connector = self.addLine(
            QLineF(40, 40, 80, 80), QPen(Qt.white, 1, Qt.DashLine))
        end_connector.setZValue(-2)

        self._control_points[0].add_line(start_connector, is_point1=True)
        self._control_points[1].add_line(start_connector, is_point1=False)
        self._control_points[-1].add_line(end_connector, is_point1=False)
        self._control_points[-2].add_line(end_connector, is_point1=True)


class CurveNodeView(QGraphicsView, object):
    def __init__(self, parent=None):
        super(CurveNodeView, self).__init__(parent)

        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.HighQualityAntialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # self.setStyleSheet('background-color: rgb(60, 60, 60); border: 1px solid rgb(90, 70, 30);')


class CurveNodeMoveUndoCommand(QUndoCommand, object):
    def __init__(self, scene, node, old_position, new_position, description=None, parent=None):
        super(CurveNodeMoveUndoCommand, self).__init__(description or self.__class__.__name__[4:-7], parent)

        self._scene = scene
        self._node = node
        self._old_position = old_position
        self._new_position = new_position

    def redo(self):
        super(CurveNodeMoveUndoCommand, self).redo()
        self._node.setPos(self._new_position)
        self._scene.update_curve()

    def undo(self):
        super(CurveNodeMoveUndoCommand, self).undo()
        self._node.setPos(self._old_position)
        self._scene.update_curve()


class CurveNodeSwitchUndoCommand(QUndoCommand, object):
    def __init__(self, scene, old_positions, new_positions, description=None, parent=None):
        super(CurveNodeSwitchUndoCommand, self).__init__(description or self.__class__.__name__[4:-7], parent)

        self._scene = scene
        self._old_positions = old_positions
        self._new_positions = new_positions

    def redo(self):
        super(CurveNodeSwitchUndoCommand, self).redo()
        self._scene.set_point_positions(self._new_positions)

    def undo(self):
        super(CurveNodeSwitchUndoCommand, self).undo()
        self._scene.set_point_positions(self._old_positions)
