# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 10:59:53 2017

@author: Weber

"""
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QLocale, Qt, QDate, QDateTime, QTime, QByteArray
from pyqtgraph.widgets import ColorButton, SpinBox
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterItem
from pyqtgraph.parametertree.Parameter import registerParameterType

from pymodaq.daq_utils.daq_utils import scroll_log, scroll_linear
from collections import OrderedDict
from decimal import Decimal as D

from pymodaq.daq_utils.plotting.qled import QLED

from pathlib import Path
import numpy as np
import os


class GroupParameterItemCustom(pTypes.GroupParameterItem):
    """
        | Group parameters are used mainly as a generic parent item that holds (and groups!) a set of child parameters. It also provides a simple mechanism for displaying a button or combo that can be used to add new parameters to the group.
        |
        | This customization is made in order to respond to the visible options.
        | Overwrite the optsChanged method from GroupParameterItem class.

    """

    def __init__(self, param, depth):
        pTypes.GroupParameterItem.__init__(self, param, depth)

    def optsChanged(self, param, changed):
        if 'addList' in changed:
            self.updateAddList()
        elif 'visible' in changed:
            self.setHidden(not changed['visible'])


class GroupParameterCustom(pTypes.GroupParameter):
    """
        |
        | Group parameters are used mainly as a generic parent item that holds (and groups!) a set of child parameters.
        |
        | It also provides a simple mechanism for displaying a button or combo that can be used to add new parameters to the group.
        |
        | To enable this, the group  must be initialized with the 'addText' option (the text will be displayed on a button which, when clicked, will cause addNew() to be called).
        |
        | If the 'addList' option is specified as well, then a dropdown-list of addable items will be displayed instead of a button.
        |

        ============== ========================================
        **Attributes**    **Type**
        itemClass         instance of GroupParameterItemCustom
        ============== ========================================
    """
    itemClass = GroupParameterItemCustom


registerParameterType('group', GroupParameterCustom, override=True)


class SpinBoxCustom(SpinBox.SpinBox):
    def __init__(self, parent=None, value=0.0, **kwargs):
        super().__init__(parent, value, **kwargs)

    def setOpts(self, **opts):
        """
            Overriden class to add the field visible in the options.

            =============== =========== ======================
            **Parameters**    **Type**     **Description**
            *opts*            string       the vararg options
            =============== =========== ======================
        """
        # print opts
        for k in opts:
            if k == 'bounds' or k == 'limits':
                self.setMinimum(opts[k][0], update=False)
                self.setMaximum(opts[k][1], update=False)
            elif k == 'min':
                self.setMinimum(opts[k], update=False)
            elif k == 'max':
                self.setMaximum(opts[k], update=False)
            elif k in ['step', 'minStep']:
                self.opts[k] = D(str(opts[k]))
            elif k == 'value':
                pass  # # don't set value until bounds have been set
            elif k == 'visible':
                self.setVisible(opts[k])
            elif k == 'readonly':
                self.setReadOnly(opts[k])
            elif k == 'enabled':
                self.setEnabled(opts[k])
            elif k == 'format':
                self.opts[k] = opts[k]
            elif k in self.opts:
                self.opts[k] = opts[k]
            elif 'tip' in k:
                self.opts[k] = opts[k]
                self.setToolTip(opts[k])
        if 'value' in opts:
            self.setValue(opts['value'])

        # # If bounds have changed, update value to match
        if 'bounds' in opts and 'value' not in opts:
            self.setValue()

        # # sanity checks:
        if self.opts['int']:
            if 'step' in opts:
                step = opts['step']
                # # not necessary..
                # if int(step) != step:
                # raise Exception('Integer SpinBox must have integer step size.')
            else:
                self.opts['step'] = int(self.opts['step'])

            if 'minStep' in opts:
                step = opts['minStep']
                if int(step) != step:
                    raise Exception('Integer SpinBox must have integer minStep size.')
            else:
                ms = int(self.opts.get('minStep', 1))
                if ms < 1:
                    ms = 1
                self.opts['minStep'] = ms

        if 'delay' in opts:
            self.proxy.setDelay(opts['delay'])

        self.updateText()


class Pixmap_check(QtWidgets.QWidget):
    """ value of this parameter is a dict with checked, data for the pixmap and optionally path in h5 node
    """

    # valuechanged=pyqtSignal(dict)

    def __init__(self):
        QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))
        super(Pixmap_check, self).__init__()
        self.path = ""
        self.data = None
        self.initUI()

    def initUI(self):
        """
            Init the User Interface.
        """
        self.ver_layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel()
        self.checkbox = QtWidgets.QCheckBox('Show/Hide')
        self.checkbox.setChecked(False)
        self.ver_layout.addWidget(self.label)
        self.ver_layout.addWidget(self.checkbox)
        self.ver_layout.setSpacing(0)
        self.ver_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.ver_layout)

    def setValue(self, dic):
        if 'data' in dic:
            if not isinstance(dic['data'], QtGui.QPixmap):
                self.data = QByteArray(dic['data'])
                im = QtGui.QImage.fromData(self.data)
                a = QtGui.QPixmap.fromImage(im)
            else:
                a = dic['data']
        else:
            a = dic['pixmap']
        self.label.setPixmap(a)
        self.checkbox.setChecked(dic['checked'])
        self.path = dic['path']
        # self.valuechanged.emit(dic)

    def value(self):
        return dict(pixmap=self.label.pixmap(), checked=self.checkbox.isChecked(), path=self.path)


class QTimeCustom(QtWidgets.QTimeEdit):
    def __init__(self, *args, **kwargs):
        super(QTimeCustom, self).__init__(*args, **kwargs)
        self.minutes_increment = 1
        self.timeChanged.connect(self.updateTime)

    def setTime(self, time):
        hours = time.hour()
        minutes = time.minute()

        minutes = int(np.round(minutes / self.minutes_increment) * self.minutes_increment)
        if minutes == 60:
            minutes = 0
            hours += 1

        time.setHMS(hours, minutes, 0)

        return super(QTimeCustom, self).setTime(time)

    def setMinuteIncrement(self, minutes_increment):
        self.minutes_increment = minutes_increment
        self.updateTime(self.time())

    @pyqtSlot(QTime)
    def updateTime(self, time):
        self.setTime(time)


class SliderSpinBox(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))
        super().__init__()
        self.subtype = kwargs['subtype']
        self.initUI(*args, **kwargs)

        self.valueChanged = self.spinbox.valueChanged  # (value)  for compatibility with QSpinBox
        self.sigValueChanged = self.spinbox.sigValueChanged  # (self)
        self.sigValueChanging = self.spinbox.sigValueChanging  # (self, value)  sent immediately; no delay.

    @property
    def opts(self):
        return self.spinbox.opts

    @opts.setter
    def opts(self, **opts):
        self.setOpts(**opts)

    def setOpts(self, **opts):
        self.spinbox.setOpts(**opts)
        if 'visible' in opts:
            self.slider.setVisible(opts['visible'])

    def initUI(self, *args, **kwargs):
        """
            Init the User Interface.
        """
        self.hor_layout = QtWidgets.QVBoxLayout()
        self.slider = QtWidgets.QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)

        self.spinbox = SpinBoxCustom(parent=None, value=1, **kwargs)

        self.hor_layout.addWidget(self.slider)
        self.hor_layout.addWidget(self.spinbox)
        self.hor_layout.setSpacing(0)
        self.hor_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.hor_layout)

        self.slider.valueChanged.connect(self.update_spinbox)
        self.spinbox.valueChanged.connect(self.update_slide)

    def update_spinbox(self, val):
        """
        val is a percentage [0-100] used in order to set the spinbox value between its min and max
        """
        min_val = float(self.opts['bounds'][0])
        max_val = float(self.opts['bounds'][1])
        if self.subtype == 'log':
            val_out = scroll_log(val, min_val, max_val)
        else:
            val_out = scroll_linear(val, min_val, max_val)
        try:
            self.slider.valueChanged.disconnect(self.update_spinbox)
            self.spinbox.valueChanged.disconnect(self.update_slide)
        except Exception:
            pass
        self.spinbox.setValue(val_out)

        self.slider.valueChanged.connect(self.update_spinbox)
        self.spinbox.valueChanged.connect(self.update_slide)

    def update_slide(self, val):
        """
        val is the spinbox value between its min and max
        """
        min_val = float(self.opts['bounds'][0])
        max_val = float(self.opts['bounds'][1])

        try:
            self.slider.valueChanged.disconnect(self.update_spinbox)
            self.spinbox.valueChanged.disconnect(self.update_slide)
        except Exception:
            pass
        self.slider.setValue(int((val - min_val) / (max_val - min_val) * 100))
        self.slider.valueChanged.connect(self.update_spinbox)
        self.spinbox.valueChanged.connect(self.update_slide)

    def setValue(self, val):
        self.spinbox.setValue(val)

    def value(self):
        return self.spinbox.value()


class WidgetParameterItemcustom(pTypes.WidgetParameterItem):
    """
        This is a subclass of widget parameteritem in order to deal with the visiblily of the spinbox when parameter visibility os toggled.
    """

    def __init__(self, param, depth):
        pTypes.WidgetParameterItem.__init__(self, param, depth)

        if 'enabled' in self.param.opts:
            self.displayLabel.setEnabled(self.param.opts['enabled'])

    def makeWidget(self):
        """
            | Return a single widget that should be placed in the second tree column.
            | The widget must be given three attributes:

            ==========  ============================================================
            sigChanged  a signal that is emitted when the widget's value is changed
            value       a function that returns the value
            setValue    a function that sets the value
            ==========  ============================================================

            | This is a good function to override in subclasses.

        """
        opts = self.param.opts
        t = opts['type']
        if t in ('int', 'float', 'slide'):
            defs = {
                'value': 0, 'min': None, 'max': None,
                'step': 1.0, 'dec': False,
                'siPrefix': False, 'suffix': '', 'decimals': 12,
            }
            if t == 'int':
                defs['int'] = True
                defs['minStep'] = 1.0
            for k in defs:
                if k in opts:
                    defs[k] = opts[k]
            if 'limits' in opts:
                defs['bounds'] = opts['limits']
            if t in ('int', 'float'):
                w = SpinBoxCustom()
            else:
                if 'subtype' not in opts:
                    opts['subtype'] = 'linear'
                if 'limits' not in opts:
                    defs['bounds'] = (0., 10.)
                w = SliderSpinBox(subtype=opts['subtype'])

            w.setOpts(**defs)
            w.sigChanged = w.sigValueChanged
            w.sigChanging = w.sigValueChanging

        elif t == 'bool':
            w = QtWidgets.QCheckBox()
            w.sigChanged = w.toggled
            w.value = w.isChecked
            w.setValue = w.setChecked
            w.setEnabled(not opts.get('readonly', False))
            self.hideWidget = False
        elif t == 'bool_push':
            w = QtWidgets.QPushButton()
            if 'label' in opts:
                w.setText(opts['label'])
            elif 'title' in opts:
                w.setText(opts['title'])
            else:
                w.setText(opts['name'])
            # w.setMaximumWidth(50)
            w.setCheckable(True)
            w.sigChanged = w.toggled
            w.value = w.isChecked
            w.setValue = w.setChecked
            w.setEnabled(not opts.get('readonly', False))
            self.hideWidget = False
        elif t == 'led_push':
            w = QLED()
            w.clickable = True
            w.set_as_false()
            w.sigChanged = w.value_changed
            w.value = w.get_state
            w.setValue = w.set_as
            self.hideWidget = False
        elif t == 'str':
            w = QtWidgets.QLineEdit()
            w.sigChanged = w.editingFinished
            w.value = lambda: str(w.text())
            w.setValue = lambda v: w.setText(str(v))
            w.sigChanging = w.textChanged
        elif t == 'color':
            w = ColorButton.ColorButton()
            w.sigChanged = w.sigColorChanged
            w.sigChanging = w.sigColorChanging
            w.value = w.color
            w.setValue = w.setColor
            self.hideWidget = False
            w.setFlat(True)
            w.setEnabled(not opts.get('readonly', False))
        elif t == 'colormap':
            from pyqtgraph.widgets.GradientWidget import GradientWidget  # # need this here to avoid import loop
            w = GradientWidget(orientation='bottom')
            w.sigChanged = w.sigGradientChangeFinished
            w.sigChanging = w.sigGradientChanged
            w.value = w.colorMap
            w.setValue = w.setColorMap
            self.hideWidget = False
        elif t == 'date_time':
            w = QtWidgets.QDateTimeEdit(QDateTime(QDate.currentDate(), QTime.currentTime()))
            w.setCalendarPopup(True)
            if 'format' in opts:
                w.setDisplayFormat(opts['format'])
            else:
                w.setDisplayFormat('dd/MM/yyyy hh:mm')
            w.sigChanged = w.dateTimeChanged
            w.value = w.dateTime
            w.setValue = w.setDateTime
        elif t == 'date':
            w = QtWidgets.QDateEdit(QDate(QDate.currentDate()))
            w.setCalendarPopup(True)
            if 'format' in opts:
                w.setDisplayFormat(opts['format'])
            else:
                w.setDisplayFormat('dd/MM/yyyy')
            w.sigChanged = w.dateChanged
            w.value = w.date
            w.setValue = w.setDate

        elif t == 'time':
            w = QTimeCustom(QTime(QTime.currentTime()))
            if 'minutes_increment' in opts:
                w.setMinuteIncrement(opts['minutes_increment'])
            w.setDisplayFormat('hh:mm')
            w.sigChanged = w.timeChanged
            w.value = w.time
            w.setValue = w.setTime

        elif t == 'led':
            w = QLED()
            w.clickable = False
            w.set_as_false()
            w.sigChanged = w.value_changed
            w.value = w.get_state
            w.setValue = w.set_as
        elif t == 'pixmap':
            w = QtWidgets.QLabel()
            w.sigChanged = None
            w.value = w.pixmap
            w.setValue = w.setPixmap
        elif t == 'pixmap_check':
            w = Pixmap_check()
            w.sigChanged = w.checkbox.toggled
            w.value = w.value
            w.setValue = w.setValue
        else:
            raise Exception("Unknown type '%s'" % str(t))
        return w

    def limitsChanged(self, param, limits):
        """Called when the parameter's limits have changed"""
        ParameterItem.limitsChanged(self, param, limits)

        t = self.param.opts['type']
        if t == 'int' or t == 'float' or t == 'slide':
            self.widget.setOpts(bounds=limits)
        else:
            return  # don't know what to do with any other types..

    def showEditor(self):
        """
            Show the widget attribute.
        """
        self.widget.show()
        self.displayLabel.hide()
        self.widget.setFocus(Qt.OtherFocusReason)
        if isinstance(self.widget, SpinBox.SpinBox):
            self.widget.selectNumber()  # select the numerical portion of the text for quick editing

    def hideEditor(self):
        """
            Hide the widget attribute.
        """
        status = 'led' in self.param.opts['type'] or self.param.opts['type'] == 'pixmap'
        status = not (status or self.param.opts['type'] == 'pixmap_check')
        if status:
            self.widget.hide()
            self.displayLabel.show()

    def optsChanged(self, param, opts):
        """
            | Called when any options are changed that are not name, value, default, or limits.
            |
            | If widget is a SpinBox, pass options straight through.
            | So that only the display label is shown when visible option is toggled.

            =============== ================================== ==============================
            **Parameters**    **Type**                           **Description**
            *param*           instance of pyqtgraph parameter    the parameter to check
            *opts*            string list                        the associated options list
            =============== ================================== ==============================

            See Also
            --------
            optsChanged
        """
        # print "opts changed:", opts
        ParameterItem.optsChanged(self, param, opts)

        if 'readonly' in opts:
            self.updateDefaultBtn()
            if isinstance(self.widget, (QtWidgets.QCheckBox, ColorButton.ColorButton)):
                self.widget.setEnabled(not opts['readonly'])

        if 'minutes_increment' in opts:
            self.widget.setMinuteIncrement(opts['minutes_increment'])

        if 'tip' in opts:
            self.displayLabel.setToolTip(opts['tip'])

        # # If widget is a SpinBox, pass options straight through
        if isinstance(self.widget, SpinBoxCustom) or isinstance(self.widget, SliderSpinBox):
            if 'visible' in opts:
                opts.pop('visible')
                self.widget.hide()  # so that only the display label is shown when visible option is toggled
            if 'units' in opts and 'suffix' not in opts:
                opts['suffix'] = opts['units']
            self.widget.setOpts(**opts)
            self.updateDisplayLabel()

        if 'title' in opts:
            self.setText(0, opts['title'])  # void QTreeWidgetItem::setText(int column, const QString &text)

    def valueChanged(self, param, val, force=False):
        # # called when the parameter's value has changed
        ParameterItem.valueChanged(self, param, val)
        if self.widget.sigChanged is not None:
            self.widget.sigChanged.disconnect(self.widgetValueChanged)

        try:
            if force or val != self.widget.value():
                self.widget.setValue(val)
            self.updateDisplayLabel(val)  # # always make sure label is updated, even if values match!
        finally:
            if self.widget.sigChanged is not None:
                self.widget.sigChanged.connect(self.widgetValueChanged)
        self.updateDefaultBtn()


