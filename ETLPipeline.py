from DataCleaner import DataCleaner
import pandas as pd
from TransactionProcessor import TransactionProcessor
import logging
class ETLPipeline:
    def __init__(self, df):
        self.df = df
   
    def run_pipeline(self):
        """Exécute l’ensemble du processus ETL."""
        supplier_df=pd.read_csv('Supplier.csv')
        cleaner = DataCleaner(self.df)
        cleaner.remove_duplicates()
        cleaner.handle_missing_values()
        cleaner.filter_valid_transactions()

        processor = TransactionProcessor(cleaner.df)
        processor.calculate_total_amount()
        processor.group_by_country()
        processor.aggregate_monthly_data()
        processor.calcul_stat_data()
        processor.aggregate_world_data()
        return processor.df

    def save_as_parquet(self, path: str):

        """
        Enregistre le DataFrame final sous forme de fichier Parquet.
        """
        if self.df is not None:
            self.df["StockCode"] = self.df["StockCode"].astype(str)
            self.df.to_parquet(path, index=False)
            logging.info(f" Données sauvegardées en Parquet : {path}")
        else:
            logging.warning(" Aucune donnée à sauvegarder !")

