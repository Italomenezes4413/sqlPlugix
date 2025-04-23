import sqlRetiroODBC as sql
from icecream import ic
# get IP of de local machine
# info = sql.informacoesMaquinas()
# info = informacoes.getAllInfo()


sqlServer = sql.SqlServer()
sqlServer.setUser('USERNAME')
sqlServer.setPassword('PASSWORD')
sqlServer.setDatabase('DATABASE')
sqlServer.setServer('SET_YOUR_SERVER_ADRESS')
ic(sqlServer.ifExistTable('TESTE_CRIACAO_TABEL1A'))
stringReturn =sqlServer.createTable('teste_NUMERIC','224434')
ic(stringReturn)