class SimpleParameterCustom(pTypes.SimpleParameter):
    itemClass = WidgetParameterItemcustom

    def __init__(self, *args, **kargs):
        pTypes.SimpleParameter.__init__(self, *args, **kargs)

    def _interpretValue(self, v):
        fn = {
            'int': int,
            'float': float,
            'bool': bool,
            'bool_push': bool,
            'str': str,
            'color': self._interpColor,
            'colormap': self._interpColormap,
            'date_time': QDateTime,
            'date': QDate,
            'time': QTime,
            'led': bool,
            'pixmap': QtWidgets.QLabel,
            'pixmap_check': Pixmap_check,
            'slide': float
        }[self.opts['type']]
        return fn(v)

    def setLimits(self, limits):
        """Set limits on the acceptable values for this parameter.
        The format of limits depends on the type of the parameter and
        some parameters do not make use of limits at all."""
        if 'limits' in self.opts and self.opts['limits'] == limits:
            return
        self.opts['limits'] = limits
        self.sigLimitsChanged.emit(self, limits)
        if self.opts['type'] in ['int', 'float', 'slide']:
            if self.value() > limits[1]:
                self.setValue(limits[1])
            elif self.value() < limits[0]:
                self.setValue(limits[0])
        return limits


registerParameterType('int', SimpleParameterCustom, override=True)
registerParameterType('float', SimpleParameterCustom, override=True)
registerParameterType('bool', SimpleParameterCustom, override=True)
registerParameterType('bool_push', SimpleParameterCustom, override=True)
registerParameterType('led_push', SimpleParameterCustom, override=True)
registerParameterType('date_time', SimpleParameterCustom, override=True)
registerParameterType('date', SimpleParameterCustom, override=True)
registerParameterType('time', SimpleParameterCustom, override=True)
registerParameterType('led', SimpleParameterCustom, override=True)
registerParameterType('pixmap', SimpleParameterCustom, override=True)
registerParameterType('pixmap_check', SimpleParameterCustom, override=True)
registerParameterType('slide', SimpleParameterCustom, override=True)


