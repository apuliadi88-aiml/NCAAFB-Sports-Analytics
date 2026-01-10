from sqlalchemy import text

def save_csv(df, filename):
    df.to_csv(f"data/{filename}.csv", index=False)

def save_to_postgres(df, table_name, engine, if_exists='append'):
    df.to_sql(table_name, con=engine, if_exists=if_exists, index=False, method='multi')

def create_table_postgres(query, engine):
    with engine.connect() as conn:
        conn.execute(text(query))
        conn.commit()



