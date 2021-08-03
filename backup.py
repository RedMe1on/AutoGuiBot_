import datetime
from typing import Union

import pandas as pd


class Backup:
    """Backup class"""

    def __init__(self):
        self._date = datetime.date.today()
        self._data = False

    def backup_create(self, data: pd, name_backup: str) -> None:
        data.to_pickle(f'backup/backup_{name_backup}_{self._date}.p')

    def backup_load(self, name_backup: str) -> pd:
        return pd.read_pickle(f'backup/backup_{name_backup}_{self._date}.p')

    def backup_check(self, name_backup: str) -> pd:
        try:
            backup = self.backup_load(name_backup)
        except FileNotFoundError:
            backup = None
        return backup

    def _filter_data(self, data: pd, column_merge: str) -> pd:
        common = data.merge(self._data, on=column_merge)
        return data[~data[column_merge].isin(common[column_merge])]

    def merge_data_with_backup(self, column_merge: str, name_backup: str, data: pd) -> pd or False:
        if self.backup_check(name_backup=name_backup):
            data = self._filter_data(data, column_merge)
        else:
            data = False
        return data