# registerParameterType('slide', SimpleParameterCustom , override=True)

class ListParameterItem_custom(pTypes.ListParameterItem):
    """
        WidgetParameterItem subclass providing comboBox that lets the user select from a list of options.

    """

    def __init__(self, param, depth):
        super(ListParameterItem_custom, self).__init__(param, depth)
        if 'tip' in param.opts:
            self.displayLabel.setToolTip(param.opts['tip'])

    def makeWidget(self):
        """
            Make a widget from self parameter options, connected to the buttonClicked function.

            Returns
            -------
            w:widget
                the initialized widget

            See Also
            --------
            buttonClicked, limitsChanged,
        """
        opts = self.param.opts
        t = opts['type']
        w = Combo_pb()
        w.add_pb.clicked.connect(self.buttonClicked)
        w.setMaximumHeight(20)  # # set to match height of spin box and line edit
        if 'show_pb' in opts:
            w.add_pb.setVisible(opts['show_pb'])
        else:
            w.add_pb.setVisible(False)
        if 'tip' in opts:
            w.setToolTip(opts['tip'])
        w.sigChanged = w.combo.currentIndexChanged
        w.value = self.value
        w.setValue = self.setValue
        self.widget = w  # # needs to be set before limits are changed
        self.limitsChanged(self.param, self.param.opts['limits'])
        if len(self.forward) > 0:
            self.setValue(self.param.value())
        return w

    def value(self):
        key = str(self.widget.combo.currentText())
        return self.forward.get(key, None)

    def setValue(self, val):
        self.targetValue = val
        if val not in self.reverse[0]:
            self.widget.combo.setCurrentIndex(0)
        else:
            key = self.reverse[1][self.reverse[0].index(val)]
            ind = self.widget.combo.findText(key)
            self.widget.combo.setCurrentIndex(ind)

    def limitsChanged(self, param, limits):
        """
            Set up forward / reverse mappings for {name:value} limits dictionnary.

            =============== ================================== ========================================
            **Parameters**    **Type**                          **Description**
            *param*           instance of pyqtgraph parameter    Not used
            *limits*          dictionnary                        the limits dictionnary to be mapped
            =============== ================================== ========================================

        """

        if len(limits) == 0:
            limits = ['']  # # Can never have an empty list--there is always at least a singhe blank item.

        self.forward, self.reverse = ListParameter_custom.mapping(limits)
        try:
            self.widget.blockSignals(True)
            val = self.targetValue  # asUnicode(self.widget.currentText())

            self.widget.combo.clear()
            for k in self.forward:
                self.widget.combo.addItem(k)
                if k == val:
                    self.widget.combo.setCurrentIndex(self.widget.count() - 1)
                    self.updateDisplayLabel()
        finally:
            self.widget.blockSignals(False)

    def buttonClicked(self):
        """
            |
            | Append the self limits attributes an added parameter with string value.
            | Update parameter and call the limitschanged method to map the added parameter.

            See Also
            --------
            limitsChanged,
        """
        if type(self.param.opts['limits']) == list:
            text, ok = QtWidgets.QInputDialog.getText(None, "Enter a value to add to the parameter",
                                                      "String value:", QtWidgets.QLineEdit.Normal)
            if ok and not (text == ""):
                self.param.opts['limits'].append(text)
                self.limitsChanged(self.param, self.param.opts['limits'])
                self.param.setValue(text)

    def optsChanged(self, param, opts):
        """
            Called when any options are changed that are not name, value, default, or limits.

            =============== ================================== =======================================
            **Parameters**    **Type**                           **Description**
            *param*           instance of pyqtgraph parameter    The parameter to be checked
            *opts*            string list                        The option dictionnary to be checked
            =============== ================================== =======================================

            See Also
            --------
            optsChanged
        """
        # print "opts changed:", opts
        ParameterItem.optsChanged(self, param, opts)

        if 'show_pb' in opts:
            self.widget.add_pb.setVisible(opts['show_pb'])
        if 'enabled' in opts:
            self.widget.setEnabled(opts['enabled'])


