import pandas as pd
import random
from typing import NamedTuple, List

from exceptions import OutOfIndexFromDB


class Name(NamedTuple):
    first_name: str
    last_name: str


class AuthAndCardInfo(NamedTuple):
    email: str
    password: str
    card_number: str
    expires: str
    security_code: str


class AddressInfo(NamedTuple):
    first_name: str
    last_name: str
    contact_number: str
    address_line: str
    town: str
    postcode: str


class CompetitionInfo(NamedTuple):
    page: str
    sizes: List[str]


class DbInfoAccount:
    """get info from file or database for account"""
    db_name = 'db_name.csv'
    db_auth = 'db_auth.csv'
    db_competition = 'db_competition.csv'

    @staticmethod
    def read_file(file: str, encoding='windows-1251', sep=';'):
        """read file with optional encoding and sep"""
        return pd.read_csv(file, encoding=encoding, sep=sep)

    @staticmethod
    def to_csv(data: pd, file_output: str) -> None:
        data.to_csv(file_output, encoding='utf-8-sig', sep=';', index=False)

    def get_first_and_last_name(self) -> Name:
        """Get last and first name to account"""
        name_db = self.read_file(self.db_name)
        first_name = str(name_db.at[random.randint(0, len(name_db)), 'first name'])
        last_name = str(name_db.at[random.randint(0, len(name_db)), 'last name'])
        return Name(first_name=first_name, last_name=last_name)

    def get_competition_info(self, index: int) -> CompetitionInfo:
        """Get info about the competition"""
        competition_db = self.read_file(self.db_competition)
        sizes = competition_db.at[index, 'size'].split(', ')
        return CompetitionInfo(page=str(competition_db.at[index, 'page']), sizes=sizes)


if __name__ == '__main__':
    pk = pd.read_csv('db_auth.csv', encoding='windows-1251', sep=';')
    print(DbInfoAccount().get_competition_info(0).sizes[0])
