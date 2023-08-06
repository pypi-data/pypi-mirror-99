import pandas as pd
import numpy as np
from azureml.studio.core.utils.missing_value_utils import has_na, drop_na
from azureml.studio.core.data_frame_schema import ElementTypeName
from azureml.studio.core.logger import common_logger
from pandas.api.types import is_datetime64_ns_dtype, is_timedelta64_ns_dtype


# This method is from azureml.studio.common.utils.datetimeutils, and will be removed in the future.
def is_datetime_dtype(argument):
    return is_datetime64_ns_dtype(argument)


# This method is from azureml.studio.common.utils.datetimeutils, and will be removed in the future.
def is_timespan_dtype(argument):
    return is_timedelta64_ns_dtype(argument)


# This method is from azureml.studio.common.datatable.data_type_conversions, and will be removed in the future.
def _drop_na_and_convert(column, new_type):
    column_has_na = has_na(column)
    # If no na value, directly convert with the type.
    if not column_has_na:
        return column.astype(new_type)

    # Otherwise, only convert the non-na values.
    # Fix bug 513210: If the index contain duplicated values, a ValueError will be raised by the reindex function.
    # To fix this bug, we store the original index, then update the column index with 1..n,
    # and recover the original index after we convert the column with the new type.
    original_index = column.index
    column.index = range(len(column))

    column_without_na = drop_na(column, reset_index=False)
    # Use np.array instead of python list for better efficiency.
    index_of_na = np.array(column.index.difference(column_without_na.index))

    column_new = column_without_na.astype(new_type).reindex(index=column.index)
    if new_type == ElementTypeName.INT or new_type == ElementTypeName.FLOAT:
        column_new[index_of_na] = np.nan
    else:
        column_new[index_of_na] = column[index_of_na]

    column_new.index = original_index
    return column_new


# This method is from azureml.studio.common.datatable.data_type_conversions, and will be removed in the future.
def convert_to_str(column):
    column_new = _drop_na_and_convert(column, ElementTypeName.STRING)
    # Replace pd.NaT (missing value in date-time column) with np.nan
    # Otherwise this column cannot be dumped into parquet
    column_new.replace(to_replace=pd.NaT, value=np.nan, inplace=True)
    return column_new


def convert_to_int(column):
    if is_datetime_dtype(column) or is_timespan_dtype(column):
        common_logger.info(f'Convert time to int with the unit of seconds')
        column_new = _drop_na_and_convert(column, ElementTypeName.INT)
        # The values are of the unit of nano-seconds
        # To convert to seconds, need to divide by 1e9
        if has_na(column_new):
            return column_new / 1e9
        return (column_new / 1e9).astype(ElementTypeName.INT)

    return _drop_na_and_convert(column, ElementTypeName.INT)


def convert_to_float(column):
    if is_datetime_dtype(column) or is_timespan_dtype(column):
        common_logger.warning(
            f'{ElementTypeName.DATETIME} and {ElementTypeName.TIMESPAN} '
            f'columns will first be converted into {ElementTypeName.INT} type, then {ElementTypeName.FLOAT} type ')
        column = convert_to_int(column)

    # Replace pd.NaT (missing value in date-time column) with np.nan
    # Otherwise error will be raised in column.astype
    column.fillna(value=np.nan, inplace=True)

    return column.astype(ElementTypeName.FLOAT)
