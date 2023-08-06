# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class PolyLineAnimate(Component):
    """A PolyLineAnimate component.


Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks.
- startAnimation (boolean; required)
- data (list; required)
- center (list; optional)
- zoom (number; required)
- style (dict; optional)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, startAnimation=Component.REQUIRED, data=Component.REQUIRED, center=Component.UNDEFINED, zoom=Component.REQUIRED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'startAnimation', 'data', 'center', 'zoom', 'style']
        self._type = 'PolyLineAnimate'
        self._namespace = 'dash_dthree'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'startAnimation', 'data', 'center', 'zoom', 'style']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['startAnimation', 'data', 'zoom']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(PolyLineAnimate, self).__init__(**args)
