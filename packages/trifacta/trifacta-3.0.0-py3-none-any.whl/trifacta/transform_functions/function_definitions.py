import numpy as np
import pandas as pd
import regex
import random
from trifacta.transform_functions.quote_matcher import QuoteMatcher

""" 
This file contains definition for custom transform functions.
"""


# -------------------- TYPE-CAST FUNCTIONS ----------------------


def to_boolean(val):
    str_cast_map = {
        'false': False,
        'f': False,
        '0': False,
        'off': False,
        'no': False,
        'n': False,
        'true': True,
        't': True,
        '1': True,
        'on': True,
        'yes': True,
        'y': True
    }
    if pd.isnull(val):
        return np.nan
    elif isinstance(val, bool):
        return bool(val)
    elif isinstance(val, int):
        return str_cast_map.get(str(val).strip().lower(), np.nan)
    elif isinstance(val, str):
        return str_cast_map.get(val.strip().lower(), np.nan)
    return np.nan


def to_double(val):
    if pd.isnull(val):
        return np.nan
    elif isinstance(val, float):
        return float(val)
    elif isinstance(val, np.double):
        return float(val)
    elif isinstance(val, int):
        return float(val)
    elif isinstance(val, np.int64):
        return float(val)
    elif isinstance(val, bool):
        return float(1.0) if val else float(0.0)
    elif isinstance(val, str):
        try:
            d = float(val)
            if d == float('inf') or d == float('nan'):
                return np.nan
            elif abs(d) < np.finfo('d').min:
                return 0.0
            return d
        except Exception as e:
            return np.nan
    return np.nan


def to_integer(val):
    if pd.isnull(val):
        return np.nan
    elif isinstance(val, int) or isinstance(val, np.int_):
        return np.int64(val)
    elif isinstance(val, float) or isinstance(val, np.float_):
        float_val = np.float64(val)
        if float_val == round(float_val):
            return np.int64(float_val)
    elif isinstance(val, bool):
        return np.int64(1) if val else np.int64(0)
    elif isinstance(val, str):
        try:
            # Type casting string directly to int64 doesn't work as expected for big numbers.
            # It causes issues with pandas IntegerArray while type casting values to Int64.
            float_val = np.float64(val)
            if float_val == round(float_val):
                return np.int64(float_val)
        except Exception as e:
            return np.nan
    return np.nan


# -------------------- TYPE-VALIDATION FUNCTIONS ----------------------

def is_empty(x):
    if x == '' or pd.isna(x):
        return True
    return False


def is_boolean(x):
    x = to_boolean(x)
    if pd.isna(x):
        return False
    elif isinstance(x, bool):
        return True
    return False


def is_string(x):
    if type(x) is str:
        return True
    return False


def is_integer(x):
    x = to_integer(x)
    if pd.isna(x):
        return False
    elif isinstance(x, np.int_):
        return True
    return False


def is_double(x):
    x = to_double(x)
    if pd.isna(x):
        return False
    elif isinstance(x, float):
        return True
    return False


# -------------------- STRING FUNCTIONS ----------------------

class Replace:
    no_action = False

    def __init__(self, replace_on, replace_with, global_, ignore_case):
        self.replace_on_pattern = None
        try:
            if replace_on is not None:
                if ignore_case:
                    self.replace_on_pattern = regex.compile(replace_on, regex.IGNORECASE, regex.VERSION1)
                else:
                    self.replace_on_pattern = regex.compile(replace_on, regex.VERSION1)
        except Exception:
            self.replace_on_pattern = None
        self.global_ = global_
        self.replace_with = replace_with
        if self.replace_on_pattern is None or self.replace_on_pattern.pattern == '' or self.replace_with is None:
            self.no_action = True

    def exec(self, val):
        val = str(val)
        if self.no_action:
            return val

        try:
            # 0 means replace all
            replacement_count = 0 if self.global_ else 1

            replaced_val = self.replace_on_pattern.sub(self.replace_with, val, count=replacement_count)
            return replaced_val
        except Exception:
            return None


class ReplacePosition:

    def __init__(self, start_index, end_index, replacement):
        self.start_index = max(start_index, 0)
        self.end_index = max(end_index, 0)
        self.replacement = replacement

    def exec(self, val):
        if pd.isnull(val):
            return val
        val = str(val)
        if len(val) <= self.start_index or self.start_index > self.end_index:
            return val

        substrings = [val[:self.start_index], self.replacement]
        if len(val) > self.end_index:
            substrings.append(val[self.end_index:])

        return ''.join(substrings)