class ListParameter_custom(pTypes.ListParameter):
    """
        =============== =======================================
        **Attributes**    **Type**
        *itemClass*       instance of ListParameterItem_custom
        *sigActivated*    instance of pyqt Signal
        =============== =======================================
    """
    itemClass = ListParameterItem_custom
    sigActivated = pyqtSignal(object)

    def __init__(self, **opts):
        super(ListParameter_custom, self).__init__(**opts)

    def activate(self):
        """
            Emit the Activated signal.
        """
        self.sigActivated.emit(self)
        self.emitStateChanged('activated', None)


registerParameterType('list', ListParameter_custom, override=True)


class Combo_pb(QtWidgets.QWidget):

    def __init__(self, items=[]):
        QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))
        super(Combo_pb, self).__init__()
        self.items = items
        self.initUI()
        self.count = self.combo.count

    def initUI(self):
        """
            Init the User Interface.
        """
        self.hor_layout = QtWidgets.QHBoxLayout()
        self.combo = QtWidgets.QComboBox()
        self.combo.addItems(self.items)
        self.add_pb = QtWidgets.QPushButton()
        self.add_pb.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/Add2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_pb.setIcon(icon3)
        self.hor_layout.addWidget(self.combo)
        self.hor_layout.addWidget(self.add_pb)
        self.hor_layout.setSpacing(0)
        self.hor_layout.setContentsMargins(0, 0, 0, 0)
        self.add_pb.setMaximumWidth(25)
        self.setLayout(self.hor_layout)


