import unittest
import pandas as pd
from DataCleaner import DataCleaner  # Assure-toi que le fichier s'appelle data_cleaner.py

class TestDataCleaner(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            'CustomerID': [1, 2, None, 4],
            'InvoiceNo': ['12345', 'C12346', '12347', '12348'],
            'StockCode': ['A001', 'A002', None, 'A004'],
            'Description': ['Produit A', None, 'Produit C', 'Produit D'],
            'Quantity': [10, 20, None, 40],
            'UnitPrice': [5.0, None, 15.0, 20.0],
            'Country': ['France', None, 'Allemagne', 'Espagne']
        })
        self.cleaner = DataCleaner(self.df)

    def test_remove_duplicates(self):
        df_test = pd.DataFrame({'A': [1, 2, 2, 3], 'B': [4, 5, 5, 6]})
        cleaner = DataCleaner(df_test)
        cleaner.remove_duplicates()
        self.assertEqual(len(cleaner.df), 3)

    def test_handle_missing_values(self):
        cleaned_df = self.cleaner.handle_missing_values()
        self.assertFalse(cleaned_df[['CustomerID', 'InvoiceNo', 'StockCode']].isnull().any().any())
        self.assertFalse(cleaned_df['Description'].isnull().any())
        self.assertFalse(cleaned_df['Quantity'].isnull().any())
        self.assertFalse(cleaned_df['UnitPrice'].isnull().any())
        self.assertFalse(cleaned_df['Country'].isnull().any())

    def test_filter_valid_transactions(self):
        cleaned_df = self.cleaner.filter_valid_transactions()
        self.assertFalse(cleaned_df['InvoiceNo'].str.startswith('C').any())

if __name__ == '__main__':
    unittest.main()

# Tu peux exécuter ce fichier avec `python -m unittest test_data_cleaner.py` ! 🎯
# Tu en penses quoi ? Tu veux que j'ajoute d'autres cas de test ou des vérifications supplémentaires ?
