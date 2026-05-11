# 03_Seams.py
# Real-life example: In a logging system, using an interface for loggers allows 
# swapping file loggers for console loggers in tests.

from abc import ABC, abstractmethod

class Logger(ABC):
    @abstractmethod
    def log(self, message):
        pass

class FileLogger(Logger):
    def log(self, message):
        with open("log.txt", "a") as f:
            f.write(message + "\n")

class ConsoleLogger(Logger):
    def log(self, message):
        print(message)

def app_function(logger: Logger):
    logger.log("App started")

# Seam: Inject different loggers
# app_function(FileLogger())  # Production
# app_function(ConsoleLogger())  # Tests

# Real-life example: A database access layer with a seam via dependency injection lets tests use in-memory databases.

class Database:
    def __init__(self, connection):
        self.connection = connection  # Seam

    def save_user(self, user):
        # Simulate save
        self.connection.execute(f"INSERT {user}")

class RealDBConnection:
    def execute(self, query):
        print(f"Executing: {query}")

class InMemoryDBConnection:
    def __init__(self):
        self.data = []

    def execute(self, query):
        self.data.append(query)

# db = Database(RealDBConnection())  # Production
# db = Database(InMemoryDBConnection())  # Tests