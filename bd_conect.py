import psycopg2

# Definir os parâmetros de conexão
conn = psycopg2.connect(
    host="database-univesp.chakokagese6.us-east-1.rds.amazonaws.com",
    port="5432",  # Porta padrão do PostgreSQL
    database="bd_SCE",  
    user="pi_univesp",
    password="PIunivesp"
)

# Criar um cursor para executar consultas
cursor = conn.cursor()

# Executar uma consulta
cursor.execute("SELECT * FROM produtos;")

# Obter os resultados
resultados = cursor.fetchall()
resultados
# # Fechar o cursor e a conexão
# cursor.close()
# conn.close()
