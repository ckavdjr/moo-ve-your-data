import sqlite3


def create_tables():
    conn = sqlite3.connect("farm.db")
    c = conn.cursor()

    q_cows = """
    CREATE TABLE IF NOT EXISTS cows (
        cow_id INTEGER PRIMARY KEY NOT NULL,
        gender CHAR(1) NOT NULL,
        dob DATE NOT NULL,
        colour VARCHAR(20),
        breed VARCHAR(20),
        identification_mark VARCHAR(50)
    );"""

    q_deliveries = """
    CREATE TABLE IF NOT EXISTS deliveries (
        delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
        parent_id INTEGER NOT NULL,
        child_id INTEGER,
        date DATE NOT NULL,
        FOREIGN KEY(parent_id) REFERENCES cows(cow_id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY(child_id) REFERENCES cows(cow_id) ON DELETE CASCADE ON UPDATE CASCADE
    );"""

    q_purchases = """
    CREATE TABLE IF NOT EXISTS purchases (
        purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cow_id INTEGER NOT NULL,
        date DATE NOT NULL,
        amount FLOAT NOT NULL,
        source VARCHAR(50),
        transactor VARCHAR(50),
        insured_amt FLOAT,
        FOREIGN KEY(cow_id) REFERENCES cows(cow_id) ON DELETE CASCADE ON UPDATE CASCADE
    );"""

    q_diseases = """
    CREATE TABLE IF NOT EXISTS diseases (
        disease_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cow_id INTEGER NOT NULL,
        disease VARCHAR(30) NOT NULL,
        date DATE,
        FOREIGN KEY(cow_id) REFERENCES cows(cow_id) ON DELETE CASCADE ON UPDATE CASCADE
    );"""

    q_vaccinations = """
    CREATE TABLE IF NOT EXISTS vaccinations (
        vaccination_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cow_id INTEGER NOT NULL,
        vaccination VARCHAR(30) NOT NULL,
        date DATE NOT NULL,
        FOREIGN KEY(cow_id) REFERENCES cows(cow_id) ON DELETE CASCADE ON UPDATE CASCADE
    );"""

    q_milk = """
    CREATE TABLE IF NOT EXISTS milk (
        milk_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cow_id INTEGER NOT NULL,
        jan FLOAT,
        feb FLOAT,
        mar FLOAT,
        apr FLOAT,
        may FLOAT,
        jun FLOAT,
        jul FLOAT,
        aug FLOAT,
        sep FLOAT,
        oct FLOAT,
        nov FLOAT,
        dec FLOAT,
        FOREIGN KEY(cow_id) REFERENCES cows(cow_id) ON DELETE CASCADE ON UPDATE CASCADE
    );"""

    try:
        c.execute(q_cows)
        c.execute(q_deliveries)
        c.execute(q_purchases)
        c.execute(q_diseases)
        c.execute(q_vaccinations)
        c.execute(q_milk)
        print("Tables created successfully")

    except sqlite3.Error as e:
        print(f"An error {e} occurred")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
