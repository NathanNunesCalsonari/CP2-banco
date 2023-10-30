##LINK para o GitHub: https://github.com/CalinaThalya/T_RHSTU_PACIENTE.git
# Importando os módulos necessários
import oracledb
import random
import string
import datetime

# Função para gerar um CPF válido aleatório
def generate_cpf():
    # Gerando nove dígitos aleatórios
    cpf = ''.join(random.choices(string.digits, k=9))
    cpf = '1' + cpf  # Adicionando o prefixo "1" para garantir validade
    cpf_list = [int(digit) for digit in cpf]
    for _ in range(2):
        val = sum([(i + 1) * cpf_list[i] for i in range(9)]) % 11
        cpf_list.append(val if val < 10 else 0)
    return ''.join(map(str, cpf_list))

# Função para gerar um nome aleatório
def generate_name():
    length = random.randint(5, 10)  # Gerando um comprimento aleatório entre 5 e 10
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

# Função para gerar uma data de nascimento aleatória
def generate_birthdate():
    # Definindo a faixa de datas de nascimento
    start_date = datetime.date(1950, 1, 1)
    end_date = datetime.date(2005, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + datetime.timedelta(days=random_days)

# Função para gerar dados fictícios
def generate_data():
    # Chamando as funções para gerar os dados
    nm_paciente = generate_name()
    nr_cpf = generate_cpf()
    nm_rg = generate_name()
    dt_nascimento = generate_birthdate()
    fl_sexo_biologico = random.choice(['M', 'F'])  # Escolhendo aleatoriamente entre masculino (M) e feminino (F)
    ds_escolaridade = random.choice(['Ensino Fundamental', 'Ensino Médio', 'Graduação', 'Pós-graduação'])  # Escolhendo um nível de escolaridade
    ds_estado_civil = random.choice(['Solteiro(a)', 'Casado(a)', 'Viúvo(a)', 'Divorciado(a)'])  # Escolhendo um estado civil
    nm_grupo_sanguineo = random.choice(['A+', 'B+', 'AB+', 'O+', 'A-', 'B-', 'AB-', 'O-'])  # Escolhendo um tipo sanguíneo
    nr_altura = round(random.uniform(1.50, 2.00), 2)  # Gerando altura entre 1.50 e 2.00 metros
    nr_peso = round(random.uniform(50.0, 100.0), 2)  # Gerando peso entre 50.0 e 100.0 kg
    dt_cadastro = datetime.datetime.now()  # Registrando a data e hora de cadastro
    nm_usuario = 'admin'  # Definindo um usuário responsável pelos registros
    return (nm_paciente, nr_cpf, nm_rg, dt_nascimento, fl_sexo_biologico, ds_escolaridade, ds_estado_civil, nm_grupo_sanguineo, nr_altura, nr_peso, dt_cadastro, nm_usuario)

# Conectar ao banco de dados Oracle
db = oracledb.connect(user='rm552539', password='130701', dsn='oracle.fiap.com.br/orcl')
cursor = db.cursor()

# Loop para inserir dados
for _ in range(100001):
    data = generate_data()

    # Gere um valor da sequência para ID_PACIENTE
    cursor.execute("SELECT paciente_seq.NEXTVAL FROM DUAL")
    id_paciente = cursor.fetchone()[0]

    data = (id_paciente,) + data  # Adicione o valor de ID_PACIENTE à tupla de dados

    cursor.execute('''
        INSERT INTO T_RHSTU_PACIENTE
        (ID_PACIENTE, NM_PACIENTE, NR_CPF, NM_RG, DT_NASCIMENTO, FL_SEXO_BIOLOGICO, DS_ESCOLARIDADE, DS_ESTADO_CIVIL, NM_GRUPO_SANGUINEO, NR_ALTURA, NR_PESO, DT_CADASTRO, NM_USUARIO)
        VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13)
    ''', data)

# Commit para inserir os dados no banco de dados
db.commit()

# Feche o cursor e a conexão com o banco de dados
cursor.close()
db.close()

# Mensagem de conclusão
print("Inserção de dados concluída.")
