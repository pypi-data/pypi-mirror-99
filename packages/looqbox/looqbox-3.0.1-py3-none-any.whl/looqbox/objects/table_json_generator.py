from looqbox.objects.looq_object import LooqObject
import warnings
import types


def cel_to_column(column, attribute, cell_component, column_component):
    cell_attribute = getattr(cell_component, attribute)
    column_attribute = getattr(column_component, attribute)

    cell_column_attribute = cell_attribute.get(column)

    is_function = isinstance(cell_column_attribute, types.FunctionType)
    if is_function:
        return None

    is_string = isinstance(cell_column_attribute, str)
    is_list = isinstance(cell_column_attribute, list)
    is_dict = isinstance(cell_column_attribute, dict)
    single_element_list = True if is_list and len(cell_column_attribute) == 1 else False
    single_element_dict = True if is_dict and len(cell_column_attribute) == 1 else False
    has_dicts = any(isinstance(element, dict) for element in cell_attribute.get(column, list()))

    if is_string or single_element_list or single_element_dict:
        column_attribute[column] = cell_attribute[column]
        del cell_attribute[column]
        cel_to_col_warning(attribute)

    elif has_dicts and attribute == "value_link":
        column_attribute[column] = cell_attribute[column]
        del cell_attribute[column]
        cel_to_col_warning(attribute)

    elif is_dict and attribute == "value_style":
        column_attribute[column] = cell_attribute[column]
        del cell_attribute[column]
        cel_to_col_warning(attribute)


def cel_to_col_warning(attr=None):
    col_attr = attr.replace("cell", "col")
    warnings.warn("use {0} attribute instead of {1}".format(col_attr, attr))