class TableParameterItem(WidgetParameterItemcustom):

    def __init__(self, param, depth):
        pTypes.WidgetParameterItem.__init__(self, param, depth)
        self.hideWidget = False
        self.subItem = QtGui.QTreeWidgetItem()
        self.addChild(self.subItem)

    def treeWidgetChanged(self):
        """
            Check for changement in the Widget tree.
        """
        # # TODO: fix so that superclass method can be called
        # # (WidgetParameter should just natively support this style)
        # WidgetParameterItem.treeWidgetChanged(self)
        self.treeWidget().setFirstItemColumnSpanned(self.subItem, True)
        self.treeWidget().setItemWidget(self.subItem, 0, self.widget)

        # for now, these are copied from ParameterItem.treeWidgetChanged
        self.setHidden(not self.param.opts.get('visible', True))
        self.setExpanded(self.param.opts.get('expanded', True))

    def makeWidget(self):
        """
            Make and initialize an instance of Table_custom.

            Returns
            -------
            table : instance of Table_custom.
                The initialized table.

            See Also
            --------
            Table_custom
        """
        opts = self.param.opts
        w = Table_custom()
        if 'tip' in opts:
            w.setToolTip(opts['tip'])
        w.setColumnCount(2)
        if 'header' in opts:
            w.setHorizontalHeaderLabels(self.param.opts['header'])
        if 'height' not in opts:
            opts['height'] = 200
        w.setMaximumHeight(opts['height'])
        # self.table.setReadOnly(self.param.opts.get('readonly', False))
        w.value = w.get_table_value
        w.setValue = w.set_table_value
        w.sigChanged = w.itemChanged
        return w


class Table_custom(QtWidgets.QTableWidget):
    """
        ============== ===========================
        *Attributes**    **Type**
        *valuechanged*   instance of pyqt Signal
        *QtWidgets*      instance of QTableWidget
        ============== ===========================
    """

    valuechanged = pyqtSignal(OrderedDict)

    def __init__(self):
        QtWidgets.QTableWidget.__init__(self)

    def get_table_value(self):
        """
            Get the contents of the self coursed table.

            Returns
            -------
            data : ordered dictionnary
                The getted values dictionnary.
        """
        data = OrderedDict([])
        for ind in range(self.rowCount()):
            item0 = self.item(ind, 0)
            item1 = self.item(ind, 1)
            if item0 is not None and item1 is not None:
                try:
                    data[item0.text()] = float(item1.text())
                except Exception:
                    data[item0.text()] = item1.text()
        return data

    def set_table_value(self, data_dict):
        """
            Set the data values dictionnary to the custom table.

            =============== ====================== ================================================
            **Parameters**    **Type**               **Description**
            *data_dict*       ordered dictionnary    the contents to be stored in the custom table
            =============== ====================== ================================================
        """
        try:
            self.setRowCount(len(data_dict))
            self.setColumnCount(2)
            for ind, (key, value) in enumerate(data_dict.items()):
                item0 = QtWidgets.QTableWidgetItem(key)
                item0.setFlags(item0.flags() ^ Qt.ItemIsEditable)
                if isinstance(value, float):
                    item1 = QtWidgets.QTableWidgetItem('{:.6e}'.format(value))
                else:
                    item1 = QtWidgets.QTableWidgetItem(str(value))
                item1.setFlags(item1.flags() ^ Qt.ItemIsEditable)
                self.setItem(ind, 0, item0)
                self.setItem(ind, 1, item1)
            # self.valuechanged.emit(data_dict)

        except Exception as e:
            pass


class TableParameter(Parameter):
    """
        =============== =================================
        **Attributes**    **Type**
        *itemClass*       instance of TableParameterItem
        *Parameter*       instance of pyqtgraph parameter
        =============== =================================
    """
    itemClass = TableParameterItem
    """Editable string; displayed as large text box in the tree."""

    # def __init(self):
    #     super(TableParameter,self).__init__()

    def setValue(self, value):
        self.opts['value'] = value
        self.sigValueChanged.emit(self, value)


registerParameterType('table', TableParameter, override=True)


