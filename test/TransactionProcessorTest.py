import unittest
import pandas as pd
from TransactionProcessor import TransactionProcessor

class TransactionProcessorTest(unittest.TestCase):

    def setUp(self):
        data = {
            'InvoiceNo': [1, 2, 3],
            'Quantity': [5, 3, -2],
            'UnitPrice': [10.0, 20.0, 15.0],
            'Country': ['France', 'United Kingdom', 'France'],
            'InvoiceDate': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'Description': ['Product A', 'Product B', 'Product C']
        }
        self.df = pd.DataFrame(data)
        self.processor = TransactionProcessor(self.df)

    def test_calculate_total_amount(self):
        self.processor.calculate_total_amount()
        expected_totals = [50.0, 60.0, -30.0]
        self.assertEqual(list(self.processor.df['TotalAmount']), expected_totals)

    def test_group_by_country(self):
        self.processor.calculate_total_amount()
        result = self.processor.group_by_country()
        expected_result = pd.DataFrame({
            'Country': ['France', 'United Kingdom'],
            'TotalAmount': [20.0, 60.0]
        })
        pd.testing.assert_frame_equal(result, expected_result)

    def test_aggregate_monthly_data(self):
        self.processor.calculate_total_amount()
        result = self.processor.aggregate_monthly_data()
        expected_result = pd.DataFrame({
            'Month': [pd.Period('2024-01')],
            'TotalAmount': [80.0],
            'InvoiceNo': [3]
        })
        pd.testing.assert_frame_equal(result, expected_result)

    def test_calcul_stat_data(self):
        # On vérifie juste que la méthode ne lève pas d'erreur
        try:
            self.processor.calcul_stat_data()
            success = True
        except Exception:
            success = False
        self.assertTrue(success)

    def test_aggregate_world_data(self):
        self.processor.aggregate_world_data()
        self.assertIn('Continent', self.processor.df.columns)

if __name__ == '__main__':
    unittest.main()


