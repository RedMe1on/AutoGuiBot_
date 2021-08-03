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
    db_accounts = 'db_accounts.csv'
    db_address = 'db_address.csv'
    db_competition = 'db_competition.csv'

    @staticmethod
    def read_file(file: str, encoding='windows-1251', sep=';'):
        """read file with optional encoding and sep"""
        return pd.read_csv(file, encoding=encoding, sep=sep)

    def get_first_and_last_name(self) -> Name:
        """Get last and first name to account"""
        name_db = self.read_file(self.db_name)
        first_name = str(name_db.at[random.randint(0, len(name_db)), 'first name'])
        last_name = str(name_db.at[random.randint(0, len(name_db)), 'last name'])
        return Name(first_name=first_name, last_name=last_name)

    def get_auth_info_with_card(self, index: int) -> AuthAndCardInfo:
        """Get email, password and card info"""
        auth_db = self.read_file(self.db_auth)
        if index <= len(auth_db):
            return AuthAndCardInfo(email=str(auth_db.at[index, 'email']), password=str(auth_db.at[index, 'password']),
                                   card_number=str(auth_db.at[index, 'card_number'][1:]),
                                   expires=str(auth_db.at[index, 'expires'][1:]),
                                   security_code=str(auth_db.at[index, 'security_code'][1:]))
        else:
            raise OutOfIndexFromDB('Индекс превышает значения строк в таблице')

    def get_address(self, index: int) -> AddressInfo:
        """Get address info"""
        address_db = self.read_file(self.db_address)
        if index <= len(address_db):
            return AddressInfo(first_name=str(address_db.at[index, 'first_name']),
                               last_name=str(address_db.at[index, 'last_name']),
                               contact_number=str(address_db.at[index, 'contact_number']),
                               address_line=str(address_db.at[index, 'address_line']),
                               town=str(address_db.at[index, 'town']), postcode=str(address_db.at[index, 'postcode']))
        else:
            raise OutOfIndexFromDB('Индекс превышает значения строк в таблице')

    def get_competition_info(self, index: int) -> CompetitionInfo:
        """Get info about the competition"""
        competition_db = self.read_file(self.db_competition)
        sizes = competition_db.at[index, 'size'].split(', ')
        return CompetitionInfo(page=str(competition_db.at[index, 'page']), sizes=sizes)


if __name__ == '__main__':
    pk = pd.read_csv('db_auth.csv', encoding='windows-1251', sep=';')
    print(DbInfoAccount().get_competition_info(0).sizes[0])
