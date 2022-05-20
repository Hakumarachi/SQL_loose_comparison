#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : main.py
# Author             : Aku
# Date created       : 20 mai 2022


from rich.console import Console
from rich.table import Table

import pymysql
import sqlite3
import psycopg2

import itertools

value = [
    "True",
    "False",
    "1",
    "0",
    "-1",
    "'1'",
    "'0'",
    "'-1'",
    "''",
    "Null",
    "'John'",
    "'1Jhon'",
    "'0John'",
    "'-1John'",
    "'1e1'",
    "'0e1'",
    "'1e0'",
    "'-1e0'",
    "10",
]


def printTable(title, values):
    table = Table(title=title)
    table.add_column("", justify="center", style="bold")
    for v in value:
        table.add_column(v, justify="center")
    for k in values:
        table.add_row(*([k] + values[k]))
    console = Console()
    console.print(table)


class Connector:
    def __init__(self, db_type):
        self.type = db_type
        if db_type == "sqlite":
            self.conn = Connector.connect_sqlite()
        elif db_type == "postgres":
            self.conn = Connector.connect_postgres()
        elif db_type == "mysql":
            self.conn = Connector.connect_mysql(3308)
        elif db_type == "mariadb":
            self.conn = Connector.connect_mysql(3306)

    @staticmethod
    def connect_sqlite():
        conn = sqlite3.connect('test.db')
        return conn

    @staticmethod
    def connect_mysql(port):
        conn = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='root',
            db='test',
            port=port
        )
        return conn

    @staticmethod
    def connect_postgres():
        connect_str = "dbname='test' user='postgres' host='localhost' " + \
                      "password='root' port='3307'"
        conn = psycopg2.connect(connect_str)
        return conn

    def tests(self):
        dataset = itertools.product(value, repeat=2)
        result = dict()
        for test in dataset:
            query = f"select {test[0]}={test[1]}"
            c = self.conn.cursor()
            try:
                c.execute(query)
                response = c.fetchall()
                for r in response:
                    if r[0] == 1:
                        if test[0] == test[1]:
                            r = '[green]True[/green]'
                        else:
                            r = '[red]True[/red]'
                    elif r[0] == 0:
                        r = 'False'
                    else:
                        r = '[blue]Null[/blue]'
                    if test[0] in result:
                        result[test[0]].append(r)
                    else:
                        result[test[0]] = [r]
            except Exception as e:
                if test[0] in result:
                    result[test[0]].append('[purple]Error[/purple]')
                else:
                    result[test[0]] = ['[purple]Error[/purple]']
            self.conn.commit()
            c.close()

        return result


if __name__ == '__main__':
    db_list = (
        'mariadb',
        'mysql',
        'postgres',
        'sqlite'
    )
    for db_type in db_list:
        db = Connector(db_type)
        result = db.tests()
        printTable(db.type, result)
