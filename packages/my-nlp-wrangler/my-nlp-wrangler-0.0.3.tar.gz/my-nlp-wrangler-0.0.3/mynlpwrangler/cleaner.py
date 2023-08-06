from urllib.parse import urlparse
import re
import string
import pandas as pd
import numpy as np
from typing import Callable


class ArticleCleaner():
    """
    clean data  for nlp
    """

    def __init__(self, col: str, cleaned_col: str = "clean_text"):
        self._col = col
        self._cleaned_col = cleaned_col
        self._clean_data_function = None

    def remove_url(self, setence: str):
        """
        remove the url from the setence
        """
        try:
            result = urlparse(setence)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def remove_punctuation(self, line: str):
        """
        remove punctuation from the sentence
        """
        rule = re.compile("[^\u4e00-\u9fa5^.^a-z^A-Z]")
        line = rule.sub(' ', line)
        line = re.sub('[%s]' % re.escape(string.punctuation), '', line)
        return line

    def set_clean_data(self, clean_data_fun: Callable):
        """ set customer  clean sentence function for dataframe

        Parameters
        ----------
        clean_data_fun: Callable
            customized function for clean data

        Returns
        -------
        customized function

        """
        self._clean_data_function = clean_data_fun
        return self._clean_data_function

    def clean_data(self, setence_df: pd.DataFrame, **kwargs):
        """
        for nlp clean data,it includ:
        1.remove url
        2.remove puntuation

        Parameters
        ----------

        Returns
        -------
        setence_df with the a new clean sentence without url and puctuation data.
        """
        if not self._clean_data_function:
            setence_df[self._col] = setence_df[self._col].replace('\r', '', regex=True)
            setence_df = setence_df.dropna(subset=[self._col])
            setence_df[self._cleaned_col] = [
                ' '.join(y for y in x.split() if not self.remove_url(y)) for x in setence_df[self._col]]
            setence_df[self._cleaned_col] = setence_df[self._cleaned_col].replace('\n', ' ', regex=True)
            setence_df[self._cleaned_col] = setence_df[self._cleaned_col].apply(self.remove_punctuation)
            setence_df = setence_df.replace(r'^\s*$', np.nan, regex=True)
            setence_df = setence_df.dropna(subset=[self._cleaned_col])
            setence_df.drop_duplicates(subset=[self._cleaned_col], keep='last', inplace=True)
        else:
            self._clean_data_function(setence_df, self._col, self._cleaned_col, **kwargs)
        return setence_df
