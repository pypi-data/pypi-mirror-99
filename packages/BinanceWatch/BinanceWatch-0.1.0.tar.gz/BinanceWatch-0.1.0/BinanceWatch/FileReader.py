import os
import pandas as pd
from pathlib import Path
from typing import List

from BinanceWatch.utils.LoggerGenerator import LoggerGenerator


class FileReader:
    """
    This class will implement the methods to reads the data unavailable with the Binance API.
    As of march 2021, this includes Fiat deposits and withdrawal, direct card purchase and locked stacking
    """
    logger = LoggerGenerator.get_logger('file_reader')

    @staticmethod
    def get_xlsx_files(folder_path: Path) -> List[str]:
        """
        from a folder path, return the names of the xlsx files in this folder

        :param folder_path: path of the folder in with
        :type folder_path: pathlib.Path
        :return: list of file names
        :rtype: List[str]
        """
        try:
            elements = os.listdir(folder_path)
        except FileNotFoundError:
            FileReader.logger.error(f"Unable to find the folder specified: {folder_path}")
            return []
        return [e for e in elements if '.xlsx' in e and os.path.isfile(folder_path / e)]

    @staticmethod
    def get_fiat_deposits(folder_path: Path) -> List[str]:
        """

        :param folder_path:
        :type folder_path:
        :return:
        :rtype:
        """

    @staticmethod
    def get_fiat_withdraws(folder_path: Path):
        withdraws_files = FileReader.get_xlsx_files(folder_path)
        withdraw_df = pd.DataFrame(columns=['withdrawTime', 'Asset', 'Amount', 'Fee'])
        for file in withdraws_files:
            file_df = pd.read_excel(folder_path / file, engine='openpyxl')

