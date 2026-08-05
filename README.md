# :dna: Healthcare_Data_Engineering :dna:
Practicing the ETL process We're extracting a dummy dataset made by Prasad Patil, available on Kaggle. We'll clean it using SQL and Python before storing it in a PostgreSQL Docker container.  The goal is to present the data in an easy-to-read format so it can be utilized for a data visualization dashboard (Like Tableau or PowerBi) with ease. 

## :bookmark_tabs: Table of Contents :bookmark_tabs:
-Issue 01: [Pipeline](./pipeline_setup.md) | ETL Pipeline: Extract from Kaggle, Transform with Python/Jupyter/Pandas, Load into Postgre Container with SQLAlchemy/Psycopg

-Issue 02: Orchestration | Coming Soon!

-Issue 03: Cloud Storage | Coming Soon!

-Issue 04: Data Warehouse | Coming Soon!

## :bar_chart: ER Diagram :bar_chart:
<img width="3141" height="6490" alt="image" src="https://github.com/user-attachments/assets/d6cc9ae4-e41b-4cac-8c7d-4ed4348cdd9b" />

The Entity Relationship, or ER Diagram, is used to represent the relational schema and display the relationship between each table. We can use it to also display the primary and foreign keys.  From here, we can get a clear picture on how we want to structure our data.  We utilized third form normalization to ensure each attribute is atomic and cannot be simplified further. 
 