class TableViewParameterItem(WidgetParameterItemcustom):
    def __init__(self, param, depth):
        pTypes.WidgetParameterItem.__init__(self, param, depth)
        self.hideWidget = False
        self.subItem = QtGui.QTreeWidgetItem()
        self.addChild(self.subItem)

    def treeWidgetChanged(self):
        """
            Check for changement in the Widget tree.
        """
        self.treeWidget().setFirstItemColumnSpanned(self.subItem, True)
        self.treeWidget().setItemWidget(self.subItem, 0, self.widget)

        # for now, these are copied from ParameterItem.treeWidgetChanged
        self.setHidden(not self.param.opts.get('visible', True))
        self.setExpanded(self.param.opts.get('expanded', True))

    def makeWidget(self):
        """
            Make and initialize an instance of Table_custom.

            Returns
            -------
            table : instance of Table_custom.
                The initialized table.

            See Also
            --------
            Table_custom
        """
        menu = False
        opts = self.param.opts
        if 'menu' in opts:
            menu = opts['menu']
        w = TableViewCustom(menu=menu)

        if 'tip' in opts:
            w.setToolTip(opts['tip'])

        w.setMaximumHeight(200)
        # self.table.setReadOnly(self.param.opts.get('readonly', False))
        w.value = w.get_table_value
        w.setValue = w.set_table_value
        w.sigChanged = w.valueChanged
        return w

    def optsChanged(self, param, opts):
        """
            | Called when any options are changed that are not name, value, default, or limits.
            |
            | If widget is a SpinBox, pass options straight through.
            | So that only the display label is shown when visible option is toggled.

            =============== ================================== ==============================
            **Parameters**    **Type**                           **Description**
            *param*           instance of pyqtgraph parameter    the parameter to check
            *opts*            string list                        the associated options list
            =============== ================================== ==============================

            See Also
            --------
            optsChanged
        """
        # print "opts changed:", opts
        ParameterItem.optsChanged(self, param, opts)

        if 'readonly' in opts:
            self.updateDefaultBtn()
            if isinstance(self.widget, (QtWidgets.QCheckBox, ColorButton.ColorButton)):
                self.widget.setEnabled(not opts['readonly'])

        if 'delegate' in opts:
            styledItemDelegate = QtWidgets.QStyledItemDelegate()
            styledItemDelegate.setItemEditorFactory(opts['delegate']())
            self.widget.setItemDelegate(styledItemDelegate)

        if 'menu' in opts:
            self.widget.setmenu(opts['menu'])


class TableViewCustom(QtWidgets.QTableView):
    """
        ============== ===========================
        *Attributes**    **Type**
        *valuechanged*   instance of pyqt Signal
        *QtWidgets*      instance of QTableWidget
        ============== ===========================
    """

    valueChanged = pyqtSignal(list)
    add_data_signal = pyqtSignal(int)
    remove_row_signal = pyqtSignal(int)
    load_data_signal = pyqtSignal()
    save_data_signal = pyqtSignal()

    def __init__(self, menu=False):
        super().__init__()
        self.setmenu(menu)

    def setmenu(self, status):
        if status:
            self.menu = QtWidgets.QMenu()
            self.menu.addAction('Add new', self.add)
            self.menu.addAction('Remove selected row', self.remove)
            self.menu.addAction('Clear all', self.clear)
            self.menu.addSeparator()
            self.menu.addAction('Load as txt', lambda: self.load_data_signal.emit())
            self.menu.addAction('Save as txt', lambda: self.save_data_signal.emit())
        else:
            self.menu = None

    def clear(self):
        self.model().clear()

    def add(self):
        self.add_data_signal.emit(self.currentIndex().row())

    def remove(self):
        self.remove_row_signal.emit(self.currentIndex().row())

    def data_has_changed(self, topleft, bottomright, roles):
        self.valueChanged.emit([topleft, bottomright, roles])

    def get_table_value(self):
        """

        """
        return self.model()

    def set_table_value(self, data_model):
        """

        """
        try:
            self.setModel(data_model)
            self.model().dataChanged.connect(self.data_has_changed)
        except Exception as e:
            pass

    def contextMenuEvent(self, event):
        if self.menu is not None:
            self.menu.exec(event.globalPos())


class TableViewParameter(Parameter):
    """
        =============== =================================
        **Attributes**    **Type**
        *itemClass*       instance of TableParameterItem
        *Parameter*       instance of pyqtgraph parameter
        =============== =================================
    """
    itemClass = TableViewParameterItem

    def setValue(self, value):
        self.opts['value'] = value
        self.sigValueChanged.emit(self, value)


registerParameterType('table_view', TableViewParameter, override=True)


class ItemSelectParameterItem(WidgetParameterItemcustom):

    def __init__(self, param, depth):
        pTypes.WidgetParameterItem.__init__(self, param, depth)
        self.hideWidget = False
        self.subItem = QtWidgets.QTreeWidgetItem()
        self.addChild(self.subItem)

    def treeWidgetChanged(self):
        """

        """
        # # TODO: fix so that superclass method can be called
        # # (WidgetParameter should just natively support this style)
        # WidgetParameterItem.treeWidgetChanged(self)
        self.treeWidget().setFirstItemColumnSpanned(self.subItem, True)
        self.treeWidget().setItemWidget(self.subItem, 0, self.widget)

        # for now, these are copied from ParameterItem.treeWidgetChanged
        self.setHidden(not self.param.opts.get('visible', True))
        self.setExpanded(self.param.opts.get('expanded', True))

    def makeWidget(self):
        """
            | Make and initialize an instance of ItemSelect_pb with itemselect value.
            | Connect the created object with the buttonClicked function.

        """
        opts = self.param.opts
        w = ItemSelect_pb()
        w.itemselect.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        if 'height' in opts:
            w.itemselect.setMaximumHeight(opts['height'])
        else:
            w.itemselect.setMaximumHeight(70)
        # w.setReadOnly(self.param.opts.get('readonly', False))
        if 'show_pb' in opts:
            w.add_pb.setVisible(opts['show_pb'])
        else:
            w.add_pb.setVisible(False)
        if 'tip' in opts:
            w.setToolTip(opts['tip'])
        w.value = w.itemselect.get_value
        w.setValue = w.itemselect.set_value
        w.sigChanged = w.itemselect.itemSelectionChanged
        w.add_pb.clicked.connect(self.buttonClicked)
        return w

    def buttonClicked(self):
        """
           Append to the param attribute the dictionnary obtained from the QtWidget add parameter procedure.
        """

        text, ok = QtWidgets.QInputDialog.getText(None, "Enter a value to add to the parameter",
                                                  "String value:", QtWidgets.QLineEdit.Normal)
        if ok and not (text == ""):
            all = self.param.value()['all_items']
            all.append(text)
            sel = self.param.value()['selected']
            sel.append(text)
            val = dict(all_items=all, selected=sel)
            self.param.setValue(val)
            self.param.sigValueChanged.emit(self.param, val)

    def optsChanged(self, param, opts):
        """
            Called when any options are changed that are not name, value, default, or limits.

            See Also
            --------
            optsChanged
        """
        # print "opts changed:", opts
        ParameterItem.optsChanged(self, param, opts)

        if 'show_pb' in opts:
            self.widget.add_pb.setVisible(opts['show_pb'])


