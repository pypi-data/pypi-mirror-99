# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Toolbar(Component):
    """A Toolbar component.


Keyword arguments:
- children (a list of or a singular dash component, string or number; optional)
- id (string; optional): The ID used to identify this component in Dash callbacks
- dataSource (string | list of strings | list of dicts | dict; optional): Binds the UI component to data
- disabled (boolean; default False): Specifies whether the UI component responds to user interaction
- elementAttr (dict; optional): Specifies the global attributes to be attached to the UI component's container element
- hint (string; optional): Specifies text for a hint that appears when a user pauses on the UI component
- hoverStateEnabled (boolean; default True): Specifies whether the UI component changes its state when a user pauses on it
- itemComponent (string | dict; optional): An alias for the itemTemplate property specified in React. Accepts a custom component.
- itemHoldTimeout (number; default 750): The time period in milliseconds before the onItemHold event is raised
- itemRender (string; optional): An alias for the itemTemplate property specified in React. Accepts a rendering function.
- items (list of strings | list of dicts | a list of or a singular dash component, string or number; default undefined): An array of items displayed by the UI component
- itemTemplate (string | dict; default 'item'): Specifies a custom template for items
- menuItemComponent (string | dict; optional): An alias for the menuItemTemplate property specified in React. Accepts a custom component.
- menuItemRender (string; optional): An alias for the menuItemTemplate property specified in React. Accepts a rendering function.
- menuItemTemplate (string | dict; default 'menuItem'): Specifies a custom template for menu items.
- noDataText (string; default 'No data to display'): The text or HTML markup displayed by the UI component if the item collection is empty
- onItemClick (string; optional): A function that is executed when a collection item is clicked or tapped
- rtlEnabled (boolean; default False): Switches the UI component to a right-to-left representation
- visible (boolean; default True): Specifies whether the UI component is visible
- width (number | string; default 'auto'): Specifies the UI component's width
- loading_state (dict; optional): Object that holds the loading state object coming from dash-renderer. loading_state has the following type: dict containing keys 'is_loading', 'prop_name', 'component_name'.
Those keys have the following types:
  - is_loading (boolean; optional): Determines if the component is loading or not
  - prop_name (string; optional): Holds which property is loading
  - component_name (string; optional): Holds the name of the component that is loading"""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, dataSource=Component.UNDEFINED, disabled=Component.UNDEFINED, elementAttr=Component.UNDEFINED, hint=Component.UNDEFINED, hoverStateEnabled=Component.UNDEFINED, itemComponent=Component.UNDEFINED, itemHoldTimeout=Component.UNDEFINED, itemRender=Component.UNDEFINED, items=Component.UNDEFINED, itemTemplate=Component.UNDEFINED, menuItemComponent=Component.UNDEFINED, menuItemRender=Component.UNDEFINED, menuItemTemplate=Component.UNDEFINED, noDataText=Component.UNDEFINED, onContentReady=Component.UNDEFINED, onDisposing=Component.UNDEFINED, onInitialized=Component.UNDEFINED, onItemClick=Component.UNDEFINED, onItemContextMenu=Component.UNDEFINED, onItemHold=Component.UNDEFINED, onItemRendered=Component.UNDEFINED, onOptionChanged=Component.UNDEFINED, rtlEnabled=Component.UNDEFINED, visible=Component.UNDEFINED, width=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'dataSource', 'disabled', 'elementAttr', 'hint', 'hoverStateEnabled', 'itemComponent', 'itemHoldTimeout', 'itemRender', 'items', 'itemTemplate', 'menuItemComponent', 'menuItemRender', 'menuItemTemplate', 'noDataText', 'onItemClick', 'rtlEnabled', 'visible', 'width', 'loading_state']
        self._type = 'Toolbar'
        self._namespace = 'dash_devextreme'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'dataSource', 'disabled', 'elementAttr', 'hint', 'hoverStateEnabled', 'itemComponent', 'itemHoldTimeout', 'itemRender', 'items', 'itemTemplate', 'menuItemComponent', 'menuItemRender', 'menuItemTemplate', 'noDataText', 'onItemClick', 'rtlEnabled', 'visible', 'width', 'loading_state']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Toolbar, self).__init__(children=children, **args)
