import pandas as pd
import logging
import country_continent_mapping
# Configurer les logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TransactionProcessor:
    def __init__(self, df):
        self.df = df
        logging.info("TransactionProcessor initialisé avec un DataFrame de forme %s", df.shape)
    

    def calculate_total_amount(self):
        """Ajoute une colonne TotalAmount (Quantity * UnitPrice)."""
        try: 
            self.df['TotalAmount'] = self.df['Quantity'] * self.df['UnitPrice']
            logging.info("Colonne 'TotalAmount' calculée et ajoutée au DataFrame.")
        except Exception as e:
            logging.error("Erreur lors du calcul de 'TotalAmount' : %s", e)


    def group_by_country(self):
        """Regroupe les transactions par pays et calcule le total des montants."""
        try:
            result = self.df.groupby('Country')['TotalAmount'].sum().reset_index()
            logging.info("Regroupement par pays effectué avec succès.")
            return result
        except Exception as e:
            logging.error("Erreur lors du regroupement par pays : %s", e)

        

    def aggregate_monthly_data(self):
        """Calcule des statistiques mensuelles."""
        try:
            self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'])
            self.df['Month'] = self.df['InvoiceDate'].dt.to_period('M')
            result =self.df.groupby('Month').agg({'TotalAmount': 'sum', 'InvoiceNo': 'count'}).reset_index()
            logging.info("Agrégation mensuelle des données réussie.")
            return result
        except Exception as e : 
            logging.error("Erreur lors de l'agrégation mensuelle des données : %s", e)


    

    def calcul_stat_data(self):
       
        try:
    # Filtrer les transactions en France
            france_df = self.df[self.df['Country'] == 'France'].copy()


    # Ajouter une colonne 'TotalRevenue'
            france_df['TotalRevenue'] = france_df['Quantity'] * france_df['UnitPrice']
    
    # Trouver le produit avec le plus de gains
            top_product = (
        france_df.groupby('Description')['TotalRevenue']
        .sum()
        .idxmax()
    )
            top_product_revenue = france_df.groupby('Description')['TotalRevenue'].sum().max()
    
    # Analyser l'heure avec le plus de transactions
            self.df['InvoiceDate'] = pd.to_datetime(self.df['InvoiceDate'])
            self.df['Hour'] = self.df['InvoiceDate'].dt.hour
    
            busiest_hour = (
            self.df.groupby('Hour')['InvoiceNo']
            .count()
            .idxmax()
                         )
            max_transactions = self.df.groupby('Hour')['InvoiceNo'].count().max()
    
    # Afficher les résultats
            print(f"Produit le plus rentable en France : {top_product} avec {top_product_revenue:.2f}€ de gains")
            print(f"Heure avec le plus de transactions : {busiest_hour}h avec {max_transactions} transactions")
            logging.info("Statistiques des transactions françaises calculées avec succès.")
            logging.info("Produit le plus rentable : %s avec %.2f€ de gains", top_product, top_product_revenue)
            logging.info("Heure la plus chargée : %dh avec %d transactions", busiest_hour, max_transactions)
        except Exception as e:
            logging.error("Erreur lors du calcul des statistiques des transactions françaises : %s", e)

    def aggregate_supplier_data(self,supplier_df):
        try:
                # Fusionner les dataframes sur 'InvoiceNo'
            merged_df = pd.merge(self.df, supplier_df, on='InvoiceNo',how='left')
            

    # Filtrer les transactions annulées
            merged_df = merged_df[merged_df['Quantity'] > 0]

    # Calculer le total des ventes par fournisseur
            supplier_sales = (
            merged_df.groupby('Fournisseur')['Quantity']
            .sum()
            .reset_index()
            .sort_values(by='Quantity', ascending=False)
              )

    # Filtrer pour l'année 2011 et le Royaume-Uni
            uk_2011_df = merged_df[(merged_df['InvoiceDate'].dt.year == 2011) & (merged_df['Country'] == 'United Kingdom')]
            uk_2011_supplier_sales = (
            uk_2011_df.groupby('Fournisseur')['Quantity']
            .sum()
            .reset_index()
            .sort_values(by='Quantity', ascending=False)
        )

    # Afficher les résultats
            print("Classement des fournisseurs selon le total des ventes :")
            print(supplier_sales)
            print("\nClassement des fournisseurs en 2011 pour le Royaume-Uni :")
            print(uk_2011_supplier_sales)
           
            logging.info("Agrégation des données fournisseurs réussie.")
            logging.info("Classement des fournisseurs selon le total des ventes :")
            logging.info("%s", supplier_sales)
            logging.info("Classement des fournisseurs en 2011 pour le Royaume-Uni :")
            logging.info("%s", uk_2011_supplier_sales)
        

        except Exception as e : 
            logging.error("Erreur lors de l'agrégation des données fournisseurs : %s", e)







    def aggregate_world_data(self):
   
        mapping_df = pd.DataFrame(list(country_continent_mapping.items()), columns=['Country', 'Continent'])
        

    # Fusionner le DataFrame des transactions avec le mapping des continents
        self.df = self.df.merge(mapping_df, left_on='Country', right_on='Country', how='left')
        logging.info("Fusion des données avec le mapping des continents terminée")

    # Calculer le montant total par transaction
        self.df['TotalAmount'] = self.df['Quantity'] * self.df['UnitPrice']
        logging.info("Calcul du montant total des transactions effectué")

    # Filtrer les opérations valides (montant positif)
        valid_sales = self.df[self.df['TotalAmount'] > 0]
        logging.info("Filtrage des ventes valides : %d lignes restantes", len(valid_sales))


    # Classer les continents selon les dépenses totales
        continent_sales = valid_sales.groupby('Continent')['TotalAmount'].sum().reset_index()
        continent_sales = continent_sales.sort_values(by='TotalAmount', ascending=False)
        logging.info("Classement des continents par dépenses effectué")
    # Identifier le continent avec le plus d’opérations annulées (quantité négative)
        cancelled_transactions = self.df[self.df['Quantity'] < 0]
        continent_cancellations = cancelled_transactions['Continent'].value_counts().reset_index()
        continent_cancellations.columns = ['Continent', 'CancelledTransactions']
        logging.info("Identification des annulations par continent terminée")


    # Résultats
        logging.info("Classement des continents par dépenses :\n%s", continent_sales)
        logging.info("Continent avec le plus d'opérations annulées :\n%s", continent_cancellations)
        return continent_sales, continent_cancellations




    