class ItemSelect_pb(QtWidgets.QWidget):
    def __init__(self):
        QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))
        super(ItemSelect_pb, self).__init__()
        self.initUI()

    def initUI(self):
        self.hor_layout = QtWidgets.QHBoxLayout()
        self.itemselect = ItemSelect()
        self.add_pb = QtWidgets.QPushButton()
        self.add_pb.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/Add2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_pb.setIcon(icon3)
        self.hor_layout.addWidget(self.itemselect)
        self.hor_layout.addWidget(self.add_pb)
        self.hor_layout.setSpacing(0)

        self.setLayout(self.hor_layout)


class ItemSelect(QtWidgets.QListWidget):
    def __init__(self):
        QtWidgets.QListWidget.__init__(self)

    def get_value(self):
        """
            Get the dictionnary of values contained in the QtWidget attribute.

            Returns
            -------
            dictionnary
                The dictionnary of all_items compared to the slelectedItems.
        """
        selitems = [item.text() for item in self.selectedItems()]
        allitems = [item.text() for item in self.all_items()]
        return dict(all_items=allitems, selected=selitems)

    def all_items(self):
        """
            Get the all_items list from the self QtWidget attribute.

            Returns
            -------
            list
                The item list.
        """
        return [self.item(ind) for ind in range(self.count())]

    def set_value(self, values):
        """
            Set values to the all_items attributes filtering values by the 'selected' key.

            =============== ============== =======================================
            **Parameters**    **Type**       **Description**
            *values*          dictionnary    the values dictionnary to be setted.
            =============== ============== =======================================
        """
        allitems = [item.text() for item in self.all_items()]
        if allitems != values['all_items']:
            self.clear()
            self.addItems(values['all_items'])
            QtWidgets.QApplication.processEvents()
        for item in self.all_items():
            if item.text() in values['selected']:
                item.setSelected(True)


class ItemSelectParameter(Parameter):
    """
        Editable string; displayed as large text box in the tree.

        =============== ======================================
        **Attributes**    **Type**
        *itemClass*       instance of ItemSelectParameterItem
        *sigActivated*    instance of pyqt Signal
        =============== ======================================
    """
    itemClass = ItemSelectParameterItem
    sigActivated = pyqtSignal(object)

    def activate(self):
        """
            Activate the "Activated" signal attribute0
        """
        self.sigActivated.emit(self)
        self.emitStateChanged('activated', None)


registerParameterType('itemselect', ItemSelectParameter, override=True)


class ActionParameterItem(pTypes.ActionParameterItem):
    def __init__(self, param, depth):
        super().__init__(param, depth)

        if 'title' in param.opts:
            name = param.opts['title']
        else:
            name = param.name()
        self.button.setText(name)


class ActionParameter(pTypes.ActionParameter):
    """Used for displaying a button within the tree."""
    itemClass = ActionParameterItem


registerParameterType('action', ActionParameter, override=True)


class file_browserParameterItem(WidgetParameterItemcustom):

    def __init__(self, param, depth):
        self.filetype = False
        super().__init__(param, depth)
        self.hideWidget = False
        self.subItem = QtWidgets.QTreeWidgetItem()
        self.addChild(self.subItem)

    def treeWidgetChanged(self):
        # # TODO: fix so that superclass method can be called
        # # (WidgetParameter should just natively support this style)
        # WidgetParameterItem.treeWidgetChanged(self)
        self.treeWidget().setFirstItemColumnSpanned(self.subItem, True)
        self.treeWidget().setItemWidget(self.subItem, 0, self.w)

        # for now, these are copied from ParameterItem.treeWidgetChanged
        self.setHidden(not self.param.opts.get('visible', True))
        self.setExpanded(self.param.opts.get('expanded', True))

    def makeWidget(self):
        """
            Make an initialized file_browser object with parameter options dictionnary ('readonly' key)0

            Returns
            -------
            w : filebrowser
                The initialized file browser.

            See Also
            --------
            file_browser
        """
        if 'filetype' in self.param.opts:
            self.filetype = self.param.opts['filetype']
        else:
            self.filetype = True

        self.w = file_browser(self.param.value(), file_type=self.filetype)
        if 'tip' in self.param.opts:
            self.w.setToolTip(self.param.opts['tip'])
        # self.file_browser.setMaximumHeight(100)
        self.w.base_path_edit.setReadOnly(self.param.opts['readonly'])
        self.w.value = self.w.get_value
        self.w.setValue = self.w.set_path
        self.w.sigChanged = self.w.value_changed
        return self.w


