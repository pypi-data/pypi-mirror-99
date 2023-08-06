from .plot_config import PlotConfig


class PlotContext(object):
    UNKNOWN_AXIS = None
    VALUE_AXIS = "VALUE"
    DATE_AXIS = "DATE"
    INDEX_AXIS = "INDEX"
    COUNT_AXIS = "COUNT"
    DENSITY_AXIS = "DENSITY"
    DEPTH_AXIS = "DEPTH"
    AXIS_TYPES = [
        UNKNOWN_AXIS,
        COUNT_AXIS,
        DATE_AXIS,
        DENSITY_AXIS,
        DEPTH_AXIS,
        INDEX_AXIS,
        VALUE_AXIS,
    ]

    def __init__(self, plot_config, cases, key):
        super(PlotContext, self).__init__()
        self._key = key
        self._cases = cases
        self._plot_config = plot_config
        self.refcase_data = None
        self.history_data = None
        self._log_scale = False

        self._date_support_active = True
        self._x_axis = None
        self._y_axis = None

    def plotConfig(self):
        """ :rtype: PlotConfig """
        return self._plot_config

    def cases(self):
        """ :rtype: list of str """
        return self._cases

    def key(self):
        """ :rtype: str """
        return self._key

    def deactivateDateSupport(self):
        self._date_support_active = False

    def isDateSupportActive(self):
        """ @rtype: bool """
        return self._date_support_active

    @property
    def x_axis(self):
        """ @rtype: str """
        return self._x_axis

    @x_axis.setter
    def x_axis(self, value):
        """ @type value: str """
        if not value in PlotContext.AXIS_TYPES:
            raise UserWarning(
                "Axis: '%s' is not one of: %s" % (value, PlotContext.AXIS_TYPES)
            )
        self._x_axis = value

    @property
    def y_axis(self):
        """ @rtype: str """
        return self._y_axis

    @y_axis.setter
    def y_axis(self, value):
        """ @type value: str """
        if not value in PlotContext.AXIS_TYPES:
            raise UserWarning(
                "Axis: '%s' is not one of: %s" % (value, PlotContext.AXIS_TYPES)
            )
        self._y_axis = value

    @property
    def log_scale(self):
        return self._log_scale

    @log_scale.setter
    def log_scale(self, value):
        self._log_scale = value