class ReplaceColumn:

    def __init__(self, is_pattern_column, global_, ignore_case):
        self.is_pattern_column = is_pattern_column
        self.global_ = global_
        self.ignore_case = ignore_case

    def exec(self, val, pattern, replacement):
        if pd.isnull(val):
            return val
        val = str(val)
        if pattern is None or pattern == '':
            return val

        temp_pattern = regex.escape(pattern) if self.is_pattern_column else pattern
        try:
            if self.ignore_case:
                replace_on_pattern = regex.compile(temp_pattern, regex.IGNORECASE, regex.VERSION1)
            else:
                replace_on_pattern = regex.compile(temp_pattern, regex.VERSION1)

            # 0 means replace all
            replacement_count = 0 if self.global_ else 1
            replaced_val = replace_on_pattern.sub(replacement, val, count=replacement_count)
            return replaced_val

        except Exception:
            return None


class Matches:
    def __init__(self, pattern, ignore_case):
        self.pattern = None
        if pattern is not None and len(pattern) > 0:
            if ignore_case:
                self.pattern = regex.compile(pattern, regex.IGNORECASE, regex.VERSION1)
            else:
                self.pattern = regex.compile(pattern, regex.VERSION1)

    def exec(self, val):
        if self.pattern is None:
            return True
        if pd.isnull(val):
            return False

        val = str(val)
        match = self.pattern.search(val)
        return match is not None


class CountPattern:
    def __init__(self, pattern, ignore_case):
        self.pattern = None
        if pattern is not None:
            if ignore_case:
                self.pattern = regex.compile(pattern, regex.IGNORECASE, regex.VERSION1)
            else:
                self.pattern = regex.compile(pattern, regex.VERSION1)

    def exec(self, val):
        if self.pattern is None or pd.isnull(val):
            return 0

        start_pos = 0
        count = 0
        while start_pos < len(val):
            match = self.pattern.search(val, start_pos)
            if match is None:
                break

            count += 1
            start_pos = match.end()

        return count


class Find:
    def __init__(self, pattern, ignore_case):
        self.pattern = None
        if pattern is not None:
            if ignore_case:
                self.pattern = regex.compile(pattern, regex.IGNORECASE, regex.VERSION1)
            else:
                self.pattern = regex.compile(pattern, regex.VERSION1)

    def exec(self, val, start_position):
        if pd.isnull(val) or start_position is None or start_position < 0 or \
                start_position >= len(val) or self.pattern is None:
            return None

        val = str(val)
        match = self.pattern.search(val, start_position)
        if match is None:
            return None

        return match.start() + start_position


class RightFind:
    def __init__(self, pattern, ignore_case):
        self.pattern = None
        if pattern is not None:
            if ignore_case:
                self.pattern = regex.compile(pattern, regex.IGNORECASE, regex.VERSION1)
            else:
                self.pattern = regex.compile(pattern, regex.VERSION1)

    def exec(self, val, start_position):
        if pd.isnull(val) or start_position is None or start_position < 0 or \
                start_position >= len(val) or self.pattern is None:
            return None

        val = str(val)
        start_search_position = 0
        end_position = len(val) - start_position
        match_position = None
        while start_search_position < end_position:
            match = self.pattern.search(val, start_search_position, end_position)
            if match is None:
                break
            match_position = match.start()
            start_search_position = match_position + 1

        return match_position


class NthOccurrence:
    LEFT_DIRECTION = 'left'
    RIGHT_DIRECTION = 'right'

    def __init__(self, pattern, ignore_case):
        self.pattern = None
        if pattern is not None or len(pattern) == 0:
            if ignore_case:
                self.pattern = regex.compile(pattern, regex.IGNORECASE, regex.VERSION1)
            else:
                self.pattern = regex.compile(pattern, regex.VERSION1)

    def exec(self, val, match_number, direction):
        if pd.isnull(val) or len(val) == 0 or match_number is None or match_number < 0 or \
                direction is None or self.pattern is None:
            return None

        val = str(val)
        matches = [match.start() for match in self.pattern.finditer(val)]

        if match_number > len(matches):
            return None

        match_position = None
        if direction == self.LEFT_DIRECTION:
            match_position = match_number - 1
        elif direction == self.RIGHT_DIRECTION:
            match_position = len(matches) - match_number

        return matches[match_position] if match_position is not None else None


class ColumnFind:

    def __init__(self, ignore_case, start):
        self.ignore_case = False if ignore_case is None else ignore_case
        self.start = -1 if start is None else start

    def exec(self, val, pattern):
        """
        @param val: basestring
        @param pattern: basestring
        """
        if pd.isnull(val) or pd.isnull(pattern):
            return None
        val = str(val)
        pattern = str(pattern)
        if len(pattern) == 0 or self.start < 0 or self.start > len(val):
            return None
        try:
            if self.ignore_case:
                val, pattern = val.lower(), pattern.lower()
            return val.index(pattern, self.start)
        except ValueError:
            return None


