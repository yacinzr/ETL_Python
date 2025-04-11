import pandas as pd
from ETLPipeline import ETLPipeline
import logging
if __name__ == "__main__":

    # Charger les données
    df = pd.read_excel("Online Retail.xlsx")
    logging.info("Début du chargement des données depuis le fichier Excel...")
 
    # Exécuter le pipeline ETL
    logging.info("Début de l'exécution du pipeline ETL...")

    pipeline = ETLPipeline(df)
    cleaned_df = pipeline.run_pipeline()
    logging.info("Pipeline ETL exécuté avec succès....")
    print(cleaned_df.head())
    output_file = "onlineRetail_cleaned.parquet"
    pipeline.df = cleaned_df  
    pipeline.save_as_parquet(output_file)
    logging.info(f"Données sauvegardées avec succès sous le nom de fichier : {output_file}")


