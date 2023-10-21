import os
import mysql.connector
from dotenv import load_dotenv


class ConnectionManager:
    _DOTENV_PATH = "server/.env"
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConnectionManager, cls).__new__(cls)
            cls._instance.init()
        return cls._instance


    def init(self):
        # Load environment variables from .env file
        load_dotenv(dotenv_path=ConnectionManager._DOTENV_PATH)

        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_DATABASE")

        self.connection = None


    def connect(self):
        if self.connection is None:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected to the database")
        else:
            print("Connection already established")


    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None


def get_connection():
    manager = ConnectionManager()
    manager.connect()
    return manager.connection
