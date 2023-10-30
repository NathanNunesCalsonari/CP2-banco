##LINK para o GitHub:  https://github.com/CalinaThalya/T_RHSTU_ENDE_UNIDHOSP.git

# Importe as bibliotecas necessárias
import datetime
import random
import oracledb

# lista de complementos e pontos de referência
complementos = ["predio azul", "Predio Verde", "cobertura", "Fundos", "Bloco A", "Bloco C", "Bloco B"]
pontos_referencia = ["Próximo à escola", "Perto da praça", "Ao lado do hospital", "Em frente à igreja", "Na esquina"]

try:
    # Conecção ao banco de dados Oracle
    db = oracledb.connect(user='rm552539', password='130701', dsn='oracle.fiap.com.br/orcl')
except oracledb.Error as e:
    print(f"Erro ao conectar-se ao banco de dados: {e}")

cursor = db.cursor()

insert_values = []

# Executa consulta para obter os valores de ID_LOGRADOURO
cursor.execute("SELECT ID_LOGRADOURO FROM T_RHSTU_LOGRADOURO")
id_logradouro_values = [row[0] for row in cursor.fetchall()]

# Executa consulta para obter os valores de ID_UNID_HOSPITAL
cursor.execute("SELECT ID_UNID_HOSPITAL FROM T_RHSTU_UNID_HOSPITALAR")
id_unid_hospital_values = [row[0] for row in cursor.fetchall()]

# Certifica de que a sequência está criada no Oracle
# Execute a consulta para obter o próximo valor da sequência
cursor.execute("SELECT Id_unidhosp.nextval FROM dual")
next_id = cursor.fetchone()[0]

for i in range(1, 1001):
    # Certifica de que ID_LOGRADOURO seja um valor válido existente na tabela T_RHSTU_LOGRADOURO
    ID_LOGRADOURO = random.choice(id_logradouro_values)

    # Certifica de que ID_UNID_HOSPITAL seja um valor válido existente na tabela T_RHSTU_UNID_HOSPITALAR
    ID_UNID_HOSPITAL = random.choice(id_unid_hospital_values)

    NR_LOGRADOURO = random.randint(1, 101)
    DS_COMPLEMENTO_NUMERO = random.choice(complementos)
    DS_PONTO_REFERENCIA = random.choice(pontos_referencia)
    DT_INICIO = datetime.date(2022, 1, 1)
    DT_FIM = datetime.date(2023, 8, 31)
    DT_CADASTRO = oracledb.Date.today()
    NM_USUARIO = "USER"

    # Use o próximo ID da sequência
    ID_END_UNIDHOSP = next_id
    next_id += 1  # Atualize o próximo ID

    insert_query = '''
        INSERT INTO T_RHSTU_ENDERECO_UNIDHOSP (
            ID_END_UNIDHOSP,
            ID_UNID_HOSPITAL,
            ID_LOGRADOURO,
            NR_LOGRADOURO,
            DS_COMPLEMENTO_NUMERO,
            DS_PONTO_REFERENCIA,
            DT_INICIO,
            DT_FIM,
            DT_CADASTRO,
            NM_USUARIO
        ) VALUES (
            :1, :2, :3, :4, :5, :6, :7, :8, :9, :10
        )
    '''

    insert_values.append((
        ID_END_UNIDHOSP,
        ID_UNID_HOSPITAL,
        ID_LOGRADOURO,
        NR_LOGRADOURO,
        DS_COMPLEMENTO_NUMERO,
        DS_PONTO_REFERENCIA,
        DT_INICIO,
        DT_FIM,
        DT_CADASTRO,
        NM_USUARIO
    ))

try:
    # Execute a consulta SQL
    cursor.executemany(insert_query, insert_values)
    db.commit()
    if cursor.rowcount > 0:
        print(f"{cursor.rowcount} linhas inseridas com sucesso.") #mensagem que deu certo
    else:
        print("Nenhuma linha foi inserida.")
except oracledb.Error as e:
    print(f"Erro ao inserir dados: {e}")
    db.rollback()  # Reverter a transação em caso de erro
finally:
    cursor.close()
    db.close()
