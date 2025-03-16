import pyodbc

server = 'SudhirPC\MSSQLSERVER_MK'
database = 'SHSProject'

try:
    connection = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes')
    cursor = connection.cursor()
    print("Database connection successful.\n")

    output_file = "database_report.txt"

    with open(output_file, 'w') as file:
        file.write("====== SHSProject Database Report ======\n\n")

        # Query 1: Retrieve Billing Details
        query1 = """
        SELECT B.Invoice_ID, B.Amount, B.Date_Issued, B.Date_Paid, PS.Status AS Payment_Status
        FROM Billing B
        JOIN Payment_Status PS ON B.Payment_Status_ID = PS.Payment_Status_ID
        WHERE B.Patient_ID = 4;
        """
        cursor.execute(query1)
        results1 = cursor.fetchall()

        file.write("Billing Details\n")
        file.write("Invoice_ID | Amount | Date_Issued | Date_Paid | Payment_Status\n")
        file.write("-" * 60 + "\n")
        for row in results1:
            line = f"{row.Invoice_ID} | {row.Amount} | {row.Date_Issued} | {row.Date_Paid} | {row.Payment_Status}"
            print(line)
            file.write(line + "\n")
        file.write("\n")

        # Query 2: Retrieve Patient's Appointment Details
        query2 = """
        SELECT A.Appointment_ID, P.First_Name, P.Last_Name, D.First_Name AS Doctor_Name, A.Date, A.Time
        FROM Appointment A
        JOIN Patient P ON A.Patient_ID = P.Patient_ID
        JOIN Doctor D ON A.Doctor_ID = D.Doctor_ID
        WHERE A.Patient_ID = 4;
        """
        cursor.execute(query2)
        results2 = cursor.fetchall()

        file.write("Appointment Details\n")
        file.write("Appointment_ID | Patient_Name | Doctor_Name | Date | Time\n")
        file.write("-" * 60 + "\n")
        for row in results2:
            line = f"{row.Appointment_ID} | {row.First_Name} {row.Last_Name} | {row.Doctor_Name} | {row.Date} | {row.Time}"
            print(line)
            file.write(line + "\n")
        file.write("\n")

        # Query 3: Retrieve Patient’s Prescriptions
        query3 = """
        SELECT P.Prescription_ID, M.Medication, M.Dosage, M.Duration, D.First_Name AS Doctor_Name
        FROM Prescription P
        JOIN Medications M ON P.Prescription_ID = M.Prescription_ID
        JOIN Doctor D ON P.Doctor_ID = D.Doctor_ID
        WHERE P.Appointment_ID IN (
            SELECT Appointment_ID FROM Appointment WHERE Patient_ID = 4
        );
        """
        cursor.execute(query3)
        results3 = cursor.fetchall()

        file.write("Prescription Details\n")
        file.write("Prescription_ID | Medication | Dosage | Duration | Doctor_Name\n")
        file.write("-" * 60 + "\n")
        for row in results3:
            line = f"{row.Prescription_ID} | {row.Medication} | {row.Dosage} | {row.Duration} days | {row.Doctor_Name}"
            print(line)
            file.write(line + "\n")
        file.write("\n")

    print("\nReport successfully generated and saved as", output_file)

except Exception as e:
    print("Error connecting to the database:", e)

finally:
    if 'connection' in locals():
        connection.close()
        print("Database connection closed.")
