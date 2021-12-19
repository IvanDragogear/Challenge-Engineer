#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
import datetime


DB_PATH = os.getcwd() + "/database.db"
RED = "\033[31m"
CYAN = "\033[96m"
BOLD = "\033[1m"
CEND = "\033[0m"


def create_initial_tables(cursor, connection):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS AEROLINIAS (
        ID_AEROLINEA INT PRIMARY KEY NOT NULL,
        NOMBRE_AEROLINIA TEXT NOT NULL
    );""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS AEROPUERTOS (
        ID_AEROPUERTO INT PRIMARY KEY NOT NULL,
        NOMBRE_AEROPUERTO TEXT NOT NULL
    );""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS MOVIMIENTOS (
        ID_MOVIMIENTO INT PRIMARY KEY NOT NULL,
        DESCRIPCION TEXT NOT NULL
    );""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS VUELOS (
        ID_VUELO INT PRIMARY KEY NOT NULL,
        ID_AEROLINEA INT NOT NULL,
        ID_AEROPUERTO INT NOT NULL,
        ID_MOVIMIENTO INT NOT NULL,
        DIA DATE NOT NULL,
        FOREIGN KEY (ID_AEROLINEA)
            REFERENCES AEROLINIAS(ID_AEROLINEA),
        FOREIGN KEY (ID_AEROPUERTO)
            REFERENCES AEROPUERTOS(ID_AEROPUERTO),
        FOREIGN KEY (ID_MOVIMIENTO )
            REFERENCES MOVIMIENTOS(ID_MOVIMIENTO)
    );""")


def insert_data(cursor, connection):
    cursor.execute("""
    INSERT INTO
        AEROLINIAS (ID_AEROLINEA, NOMBRE_AEROLINIA)
        VALUES
            (1, 'Volaris'),
            (2, 'Aeromar'),
            (3, 'Interjet'),
            (4, 'Aeromexico')
        ;""")
    cursor.execute("""
    INSERT INTO
        AEROPUERTOS (ID_AEROPUERTO, NOMBRE_AEROPUERTO)
        VALUES
            (1, 'Benito Juarez'),
            (2, 'Guanajuato'),
            (3, 'La paz'),
            (4, 'Oaxaca')
        ;""")
    cursor.execute("""
    INSERT INTO
        MOVIMIENTOS (ID_MOVIMIENTO, DESCRIPCION)
        VALUES
            (1, 'Salida'),
            (2, 'Llegada')
        ;""")
    cursor.execute("""
    INSERT INTO
        VUELOS (ID_VUELO, ID_AEROLINEA, ID_AEROPUERTO, ID_MOVIMIENTO, DIA)
        VALUES
            (1, 1, 1, 1, '2021-05-02'),
            (2, 2, 1, 1, '2021-05-02'),
            (3, 3, 2, 2, '2021-05-02'),
            (4, 4, 3, 2, '2021-05-02'),
            (5, 1, 3, 2, '2021-05-02'),
            (6, 2, 1, 1, '2021-05-02'),
            (7, 2, 3, 1, '2021-05-04'),
            (8, 3, 4, 1, '2021-05-04'),
            (9, 3, 4, 1, '2021-05-04')
        ;""")
    connection.commit()


# 1. ¿Cuál es el nombre aeropuerto que ha tenido mayor movimiento durante el año?
def get_busiest_airport(cursor):
    # Selects IDs with the highest number of flights
    cursor.execute("""
    SELECT ID_AEROPUERTO, Total
    FROM (SELECT ID_AEROPUERTO, COUNT(ID_AEROPUERTO) AS Total
            FROM VUELOS
            GROUP BY  ID_AEROPUERTO
            ORDER BY Total DESC)
    WHERE Total = (
        SELECT MAX(Total)
            FROM (SELECT ID_AEROPUERTO, COUNT(ID_AEROPUERTO) AS Total
                    FROM VUELOS
                    GROUP BY  ID_AEROPUERTO
                    ORDER BY Total DESC))
    ;""")
    # Separates the IDs with the highest number of flights
    id_busiest_airport_list = []
    for i in cursor:
        id_busiest_airport_list.append(i[0])
    # Select the names of the airports
    cursor.execute("""
    SELECT DISTINCT AEROPUERTOS.NOMBRE_AEROPUERTO
    FROM VUELOS INNER JOIN AEROPUERTOS
        ON VUELOS.ID_AEROPUERTO = AEROPUERTOS.ID_AEROPUERTO
    WHERE VUELOS.ID_AEROPUERTO in {}
    ;""".format(str(tuple(id_busiest_airport_list))))

    return cursor.fetchall()


# 2. ¿Cuál es el nombre aerolínea que ha realizado mayor número de vuelos durante el año?
def get_busiest_airline(cursor):
    # Selects IDs with the highest number of movements
    cursor.execute("""
    SELECT ID_AEROLINEA, Total
    FROM (SELECT ID_AEROLINEA, COUNT(ID_AEROLINEA) AS Total
            FROM VUELOS
            GROUP BY  ID_AEROLINEA
            ORDER BY Total DESC)
    WHERE Total = (
        SELECT MAX(Total)
            FROM (SELECT ID_AEROLINEA, COUNT(ID_AEROLINEA) AS Total
                    FROM VUELOS
                    GROUP BY  ID_AEROLINEA
                    ORDER BY Total DESC))
    ;""")
    # Separates the IDs with the highest number of movements
    id_busiest_airport_list = []
    for i in cursor:
        id_busiest_airport_list.append(i[0])
    # Select the names of the airlines
    cursor.execute("""
    SELECT DISTINCT AEROLINIAS.NOMBRE_AEROLINIA
    FROM VUELOS INNER JOIN AEROLINIAS
        ON VUELOS.ID_AEROLINEA = AEROLINIAS.ID_AEROLINEA
    WHERE VUELOS.ID_AEROLINEA in {}
    ;""".format(str(tuple(id_busiest_airport_list))))

    return cursor.fetchall()


# 3. ¿En qué día se han tenido mayor número de vuelos?
def get_date_with_more_flights(cursor):
    # This selects the dates with the highest number of movements.
    cursor.execute("""
    SELECT DIA, Total
    FROM (SELECT DIA, COUNT(DIA) AS Total
            FROM VUELOS
            GROUP BY  DIA
            ORDER BY Total DESC)
    WHERE Total = (
        SELECT MAX(Total)
            FROM (SELECT DIA, COUNT(DIA) AS Total
                    FROM VUELOS
                    GROUP BY  DIA
                    ORDER BY Total DESC))
    ;""")
    return cursor.fetchall()


# 4. ¿Cuáles son las aerolíneas que tienen más de 2 vuelos por día?
def get_airlines_moviemots_greater_than_two(cursor):
    cursor.execute("""
    SELECT ID_AEROLINEA
        FROM
            (SELECT ID_AEROLINEA, DIA FROM VUELOS
            WHERE ID_AEROLINEA IN (
                SELECT ID_AEROLINEA
                FROM VUELOS
                GROUP BY ID_AEROLINEA
                HAVING COUNT(*) > 2
            )
            ORDER BY ID_AEROLINEA)
    GROUP BY ID_AEROLINEA
    HAVING COUNT(*) > 2
    ;""")

    # Separates the IDs with the highest number of movements
    id_busiest_airport_list = []
    for i in cursor:
        id_busiest_airport_list.append(i[0])
    # Select the names of the airlines
    cursor.execute("""
    SELECT DISTINCT AEROLINIAS.NOMBRE_AEROLINIA
    FROM VUELOS INNER JOIN AEROLINIAS
        ON VUELOS.ID_AEROLINEA = AEROLINIAS.ID_AEROLINEA
    WHERE VUELOS.ID_AEROLINEA in {}
    ;""".format(str(tuple(id_busiest_airport_list))))
    return cursor.fetchall()


def run():
    print(DB_PATH)
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    create_initial_tables(cursor, connection)
    try:
        insert_data(cursor, connection)
    except Exception as e:
        print("Warnning:", e)

    print(RED + "\n\nSQL" + CEND)
    print(CYAN + "\n\n1. ¿Cuál es el nombre aeropuerto que ha tenido mayor movimiento durante el año?" + CEND)
    print(get_busiest_airport(cursor))
    print(CYAN + "\n\n2. ¿Cuál es el nombre aerolínea que ha realizado mayor número de vuelos durante el año?" + CEND)
    print(get_busiest_airline(cursor))
    print(CYAN + "\n\n3. ¿En qué día se han tenido mayor número de vuelos?" + CEND)
    print(get_date_with_more_flights(cursor))
    print(CYAN + "\n\n4. ¿Cuáles son las aerolíneas que tienen más de 2 vuelos por día" + CEND)
    print(get_airlines_moviemots_greater_than_two(cursor))
    connection.close()
