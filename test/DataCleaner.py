import pandas as pd
import logging

# Configurer les logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataCleaner:
    def __init__(self, df):
        self.df = df
        logging.info("DataCleaner initialisé avec un DataFrame de %d lignes et %d colonnes", df.shape[0], df.shape[1])

    def remove_duplicates(self):
        """Supprime les lignes dupliquées."""
        initial_rows = self.df.shape[0]
        self.df = self.df.drop_duplicates()
        final_rows = self.df.shape[0]
        num_row=initial_rows -  final_rows
        logging.info("le nombre des doublons aprés le traitement  : %s", num_row)

    def handle_missing_values(self):

        """
        Gère les valeurs manquantes sur des colonnes critiques.
        Remplit ou supprime les valeurs manquantes en fonction du type de la colonne.
        """
        missing_before = self.df.isnull().sum().sum()
    # Gérer les valeurs manquantes pour des colonnes spécifiques
        self.df = self.df.dropna(subset=['CustomerID', 'InvoiceNo', 'StockCode'])
        self.df.loc[:, 'Description'] = self.df['Description'].fillna('Inconnu')
        self.df.loc[:, 'Quantity'] = self.df['Quantity'].fillna(self.df['Quantity'].median())
        self.df.loc[:, 'UnitPrice'] = self.df['UnitPrice'].fillna(self.df['UnitPrice'].mean())
        self.df.loc[:, 'Country'] = self.df['Country'].fillna(self.df['Country'].mode()[0])

        missing_after = self.df.isnull().sum().sum()
        num= missing_before  - missing_after
        logging.info("Valeurs manquantes sup aprés le traitement   :%s", num)
        return self.df
   
    #méthode pour garder que les transactions non annulées
    def filter_valid_transactions(self):
        init_count = len(self.df) # compter le nombre de ligne avant suppression pour comparer dans les logs
        self.df = self.df[~self.df['InvoiceNo'].astype(str).str.startswith('C')]         #suppression de toutes transaction qui commence par 'C'
        logging.info(f"{init_count - len(self.df)} transaction annulées supprimées! ")
 
        return self.df
