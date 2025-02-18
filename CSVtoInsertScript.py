import pandas as pd
def csv_to_sql(csv_file, table_name):
    df = pd.read_csv(csv_file)
    sql_statements = []
    
    for _, row in df.iterrows():
        values = "', '".join(str(value) for value in row.values)
        sql = f"INSERT INTO {table_name} VALUES ('{values}');"
        sql_statements.append(sql)
    
    return sql_statements

# Example Usage
tables = {
    "patients.csv": "Patient",
    "doctors.csv": "Doctor",
    "billing.csv": "Billing"
}

for file, table in tables.items():
    sql_statements = csv_to_sql(file, table)
    with open(f"{table}_insert.sql", "w") as f:
        f.write("\n".join(sql_statements))
