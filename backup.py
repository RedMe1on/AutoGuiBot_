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

    def backup_check(self, name_backup: str, backup_empty_default: pd) -> pd:
        try:
            backup = self.backup_load(name_backup)
        except FileNotFoundError:
            backup = backup_empty_default
        return backup

    @staticmethod
    def filter_data(data: pd, backup_data: pd, column_merge: str) -> pd:
        common = data.merge(backup_data, on=column_merge)
        return data[~data[column_merge].isin(common[column_merge])]


