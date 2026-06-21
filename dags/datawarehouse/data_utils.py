from airflow.providers.postgres.hooks.postgres import PostgresHook

from psycopg2.extras import RealDictCursor

table = "yt_api"

#----------------------------------------------------------------------------
def get_conn_cursor():
    """
    Establishes a connection to the PostgreSQL database and returns a cursor.
    
    Returns:
        cursor: A RealDictCursor for executing SQL queries.
    """
    # Create a PostgresHook instance using the connection ID defined in Airflow
    hook = PostgresHook(postgres_conn_id="postgres_db_yt_elt", database="elt_db")
    
    # Get a connection from the hook
    conn = hook.get_conn()
    
    # Create and return a RealDictCursor for executing SQL queries
    cur =  conn.cursor(cursor_factory=RealDictCursor) 
    
    # Create and return a RealDictCursor for executing SQL queries
    return conn, cur  

    
    
#----------------------------------------------------------------------------    
def close_conn_cursor(cur, conn):
    cur.close()
    conn.close() 

#----------------------------------------------------------------------------    
def create_schema(schema):
    """
    Creates a schema in the PostgreSQL database if it does not already exist.
    
    Args:
        schema (str): The name of the schema to be created.
    """
    conn, cur = get_conn_cursor()
    
    # Execute the SQL command to create the schema if it does not exist
    schema_sql = (f"CREATE SCHEMA IF NOT EXISTS {schema};")
    
    cur.execute(schema_sql)
    
    # Commit the transaction to save changes to the database
    conn.commit()
    
    # Close the cursor and connection
    close_conn_cursor(cur, conn)
  
#----------------------------------------------------------------------------    
def create_table(schema):
    """
    Creates a table in the PostgreSQL database if it does not already exist.
    
    Args:
        table (str): The name of the table to be created.
    """
    conn, cur = get_conn_cursor()
    
    # Execute the SQL command to create the table if it does not exist
    if schema == "staging":
        table_sql  = f"""
                CREATE TABLE IF NOT EXISTS {schema}.{table} (
                    "Video_ID" VARCHAR(11) NOT NULL PRIMARY KEY,
                    "Video_Title" TEXT NOT NULL,
                    "Upload_Date" TIMESTAMP NOT NULL,
                    "Duration" VARCHAR(20) NOT NULL,
                    "Video_Views" INTEGER,
                    "Likes_Count" INTEGER,
                    "Comments_Count" INTEGER
                );    
            """
    else:   
        table_sql = f"""
                CREATE TABLE IF NOT EXISTS {schema}.{table} (
                    "Video_ID" VARCHAR(11) NOT NULL PRIMARY KEY,
                    "Video_Title" TEXT NOT NULL,
                    "Upload_Date" TIMESTAMP NOT NULL,
                    "Duration" VARCHAR(20) NOT NULL,
                    "Video_Type" VARCHAR(10) NOT NULL,
                    "Video_Views" INTEGER,
                    "Likes_Count" INTEGER,
                    "Comments_Count" INTEGER
                );    
            """
    
    cur.execute(table_sql)
    
    # Commit the transaction to save changes to the database
    conn.commit()
    
    # Close the cursor and connection
    close_conn_cursor(cur, conn)   
    
  
#----------------------------------------------------------------------------  
def get_video_ids(cur, schema):
    """
    Retrieves a list of video IDs from the specified schema and table.
    
    Args:
        cur: A cursor for executing SQL queries.
        schema (str): The name of the schema from which to retrieve video IDs.
    
    Returns:
        list: A list of video IDs retrieved from the database.
    """
    # Execute the SQL command to select video IDs from the specified schema and table
    cur.execute(f"SELECT \"Video_ID\" FROM {schema}.{table};")
    
    # Fetch all results and extract video IDs into a list
    ids = cur.fetchall()
    
    video_ids = [row["Video_ID"] for row in ids]
    
    return video_ids