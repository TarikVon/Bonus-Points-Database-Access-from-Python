import psycopg2


def connect_to_database(usr, pw, hst, pt, db):
    try:
        connection = psycopg2.connect(user=usr, password=pw, host=hst, port=pt, database=db)
        print("Connected to the database.")
        return connection
    except psycopg2.Error as e:
        print(f"Unable to connect to the database. Error: {e}")
        return None


def truncate_string(s, max_length):
    return (s[: max_length - 3] + "...") if len(s) > max_length else s


def execute_query(connection, query, max_cell_length=30):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        if query.lower().startswith("select"):
            result = cursor.fetchall()
            if result:
                columns = [desc[0] for desc in cursor.description]
                print("\nQuery result:")
                print("|".join(column.ljust(max_cell_length) for column in columns))
                print("-" * (max_cell_length * len(columns) + len(columns) - 1))
                for row in result:
                    formatted_row = [truncate_string(str(cell), max_cell_length).ljust(max_cell_length) for cell in row]
                    print("|".join(formatted_row))
            else:
                print("No data found.")
        else:
            connection.commit()
            print("Query executed successfully.")
    except psycopg2.Error as e:
        print(f"Error executing the query. Error: {e}")


def main():
    connection = connect_to_database("postgres", "159357", "47.236.6.228", "5432", "INFO-210 As3")

    if connection:
        while True:
            print("\nChoose an option:")
            print("1. Run a SQL query")
            print("2. Query all data in a table")
            print("3. Exit")

            choice = input("Enter your choice (1/2/3): ")

            if choice == "1":
                sql_query = input("Enter your SQL query: ")
                execute_query(connection, sql_query)
            elif choice == "2":
                table_name = input("Enter the table name: ")
                query = f"SELECT * FROM {table_name};"
                execute_query(connection, query)
            elif choice == "3":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

        connection.close()


if __name__ == "__main__":
    main()
