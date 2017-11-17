# -*- coding: utf-8 -*-
import sys
import logging
import abc
import psycopg2

import ConfigParser
logger = logging.getLogger(__name__)

class ConnectManager:
    _metaclass_ = abc.ABCMeta

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def get_conn(self):
        pass


class MysqlConnectManager():
    
    def __init__(self, host, user, password, database):
        
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connect()

    def connect(self):
        try:
            logger.info("try connect(PostgreSQL) : %s %s", self.host, self.user)
            self.conn = psycopg2.connect(host=self.host, user=self.user,
            password=self.password, database=self.database)
            logger.info("connected(PostgreSQL) : %s, %s", self.host, self.user)

        except Exception as ex:
            logger.error("connect error : %s", ex)
            self.conn.close()

    def get_conn(self):
        return self.conn

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

class MssqlConnectManager():
    
    def __init__(self, host, user, password, database):
        
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connect()

    def connect(self):
        try:
            logger.info("try connect(PostgreSQL) : %s %s", self.host, self.user)
            self.conn = psycopg2.connect(host=self.host, user=self.user,
            password=self.password, database=self.database)
            logger.info("connected(PostgreSQL) : %s, %s", self.host, self.user)

        except Exception as ex:
            logger.error("connect error : %s", ex)
            self.conn.close()

    def get_conn(self):
        return self.conn

    def __del__(self):
        if self.conn is not None:
            self.conn.close()


class PostgreSQLQueryManager():

    def __init__(self, config_path, section):
        config = ConfigParser.ConfigParser()
        config.read(config_path)
        self.mysqlConnectManager = MysqlConnectManager(config.get(section, 'host'), config.get(section, 'user'), 
        config.get(section, 'password'), config.get(section, 'database'))
        self.cursor = self.mysqlConnectManager.get_conn().cursor()

    def selectList(self, query):
        
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert(self, query):

        try:
            cursor = self.cursor()
            with cursor:
                logger.info("insert start")
                cursor.execute(query)
                self.cursor.commit()

            logger.info("insert end")

        except Exception as e:
            logger.error("insert fail %s" % e)

    def __del__(self):
        if self.cursor is not None:
            self.cursor.close()