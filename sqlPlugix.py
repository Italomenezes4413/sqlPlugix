import pyodbc
import mysql.connector as mysql
from datetime import datetime
import socket 
import os
from dotenv import load_dotenv




class SqlServer():
    def __init__(self) -> None:
        self.__connectionString = None
        self.__cursor = None
        self.__portNumber = '1433'
        self.__errorsSqlServer = {
            '08001': 'Connection failure',
            '08004': 'Server rejected the connection',
            '08S01': 'Communication link failure',
            '23000': 'Integrity constraint violation (foreign key, unique constraint, etc.)',
            '42000': 'Syntax error or access violation',
            '42S01': 'Table already exists',
            '42S02': 'Table or view not found',
            '42S22': 'Column not found',
            'HY000': 'General error (catch-all for errors not covered by other codes)',
            '28000': 'Invalid authorization specification (e.g., wrong username or password)',
            'HY001': 'Memory allocation error',
            '22001': 'String data, right-truncated (trying to insert too long value)',
            '22003': 'Numeric value out of range',
            '22007': 'Invalid datetime format',
            '40001': 'Serialization failure (deadlock)',
            'S0002': 'Table or view not found (SQL Server specific)',
            'S1000': 'General error (non-specific error, may vary between drivers)',
        }
        load_dotenv()
        self.setServer()
        self.setDatabase()
        self.setUser()
        self.setPassword()


    #Configuração Conexão
    def setServer(self):
        
        self.__server = os.getenv('SERVER')

    def setUser(self):
        self.__username = os.getenv('USERNAME')

    def setDatabase(self):
        self.__database = os.getenv('DATABASE')
    
    def setPassword(self):
        self.__password = os.getenv('PASSWORD')

    def setCommand(self, command):
        self.__command = command

    #Retornos conexão
    def getValidation(self):
        self.__connectionString = f'DRIVER={{SQL Server}};SERVER={self.__server},{self.__portNumber};DATABASE={self.__database};UID={self.__username};PWD={self.__password}'
        self.__conn = pyodbc.connect(self.__connectionString)
        self.__cursor = self.__conn.cursor()
        self.__cursor.execute(self.__command)
        usuario = self.__cursor.fetchall()
        self.__cursor.close()

        if usuario:
            retornoBanco = usuario[0][0]
            return retornoBanco
        else:
            return False         
        
    def stringPBS(self):
        self.__connectionString = f'DRIVER={{SQL Server}};SERVER={self.__server},{self.__portNumber};DATABASE={self.__database};UID={self.__username};PWD={self.__password}'
        self.__conexao = pyodbc.connect(self.__connectionString)
        cursor = self.__conexao.cursor()
        cursor.execute(self.__command)
        resultado = cursor.fetchall()
        cursor.close()
        
        return resultado

    def stringPBSDicionario(self):
        self.__connectionString = f'DRIVER={{SQL Server}};SERVER={self.__server},{self.__portNumber};DATABASE={self.__database};UID={self.__username};PWD={self.__password}'
        self.__conexao = pyodbc.connect(self.__connectionString)
        cursor = self.__conexao.cursor()
        
        try:
            cursor.execute(self.__command)
            colunas = [col[0] for col in cursor.description]
            resultado = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
        except Exception as e:
            cursor.close()
            raise e
        
        cursor.close()
        return resultado

    
    def insertPBS(self):
        self.__connectionString = f'DRIVER={{SQL Server}};SERVER={self.__server},{self.__portNumber};DATABASE={self.__database};UID={self.__username};PWD={self.__password}'
        self.__conexao = pyodbc.connect(self.__connectionString)
        cursor = self.__conexao.cursor()
        cursor.execute(self.__command)
        cursor.commit()

    
    def ifExistTable (self, nameTable:str):
        self.__connectionString = f'DRIVER={{SQL Server}};SERVER={self.__server},{self.__portNumber};DATABASE={self.__database};UID={self.__username};PWD={self.__password}'
        self.__conexao = pyodbc.connect(self.__connectionString)
        comand = f"select name from sys.tables where name = '{nameTable}'"
        if comand == None:
            return False
        else:
            return True
   

    def createTable(self, nameTable:str, primaryKey):
        self.__connectionString = f'DRIVER={{SQL Server}};SERVER={self.__server},{self.__portNumber};DATABASE={self.__database};UID={self.__username};PWD={self.__password}'
        self.__conexao = pyodbc.connect(self.__connectionString)
        cursor = self.__conexao.cursor()
        
        try:
            cursor.execute(f'CREATE TABLE {nameTable} ({primaryKey} INT IDENTITY(1,1) PRIMARY KEY)')
            cursor.commit()
            cursor.close()
            return {'message':'success'}
        except pyodbc.ProgrammingError as e:
            # check 'SQLServer Erros Dic' at the constructor
            codigoError = e.args[0]
            dicionario = self.__errorsSqlServer[codigoError]
            return {'message':'error', 'info': dicionario}  
            
    
    def addColumnTable(self, nameTable:str , column:str , type:str, size):
        if size == "":
            tamanho = ""
        else:
            tamanho = size
        self.__connectionString = f'DRIVER={{SQL Server}};SERVER={self.__server},{self.__portNumber};DATABASE={self.__database};UID={self.__username};PWD={self.__password}'
        self.__conexao = pyodbc.connect(self.__connectionString)
        cursor = self.__conexao.cursor()
        self.__command = F"""
        ALTER TABLE {nameTable} ADD COLUMN {column} {tamanho} NULL 
                        """
        cursor.execute(self.__command)
        cursor.commit()
        cursor.close()





class MysqlServer():

    def __init__(self) -> None:
        self.__username = None
        self.__password = None
        self.__server = None
        self.__database =None
        self.__command= None
        load_dotenv()
        self.setServer()
        self.setDatabase()
        self.setUser()
        self.setPassword()
        
        
        
    def setServer(self):
        
        self.__server = os.getenv('MYSQLSEVER')

    def setUser(self):
        self.__username = os.getenv('MYSQLUSER')

    def setDatabase(self):
        self.__database = os.getenv('MYSQLDATABASE')
    
    def setPassword(self):
        self.__password = os.getenv('MYSQLPASSWORD')

    def setCommand(self, command):
        self.__command = command


    def stringGLPI(self):
        conexao = mysql.connect(host=f'{self.__server}', database=f'{self.__database}',user=f'{self.__username}', password=f'{self.__password}')
        cursor = conexao.cursor()
        cursor.execute(self.__command)
        retorno = cursor.fetchall()
        if retorno:
            retornoBanco = retorno[0][0]
            return retornoBanco
        else:
            return False


'''
proximas classes e funções para pegar informações da máquinas
importante na geração de logs de usuários e/ou locais de envio de comandos
Serão acrescentadas maiores funcionalidades na biblioteca
'''

class infoMachines():           
    def __init__(self):
        self.__teste = None
        self.__ip = None
    
    def getIp(self):
        '''
        You have to pass first the hostname to get the IP info, ok? Like next sample.
        '''
        hostName = socket.gethostname()
        ip = socket.gethostbyname(hostName)
        
        return ip

    
    def getAllInfo(self):
        hostName = socket.gethostname()
        ip = socket.gethostbyname(hostName)
        data = datetime.now()
        dataForm = data.strftime("%d%m%Y")
        dic = {'ip': ip,'hostname': hostName,'date':dataForm}
        return dic

