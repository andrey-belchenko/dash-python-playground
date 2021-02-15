import pyodbc 
import pandas
conn = pyodbc.connect('Driver={SQL Server};Server=192.168.0.115;Database=Ilim.DataMart;UID=conteq;Password=conteq;Trusted_Connection=yes')


sql = "SELECT top 10 * FROM [data].[DimProject]"
data = pandas.read_sql(sql,conn)

print(data)