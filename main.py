import sqlite3

with sqlite3.connect('medical.db') as connection:
    cursor = connection.cursor()

    create_provider_table_query = '''
    CREATE TABLE IF NOT EXISTS Providers(
    provider_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    specialty_name TEXT,
    phone_number TEXT,
    fax_number TEXT,
    email_address TEXT,
    website TEXT,
    scheduling_type TEXT
    )
    '''

    create_appointment_table_query = '''
    CREATE TABLE IF NOT EXISTS Appointments(
    appointment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    date_time TEXT NOT NULL,
    status TEXT,
    provider_ID,
    location_ID,
    visit_purpose,
    FOREIGN KEY (provider_ID) REFERENCES Providers(provider_ID),
    FOREIGN KEY (location_ID) REFERENCES Locations(location_ID),
    FOREIGN KEY (visit_purpose) REFERENCES Visit_Purpose(visit_purpose)
    )
    ''' 

    create_locations_table_query = '''
    CREATE TABLE IF NOT EXISTS Locations(
    location_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    address_row_1 TEXT,
    address_row_2 TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    travel_time_from_home_location REAL,
    travel_time_from_work_location REAL
    )
    '''

    create_visit_purpose_table_query = '''
    CREATE TABLE IF NOT EXISTS Visit_Purpose(
    visit_purpose TEXT PRIMARY KEY,
    appointment_frequency INTEGER,
    scheduling_reminder_needed INTEGER,
    scheduling_reminder_lead_time INTEGER,
    visit_duration INTEGER
    )
    '''

    cursor.execute(create_locations_table_query)
    cursor.execute(create_visit_purpose_table_query)
    cursor.execute(create_provider_table_query)
    cursor.execute(create_appointment_table_query)

    connection.commit()