class TableJson(LooqObject):

    def __init__(self,
                 data=None,
                 cell_link=None,
                 cell_style=None,
                 cell_class=None,
                 cell_tooltip=None,
                 cell_format=None,
                 cell_filter=None):

        super().__init__()
        self.data = data
        self.cell_link = cell_link
        self.cell_style = cell_style
        self.cell_class = cell_class
        self.cell_format = cell_format
        self.cell_tooltip = cell_tooltip
        self.cell_filter = cell_filter

    def cell_config(self, config_dict, column, idx=None):

        config_dict[column] = {
                "filter": None,
                "class": None,
                "style": None,
                "format": None,
                "tooltip": None,
                "drill": None
            }

        self._get_link(config_dict, column, idx)
        self._get_style(config_dict, column, idx)
        self._get_class(config_dict, column, idx)
        self._get_format(config_dict, column, idx)
        self._get_tooltip(config_dict, column, idx)
        self._get_filter(config_dict, column, idx)

        # Remove unnecessary fields
        config_dict[column] = self.remove_json_nones(config_dict[column])
        if not config_dict[column]:
            del config_dict[column]

        return config_dict

    def _get_link(self, config_dict, column, idx):
        if isinstance(self.cell_link, dict):
            mode = "dropdown"
            if isinstance(self.cell_link.get(column), str) or \
                    isinstance(self.cell_link.get(idx, dict()).get(column), str):
                mode = "link"
            if any(isinstance(element, list) for element in self.cell_link.get(column, list())):
                link_list = list(zip(*self.cell_link.get(column)))
                links = {}
                counter = 0
                for link in link_list:
                    if self.cell_link.get(counter):
                        if self.cell_link[counter].get(column):
                            self.cell_link[counter][column] = link

                        links[counter] = self.cell_link.get(counter)
                    else:
                        links[counter] = {}
                        links[counter][column] = link
                    counter += 1
                self.cell_link = links
                self._get_link(config_dict, column, idx)

            elif self.cell_link.get(column):

                config_dict[column]["drill"] = {
                    "active": True,
                    "mode": mode,
                    "content": self.cell_link[column]}

            elif self.cell_link.get(idx, dict()).get(column):
                config_dict[column]["drill"] = {
                    "active": True,
                    "mode": mode,
                    "content": self.cell_link[idx][column]}

    def _get_style(self, config_dict, column, idx):
        if idx is not None and self.cell_style.get(idx):
            config_dict[column]["style"] = self.cell_style.get(idx).get(column)

        elif self.cell_style is None:
            config_dict[column]["style"] = None

        elif isinstance(self.cell_style.get(column), types.FunctionType):
            styles = tuple(map(self.cell_style.get(column), self.data[column]))
            index = 0
            style_dict = {}
            for style in styles:
                style_dict[index] = {}
                style_dict[index][column] = style
                index += 1
            self.cell_style = style_dict
            self._get_style(config_dict, column, idx)

        elif isinstance(self.cell_style, dict):
            config_dict[column]["style"] = self.cell_style.get(column)

        else:
            raise TypeError("Style is not a dictionary or a function")  # TODO pass table attribute in the message

    def _get_class(self, config_dict, column, idx):
        if idx is not None and self.cell_class.get(idx):
            config_dict[column]["class"] = self.cell_class.get(idx).get(column)

        elif self.cell_class.get(column) is None:
            config_dict[column]["class"] = None

        elif isinstance(self.cell_class, dict):
            if len(self.cell_class.get(column, list())) == self.data.shape[0]:
                if self.cell_class.get(column)[idx] is not None:
                    config_dict[column]["class"] = [self.cell_class.get(column)[idx]]

            # Class attribute must be a list
            elif not isinstance(config_dict[column]["class"], list):
                config_dict[column]["class"] = [self.cell_class.get(column)]

            else:
                config_dict[column]["class"] = self.cell_class.get(column)

    def _get_tooltip(self, config_dict, column, idx):
        if idx is not None and self.cell_tooltip.get(idx):
            if self.cell_tooltip.get(idx).get(column):
                config_dict[column]["tooltip"] = {
                    "active": True,
                    "value": self.cell_tooltip.get(idx).get(column)}

        elif isinstance(self.cell_tooltip, dict):
            if len(self.cell_tooltip.get(column, list())) == self.data.shape[0] and self.data.shape[0] != 0:
                if self.cell_tooltip.get(column)[idx] is not None:
                    config_dict[column]["tooltip"] = {
                        "active": True,
                        "value": self.cell_tooltip.get(column)[idx]}

            elif self.cell_tooltip.get(column):

                config_dict[column]["tooltip"] = {
                    "active": True,
                    "value": self.cell_tooltip[column]}

    def _get_format(self, config_dict, column, idx):
        if isinstance(self.cell_format, dict):

            if idx is not None and self.cell_format.get(idx):
                # config_dict[column]["format"] = self.value_format.get(idx).get(column)

                if isinstance(self.cell_format[idx][column], str):
                    config_dict[column]["format"] = {
                        "active": True,
                        "value": self.cell_format[idx][column]}
                else:
                    config_dict[column]["format"] = {
                        "active": self.cell_format[idx][column].get("active", True),
                        "value": self.cell_format[idx][column].get("value")}

            elif self.cell_format.get(column):

                if isinstance(self.cell_format[column], str):
                    config_dict[column]["format"] = {
                        "active": True,
                        "value": self.cell_format[column]}
                else:
                    config_dict[column]["format"] = {
                        "active": self.cell_format[column].get("active", True),
                        "value": self.cell_format[column].get("value")}  # TODO add error messages

    def _get_filter(self, config_dict, column, idx):
        if self.cell_filter is None:
            config_dict[column]["filter"] = None

        if isinstance(self.cell_filter, dict):
            helper_filter = self.cell_filter

            if helper_filter.get(column):

                if isinstance(helper_filter[column], dict) and len(helper_filter[column]) != 0:

                    if not isinstance(helper_filter[column]["active"], bool):
                        helper_filter[column]["active"] = False  # TODO add warning
                        # "headFilter$active must be of type logical. A FALSE value was assigned."

                    config_dict[column]["filter"] = {
                        "active": helper_filter[column].get("active", True),
                        "mode": helper_filter[column].get("mode", "search"),
                        "filters": helper_filter[column].get("filters", list())}

                    # Filter method in search mode can`t have filters
                    if config_dict[column]["filter"]["mode"] == "search":
                        config_dict[column]["filter"]["filters"] = list()


