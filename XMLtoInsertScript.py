import xml.etree.ElementTree as ET

def xml_to_sql(xml_file, table_name):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    sql_statements = []
    for record in root.findall(table_name):
        columns = ', '.join(child.tag for child in record)
        values = "', '".join(child.text for child in record)
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ('{values}');"
        sql_statements.append(sql)
    
    return sql_statements

# Example Usage
xml_files = {
    "prescriptions.xml": "Prescription"
}

for file, table in xml_files.items():
    sql_statements = xml_to_sql(file, table)
    with open(f"{table}_insert.sql", "w") as f:
        f.write("\n".join(sql_statements))