# -------------------- MATH FUNCTIONS ----------------------

class Rand:
    def __init__(self, seed):
        random.seed(seed)

    @staticmethod
    def exec():
        return random.random()


# -------------------- TEXT FUNCTIONS ----------------------

class Text:
    """
    Generic TextTransform function, needs to extended by specific TextTransform UDF
    implementation class.
    """

    def __init__(self, on, limit, ignore_case, quote, target_group, num_outputs):
        self.on = on
        self.limit = limit
        self.num_outputs = num_outputs
        self.ignore_case = ignore_case
        self.quote = quote
        self.target_group = target_group
        self.pattern = None
        if ignore_case:
            self.pattern = regex.compile(self.on, regex.IGNORECASE, regex.VERSION1)
        else:
            self.pattern = regex.compile(self.on, regex.VERSION1)

    def get_pandas_series(self, value_list):
        return pd.Series(value_list)

    def exec(self, val):
        if pd.isnull(val) or val == '':
            empty_col = [''] * self.num_outputs
            return self.get_pandas_series(empty_col)

        if self.limit == 0:
            cols = [val] * self.num_outputs
            return cols

        quote_matcher = QuoteMatcher(val, self.quote) if (self.quote is not None and len(self.quote) > 0) else None
        start_pos, end_pos = 0, len(val)
        num_matches = 0
        result = []
        try:
            while start_pos < end_pos and num_matches < self.limit:
                m = self.pattern.search(val, start_pos)
                if m is None:
                    break
                start_target_group_index = m.start(self.target_group)
                end_target_group_index = m.end(self.target_group)

                if quote_matcher is not None and quote_matcher.in_quotes(m.start()):
                    continue

                self.push_regex_match(result, val, start_pos, start_target_group_index, end_target_group_index)
                start_pos = end_target_group_index
                num_matches += 1

        except Exception as e:
            print('Text transform operation failed, {}'.format(e))
            return self.handle_regex_exception(val)

        self.push_remaining_string(result, val, start_pos)
        self.backfill_columns(result)
        return self.get_pandas_series(result)

    def push_regex_match(self, output_columns, input_val, start_search_index,
                         start_target_group_ind, end_target_group_ind):
        # Provide definition in specific function implementation class.
        pass

    def push_remaining_string(self, output_columns, input_val, start_index):
        # Provide definition in specific function implementation class.
        pass

    def backfill_columns(self, output_columns):
        curr_size = len(output_columns)
        null_columns = [pd.NA] * (self.num_outputs - curr_size - 1)
        output_columns.extend(null_columns)

    def handle_regex_exception(self, input_val):
        result = []
        self.push_remaining_string(result, input_val, 0)
        self.backfill_columns(result)
        return result


class Split(Text):
    def __init__(self, on, limit, ignore_case, quote, target_group):
        super().__init__(on, limit, ignore_case, quote, target_group, limit + 1)

    def push_regex_match(self, output_columns, input_val, start_search_index,
                         start_target_group_index, end_target_group_index):
        output_columns.append(input_val[start_search_index: start_target_group_index])

    def push_remaining_string(self, output_columns, input_val, start_index):
        if start_index >= len(input_val):
            output_columns.append('')
        else:
            output_columns.append(input_val[start_index:])

    def backfill_columns(self, output_columns):
        # if input value is empty line, then first generated
        # column would be empty string
        if len(output_columns) == 0 and self.num_outputs > 0:
            output_columns.append('')
        super().backfill_columns(output_columns)


class Extract(Text):
    def __init__(self, on, limit, ignore_case, quote, target_group):
        super().__init__(on, limit, ignore_case, quote, target_group, limit)

    def push_regex_match(self, output_columns, input_val, start_search_index, start_target_group_index,
                         end_target_group_index):
        output_columns.append(input_val[start_target_group_index: end_target_group_index])

    def push_remaining_string(self, output_columns, input_column, start_index):
        # No need to do anything here as remaining string is not needed in an
        # Extract transform operation.
        pass


class SplitPositions:
    def __init__(self, positions):
        self.positions = [0] + positions

    def exec(self, val):
        if pd.isnull(val) or val == '':
            return pd.Series([''] * len(self.positions))

        output = []
        for i in range(0, len(self.positions) - 1):
            start_ind = min(self.positions[i], len(val))
            end_ind = min(self.positions[i + 1], len(val))
            output.append(val[start_ind: end_ind])

        start_ind = min(self.positions[-1], len(val))
        output.append(val[start_ind:])

        return pd.Series(output)