class RowJson(LooqObject):

    def __init__(self,
                 data=None,
                 value_link=None,
                 value_style=None,
                 value_class=None,
                 value_tooltip=None,
                 value_format=None,
                 value_filter=None):

        super().__init__()
        self.data = data
        self.value_link = value_link
        self.value_style = value_style
        self.value_class = value_class
        self.value_format = value_format
        self.value_tooltip = value_tooltip
        self.value_filter = value_filter

    def row_config(self, idx, cell_generator):
        row_config = {
            "class": self._get_row_class(idx, cell_generator),
            "style": self._get_row_style(idx, cell_generator),
            "format": self._get_row_format(idx, cell_generator),
            "tooltip": self._get_row_tooltip(idx, cell_generator),
            "drill": self._get_row_link(idx, cell_generator)
        }

        return self.remove_json_nones(row_config)

    def _get_row_class(self, idx, cell_generator):
        try:
            row_class_idx = self.value_class.get(idx)
        except:
            row_class_idx = self.value_class

        # Apply row_class if it is a function
        if isinstance(row_class_idx, types.FunctionType):
            classes = tuple(map(row_class_idx, self.data.iloc[idx]))
            cell_generator.cell_class = {idx: dict(zip(self.data.columns, classes))}

        elif isinstance(row_class_idx, list):
            return row_class_idx

        elif row_class_idx:
            return [row_class_idx]

    def _get_row_format(self, idx, cell_generator):
        try:
            row_format_idx = self.value_format.get(idx)
        except:
            row_format_idx = self.value_format

        if isinstance(row_format_idx, types.FunctionType):
            formats = tuple(map(row_format_idx, self.data.iloc[idx]))
            cell_generator.cell_format = {idx: dict(zip(self.data.columns, formats))}

        elif row_format_idx:
            if isinstance(row_format_idx, str):
                return dict(active=True, value=row_format_idx)
            else:
                return dict(active=row_format_idx.get("active", True),
                            value=row_format_idx.get("value"))

    def _get_row_style(self, idx, cell_generator):
        try:
            row_style_idx = self.value_style.get(idx)
        except:
            row_style_idx = self.value_style

        if isinstance(row_style_idx, types.FunctionType):
            styles = tuple(map(row_style_idx, self.data.iloc[idx]))
            cell_generator.cell_style = {idx: dict(zip(self.data.columns, styles))}

        elif row_style_idx:
            return row_style_idx

    def _get_row_tooltip(self, idx, cell_generator):
        try:
            row_tooltip_idx = self.value_tooltip.get(idx)
        except:
            row_tooltip_idx = self.value_tooltip

        if isinstance(row_tooltip_idx, str):
            return dict(active=True, value=row_tooltip_idx)

        elif row_tooltip_idx:
            return row_tooltip_idx

    def _get_row_link(self, idx, cell_generator):
        try:
            row_link_idx = self.value_link.get(idx)
        except:
            row_link_idx = self.value_link
            self.value_link = {
                0: row_link_idx
            }

        if any(isinstance(element, list) for element in self.value_link.get(idx, list())):
            links = dict(zip(self.data.columns, zip(*row_link_idx)))
            cell_generator.cell_link.update({idx: links})

        elif isinstance(row_link_idx, str):
            drill_dict = {
                "active": True,
                "mode": "link",
                "content": dict(text=None, link=row_link_idx)
            }
            return drill_dict

        elif row_link_idx:
            drill_dict = {
                "active": True,
                "mode": "dropdown",
                "content": row_link_idx
            }
            return drill_dict
