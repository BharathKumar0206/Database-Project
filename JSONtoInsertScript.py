import json

def json_to_sql(json_file, table_name):
    with open(json_file, "r") as file:
        data = json.load(file)
    
    sql_statements = []
    for record in data:
        columns = ', '.join(record.keys())
        values = "', '".join(str(value) for value in record.values())
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ('{values}');"
        sql_statements.append(sql)
    
    return sql_statements

# Example Usage
json_files = {
    "appointments.json": "Appointment",
    "lab_results.json": "Lab_Test"
}

for file, table in json_files.items():
    sql_statements = json_to_sql(file, table)
    with open(f"{table}_insert.sql", "w") as f:
        f.write("\n".join(sql_statements))