class file_browser(QtWidgets.QWidget):
    """
        ================ =========================
        **Attributes**    **Type**
        *value_changed*   instance of pyqt Signal
        *path*            string
        ================ =========================

        See Also
        --------
        browse_path
    """
    value_changed = pyqtSignal(str)

    def __init__(self, init_path='D:/Data', file_type=False):
        QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))
        super(file_browser, self).__init__()
        self.filetype = file_type
        self.path = init_path
        self.initUI()

        self.base_path_browse_pb.clicked.connect(self.browse_path)

    def browse_path(self):
        """
            Browse the path attribute if exist.

            See Also
            --------
            set_path
        """
        if self.filetype is True:
            folder_name = QtWidgets.QFileDialog.getOpenFileName(None, 'Choose File', os.path.split(self.path)[0])[0]
        elif self.filetype is False:
            folder_name = QtWidgets.QFileDialog.getExistingDirectory(None, 'Choose Folder', self.path)

        elif self.filetype == "save":
            folder_name = QtWidgets.QFileDialog.getSaveFileName(None, 'Enter a Filename', os.path.split(self.path)[0])[
                0]

        if not (not (folder_name)):  # execute if the user didn't cancel the file selection
            self.set_path(folder_name)
            self.value_changed.emit(folder_name)

    def set_path(self, path_file):
        """
            Set the base path attribute with the given path_file.

            =============== =========== ===========================
            **Parameters**    **Type**    **Description**
            *path_file*       string      the pathname of the file
            =============== =========== ===========================
        """
        if isinstance(path_file, Path):
            path_file = str(path_file)
        self.base_path_edit.setPlainText(path_file)
        self.path = path_file

    def get_value(self):
        """
            Get the value of the base_path_edit attribute.

            Returns
            -------
            string
                the path name
        """
        return self.base_path_edit.toPlainText()

    def initUI(self):
        """
            Init the User Interface.
        """

        self.hor_layout = QtWidgets.QHBoxLayout()
        self.base_path_edit = QtWidgets.QPlainTextEdit(self.path)
        self.base_path_edit.setMaximumHeight(50)
        self.base_path_browse_pb = QtWidgets.QPushButton()
        self.base_path_browse_pb.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/Browse_Dir_Path.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.base_path_browse_pb.setIcon(icon3)
        self.hor_layout.addWidget(self.base_path_edit)

        verlayout = QtWidgets.QVBoxLayout()
        verlayout.addWidget(self.base_path_browse_pb)
        verlayout.addStretch()
        self.hor_layout.addLayout(verlayout)
        self.hor_layout.setSpacing(0)
        self.setLayout(self.hor_layout)


class file_browserParameter(Parameter):
    """
        Editable string; displayed as large text box in the tree.
        See Also
        --------
        file_browserParameterItem
    """
    itemClass = file_browserParameterItem


registerParameterType('browsepath', file_browserParameter, override=True)


class Plain_text_pbParameterItem(pTypes.WidgetParameterItem):

    def __init__(self, param, depth):
        pTypes.WidgetParameterItem.__init__(self, param, depth)
        self.hideWidget = False
        self.subItem = QtWidgets.QTreeWidgetItem()
        self.addChild(self.subItem)

    def treeWidgetChanged(self):
        # # TODO: fix so that superclass method can be called
        # # (WidgetParameter should just natively support this style)
        # WidgetParameterItem.treeWidgetChanged(self)
        self.treeWidget().setFirstItemColumnSpanned(self.subItem, True)
        self.treeWidget().setItemWidget(self.subItem, 0, self.w)

        # for now, these are copied from ParameterItem.treeWidgetChanged
        self.setHidden(not self.param.opts.get('visible', True))
        self.setExpanded(self.param.opts.get('expanded', True))

    def makeWidget(self):
        """
            Make and initialize an instance of Plain_text_pb object from parameter options dictionnary (using 'readonly' key).

            Returns
            -------
            Plain_text_pb object
                The initialized object.

            See Also
            --------
            Plain_text_pb, buttonClicked
        """
        self.w = Plain_text_pb()
        self.w.text_edit.setReadOnly(self.param.opts.get('readonly', False))
        self.w.value = self.w.get_value
        self.w.setValue = self.w.set_value
        self.w.sigChanged = self.w.value_changed
        self.w.add_pb.clicked.connect(self.buttonClicked)
        return self.w

    def buttonClicked(self):
        text, ok = QtWidgets.QInputDialog.getText(None, "Enter a value to add to the parameter",
                                                  "String value:", QtWidgets.QLineEdit.Normal)
        if ok and not (text == ""):
            self.param.setValue(self.param.value() + '\n' + text)


class Plain_text_pb(QtWidgets.QWidget):
    """
        ================ ========================
        **Attributes**    **Type**
        *value_changed*   instance of pyqt Signal
        ================ ========================

        See Also
        --------
        initUI, emitsignal
    """
    value_changed = pyqtSignal(str)

    def __init__(self):
        QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))
        super(Plain_text_pb, self).__init__()

        self.initUI()
        self.text_edit.textChanged.connect(self.emitsignal)

    def emitsignal(self):
        """
            Emit the value changed signal from the text_edit attribute.
        """
        text = self.text_edit.toPlainText()
        self.value_changed.emit(text)

    def set_value(self, txt):
        """
            Set the value of the text_edit attribute.

            =============== =========== ================================
            **Parameters**    **Type**    **Description**
            *txt*             string      the string value to be setted
            =============== =========== ================================
        """
        self.text_edit.setPlainText(txt)

    def get_value(self):
        """
            Get the value of the text_edit attribute.

            Returns
            -------
            string
                The string value of text_edit.
        """
        return self.text_edit.toPlainText()

    def initUI(self):
        """
            Init the User Interface.
        """

        self.hor_layout = QtWidgets.QHBoxLayout()
        self.text_edit = QtWidgets.QPlainTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setMaximumHeight(50)

        self.add_pb = QtWidgets.QPushButton()
        self.add_pb.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/Icon_Library/Add2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_pb.setIcon(icon3)
        self.hor_layout.addWidget(self.text_edit)

        verlayout = QtWidgets.QVBoxLayout()
        verlayout.addWidget(self.add_pb)
        verlayout.addStretch()
        self.hor_layout.addLayout(verlayout)
        self.hor_layout.setSpacing(0)
        self.setLayout(self.hor_layout)


class Plain_text_pbParameter(Parameter):
    """Editable string; displayed as large text box in the tree."""
    itemClass = Plain_text_pbParameterItem
    sigActivated = pyqtSignal(object)

    def activate(self):
        """
            Send the Activated signal.
        """
        self.sigActivated.emit(self)
        self.emitStateChanged('activated', None)


registerParameterType('text_pb', Plain_text_pbParameter, override=True)


class TextParameterItemCustom(pTypes.TextParameterItem):
    def __init__(self, param, depth):
        super(TextParameterItemCustom, self).__init__(param, depth)

        self.textBox.setMaximumHeight(50)


class TextParameter(Parameter):
    """Editable string; displayed as large text box in the tree."""
    itemClass = TextParameterItemCustom


registerParameterType('text', TextParameter, override=True)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = QTimeCustom()
    ex.setMinuteIncrement(30)
    ex.show()
    sys.exit(app.exec_())
