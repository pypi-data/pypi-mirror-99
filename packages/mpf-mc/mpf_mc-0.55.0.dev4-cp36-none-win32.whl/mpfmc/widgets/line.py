"""Widget showing a line."""
from typing import Optional

from kivy.graphics import Line as KivyLine
from kivy.graphics.context_instructions import Color, Scale, Rotate
from kivy.properties import (ListProperty, NumericProperty, OptionProperty,
                             BooleanProperty)

from mpfmc.uix.widget import Widget
from mpfmc.core.utils import center_of_points_list

MYPY = False
if MYPY:   # pragma: no cover
    from mpfmc.core.mc import MpfMc     # pylint: disable-msg=cyclic-import,unused-import


class Line(Widget):

    """Widget showing a line."""

    widget_type_name = 'Line'
    animation_properties = ('color', 'thickness', 'opacity', 'points', 'rotation', 'scale')

    def __init__(self, mc: "MpfMc", config: dict, key: Optional[str] = None, **kwargs) -> None:
        del kwargs
        super().__init__(mc=mc, config=config, key=key)

        # The points in this widget are always relative to the bottom left corner
        self.anchor_pos = ("left", "bottom")

        # Bind to all properties that when changed need to force
        # the widget to be redrawn
        self.bind(color=self._draw_widget,
                  points=self._draw_widget,
                  thickness=self._draw_widget,
                  rotation=self._draw_widget,
                  scale=self._draw_widget)

        self._draw_widget()

    def _draw_widget(self, *args) -> None:
        """Establish the drawing instructions for the widget."""
        del args

        if self.canvas is None:
            return

        # TODO: allow user to set rotation/scale origin
        center = center_of_points_list(self.points)
        self.canvas.clear()

        with self.canvas:
            Color(*self.color)
            Scale(self.scale, origin=center)
            Rotate(angle=self.rotation, origin=center)
            KivyLine(points=self.points,
                     width=self.thickness,
                     cap=self.cap,
                     joint=self.joint,
                     cap_precision=self.cap_precision,
                     joint_precision=self.joint_precision,
                     close=self.close)

    #
    # Properties
    #

    points = ListProperty()
    '''The list of points to use to draw the widget in (x1, y1, x2, y2...)
    format.

    :attr:`points` is a :class:`~kivy.properties.ListProperty`.
    '''

    cap = OptionProperty("round", options=["none", "square", "round"])
    '''The cap of the line, defaults to 'round'. Can be one of 'none',
    'square' or 'round'
    '''

    cap_precision = NumericProperty(10)
    '''Number of iterations for drawing the "round" cap, defaults to 10. The
    cap_precision must be at least 1.
    '''

    close = BooleanProperty(False)
    '''If True, the line will be closed.
    '''

    joint = OptionProperty("round", options=["none", "round", "bevel", "miter"])
    '''The join of the line, defaults to 'round'. Can be one of 'none', 'round',
    'bevel', 'miter'.
    '''

    joint_precision = NumericProperty(10)
    '''Number of iterations for drawing the "round" joint, defaults to 10. The
    joint_precision must be at least 1.
    '''

    thickness = NumericProperty(1.0)
    '''Width of the line.

    :attr:`thickness` is a :class:`~kivy.properties.NumericProperty` and defaults
    to 1.0.
    '''

    rotation = NumericProperty(0)
    '''Rotation angle value of the widget.

    :attr:`rotation` is an :class:`~kivy.properties.NumericProperty` and defaults to
    0.
    '''

    scale = NumericProperty(1.0)
    '''Scale value of the widget.

    :attr:`scale` is an :class:`~kivy.properties.NumericProperty` and defaults to
    1.0.
    '''


widget_classes = [Line]
