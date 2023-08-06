from typing import (
    Dict,
    Any,
    Callable,
    Tuple,
    Type,
    Union,
    List,
    Optional
)

from pandas import (
    DataFrame,
    Series,
    to_datetime
)
from pandas.core.generic import NDFrame

import numpy as np

from .directive import (
    parse,
    Directive,
    DirectiveCache,
    directive_cache
)

from .common import rolling_calc

from .meta import (
    ColumnInfo,

    init_stock_metas,
    copy_stock_metas,
    copy_clean_stock_metas,
    ensure_return_type
)


class StockDataFrame(DataFrame):
    """The wrapper class for `pandas.DataFrame`

    Args definitions are the same as `pandas.DataFrame`
    """

    _date_col: Optional[str] = None

    _stock_create_column: bool = False
    _stock_indexer_slice: Optional[slice] = None
    _stock_indexer_axis: int = 0

    # Directive cache can be shared between instances,
    # so declare as static property
    _stock_directives_cache: DirectiveCache = directive_cache

    _stock_aliases_map: Dict[str, str]
    _stock_columns_info_map: Dict[str, ColumnInfo]

    # Methods that used by pandas and sub classes
    # --------------------------------------------------------------------

    @property
    def _constructor(_) -> Type['StockDataFrame']:
        """
        This method overrides `DataFrame._constructor`
        which ensures the return type of several DataFrame methods
        """

        return StockDataFrame

    def __finalize__(self, other, *args, **kwargs) -> 'StockDataFrame':
        """
        Propagate metadata from other to self.

        This method overrides `DataFrame.__finalize__`
        which ensures the meta info of StockDataFrame
        """

        super().__finalize__(other, *args, **kwargs)

        if isinstance(other, StockDataFrame):
            copy_clean_stock_metas(
                other,
                self,
                other._stock_indexer_slice,
                other._stock_indexer_axis
            )

        return self

    def _slice(self, slice_obj: slice, axis: int = 0) -> 'StockDataFrame':
        """
        This method is called in several cases, self.iloc[slice] for example

        We mark the slice and axis here to prevent extra calculations
        """

        self._stock_indexer_slice = slice_obj
        self._stock_indexer_axis = axis

        try:
            result = super()._slice(slice_obj, axis)
        except Exception as e:
            raise e
        finally:
            self._stock_indexer_slice = None
            self._stock_indexer_axis = 0

        return result

    # --------------------------------------------------------------------

    def __init__(
        self,
        data=None,
        date_col: Optional[str] = None,
        *args,
        **kwargs
    ) -> None:
        DataFrame.__init__(self, data, *args, **kwargs)

        if self.columns.nlevels > 1:
            # For now, I admit,
            # there are a lot of works to support MultiIndex dataframes
            raise ValueError(
                'stock-pandas does not support dataframes with MultiIndex columns'  # noqa:E501
            )

        if isinstance(data, StockDataFrame):
            copy_stock_metas(data, self)
        else:
            init_stock_metas(self)

        self._date_col = date_col

        if date_col:
            self[date_col] = to_datetime(self[date_col])
            self.set_index(date_col, inplace=True)

    def __getitem__(self, key) -> Union[Series, 'StockDataFrame']:
        if isinstance(key, str):
            key = self._map_single_key(key)

            # We just return super __getitem__,
            # because the result must be series
            return super().__getitem__(key)

        if isinstance(key, list):
            key = self._map_keys(key)

        # else: key of another type

        result = super().__getitem__(key)

        if isinstance(result, Series):
            # The series has already been fulfilled by
            # `self._get_or_calc_series()`
            return result

        result = StockDataFrame(result)

        return result

    # Public Methods of stock-pandas
    # --------------------------------------------------------------------

    def get_column(self, name: str) -> Series:
        """
        Gets the column directly from dataframe by key.

        This method applies column name aliases before getting the value.

        Args:
            name (str): The name of the column

        Returns:
            np.Series
        """

        origin_name = name

        if name in self._stock_aliases_map:
            # Map alias, if the key is an alias
            name = self._stock_aliases_map[name]

        try:
            return self._get_item_cache(name)
        except KeyError:
            raise KeyError(f'column "{origin_name}" not found')

    def exec(
        self,
        directive_str: str,
        create_column: Optional[bool] = None
    ) -> np.ndarray:
        """
        Executes the given directive and returns a numpy ndarray according to the directive.

        This method is **NOT** Thread-safe.

        Args:
            directive_str (str): directive
            create_column (:obj:`bool`, optional): whether we should create a column for the calculated series.

        Returns:
            np.ndarray
        """

        if self._is_normal_column(directive_str):
            return self[directive_str].to_numpy()

        # We should call self.exec() without `create_column`
        # inside command formulas
        explicit_create_column = isinstance(create_column, bool)
        original_create_column = self._stock_create_column

        if explicit_create_column:
            self._stock_create_column = create_column
        else:
            # cases
            # 1. called by users
            # 2. or called by command formulas
            create_column = self._stock_create_column

        series = self._calc(directive_str)

        if explicit_create_column:
            # Set back to default value, since we complete calculatiing
            self._stock_create_column = original_create_column

        return series

    def alias(
        self,
        as_name: str,
        src_name: str
    ) -> None:
        """
        Defines column alias or directive alias

        Args:
            as_name (str): the alias name
            src_name (str): the name of the original column, or directive

        Returns:
            None
        """
        columns = self.columns
        if as_name in columns:
            raise ValueError(f'column "{as_name}" already exists')

        if src_name not in columns:
            raise ValueError(f'column "{src_name}" not exists')

        self._stock_aliases_map[as_name] = src_name

    def directive_stringify(
        self,
        directive_str: str
    ) -> str:
        """
        Stringify a `Directive` and get its full name which is the actual column of the dataframe

        Usage::

            stock.directive_stringify('boll')
            # It gets "boll:20,close"

        Args:
            directive_str (str): directive

        Returns:
            str
        """

        return str(self._parse_directive(directive_str))

    def rolling_calc(
        self,
        size: int,
        on: str,
        apply: Callable[[np.ndarray], Any],
        forward: bool = False,
        fill=np.nan
    ) -> np.ndarray:
        """Apply a 1-D function along the given column `on`

        Args:
            size (int): the size of the rolling window
            on (str | Directive): along which the function should be applied
            apply (Callable): the 1-D function to apply
            forward (:obj:`bool`, optional): whether we should look forward to get each rolling window or not (default value)
            fill (:obj:`any`): the value used to fill where there are not enough items to form a rolling window

        Returns:
            np.ndarray

        Usage::

            stock.rolling_calc(5, 'high', max)
            # Gets the 5-period highest of high value, which is equivalent to
            stock.exec('hhv:5').to_numpy()
        """

        array = self[on].to_numpy()

        *_, stride = array.strides

        return rolling_calc(
            array,
            size,
            apply,
            fill,
            stride,
            not forward
        )

    # --------------------------------------------------------------------

    def _map_keys(self, keys) -> List:
        return [
            self._map_single_key(key)
            for key in keys
        ]

    def _map_single_key(self, key):
        if not isinstance(key, str):
            # It might be an `pandas.DataFrame` indexer type,
            # or an KeyError which we should let pandas raise
            return key

        if key in self._stock_aliases_map:
            # Map alias, if the key is an alias
            key = self._stock_aliases_map[key]

        if self._is_normal_column(key):
            # There exists a column named `key`,
            # and it is a normal column
            return key

        # Not exists
        directive = self._parse_directive(key)

        # It is a valid directive
        # If the column exists, then fulfill it,
        #   else create it
        column_name, _ = self._get_or_calc_series(directive, True)

        # Append the real column name to the mapped key,
        #   So `pandas.DataFrame.__getitem__` could index the right column
        return column_name

    def _parse_directive(
        self,
        directive_str: str
    ) -> Directive:
        return parse(directive_str, self._stock_directives_cache)

    def _get_or_calc_series(
        self,
        directive: Directive,
        create_column: bool
    ) -> Tuple[str, np.ndarray]:
        """Gets the series column corresponds the `directive` or
        calculate by using the `directive`

        Args:
            directive (Directive): the parsed `Directive` instance
            create_column (bool): whether we should create a column for the
            calculated series

        Returns:
            Tuple[str, np.ndarray]: the name of the series, and the series
        """

        name = str(directive)

        if name in self._stock_columns_info_map:
            return name, self._fulfill_series(name)

        array, period = directive.run(
            self,
            # create the whole series
            slice(None)
        )

        if create_column:
            self._stock_columns_info_map[name] = ColumnInfo(
                len(self),
                directive,
                period
            )

            self._set_new_item(name, array)

        return name, array

    def _set_new_item(
        self,
        name: str,
        value: np.ndarray
    ) -> None:
        """Set a new column and avoid SettingWithCopyWarning by using
        pandas internal APIs

        see: https://github.com/pandas-dev/pandas/blob/v1.1.0/pandas/core/frame.py#L3114
        """  # noqa: E501

        NDFrame._set_item(self, name, value)

    def _fulfill_series(self, column_name: str) -> np.ndarray:
        column_info = self._stock_columns_info_map.get(column_name)
        size = len(self)

        array = self.get_column(column_name).to_numpy()

        if size == column_info.size:
            # Already fulfilled
            return array

        neg_delta = column_info.size - size

        # Sometimes, there is not enough items to calculate
        calc_delta = max(
            neg_delta - column_info.period + 1,
            - size
        )

        calc_slice = slice(calc_delta, None)
        fulfill_slice = slice(neg_delta, None)

        partial, _ = column_info.directive.run(self, calc_slice)

        if neg_delta == calc_delta:
            array = partial
        else:
            array[fulfill_slice] = partial[fulfill_slice]

        self._set_new_item(column_name, array)

        column_info.size = size

        return array

    def _is_normal_column(self, column_name) -> bool:
        return column_name in self.columns and \
            column_name not in self._stock_columns_info_map

    def _calc(self, directive_str: str) -> np.ndarray:
        directive = self._parse_directive(directive_str)

        _, series = self._get_or_calc_series(
            directive,
            self._stock_create_column
        )

        return series


METHODS_TO_ENSURE_RETURN_TYPE = [
    # TODO:
    # astype needs special treatment
    # astype(dict_like) could not ensure return type
    ('astype', True)
]

for method, should_apply_constructor in METHODS_TO_ENSURE_RETURN_TYPE:
    ensure_return_type(StockDataFrame, method, should_apply_constructor)
