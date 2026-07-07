#Conexão com o banco de dados da aplicação
import sqlite3 

#Sistema de criptografia e segurança de senhas
import bcrypt 

#Captura do ano atual para validação de data
from datetime import datetime 

def iniciar_conexao():
    """
    Cria a conexão com o banco de dados 'db_users.db' e gera o seu respectivo cursor.

    Argumentos: 
        Não possui parâmetros de entrada. 

    Retorna:
        tuple:
            - connection (sqlite3.Connection ou None): Objeto de conexão com o banco de dados ou None se falhar.
            - cursor (sqlite3.Cursor ou None): Objeto cursor para execução de comandos SQL ou None se falhar.
    """
    try:
        connection = sqlite3.connect("db_users.db")
        cursor = connection.cursor()

        # retorna os objetos ativos caso a conexão seja estabelecida com sucesso.
        return connection, cursor 
    
    except Exception as erro:
        print(f"Ocorreu um erro ao estabelecer conexão: {erro}")

        #garante o retorno de None duplo para evitar erros de desempacotamento. 
        return None, None

def fechar_conexao(conexao, cursor):
    """
    Fecha a conexão com o banco de dados e o respectivo cursor passado nos argumentos se estiverem ativos.

    Argumentos: 
        conexao (sqlite3.Connection): Variável que armazena a conexão com o banco de dados.
        cursor (sqlite3.Cursor): Variável que armazena o cursor associado à conexão.

    Retorna:
        None: A função não retorna valores, apenas exibe no terminal se o encerramento foi bem-sucedido ou falhou.
    """ 
    try:
        #checa a conexão e o cursor e os fecha se estiverem ativos.
        if cursor: cursor.close()
        if conexao: conexao.close()
        print("conexão encerrada com sucesso")

    except Exception as erro:
        print(f"Ocorreu um erro ao encerrar conexão: {erro}")

def criar_tabela():
    """
    Cria uma tabela 'usuario' no banco de dados 'db_users.db' caso ela não exista. 

    Argumentos: 
        Não possui parâmetros de entrada.
    
    Retorna:
        None: A função não retorna valores, apenas exibe no terminal se a criação da tabela foi bem-sucedida ou falhou. 
    """
    try:
        #chama a função para criar uma conexão com o banco de dados e seu respectivo cursor e faz o desempacotamento dos valores retornados.
        conexao, cursor = iniciar_conexao() 
        #NOTA: O campo 'senha' está sendo declarada no tipo BLOB porque o bcrypt gera um hash em formato de bytes puros. 
        comando = ''' CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        nome_de_usuario TEXT UNIQUE NOT NULL,
        data_de_nascimento TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha BLOB NOT NULL
        )'''
        cursor.execute(comando)
        conexao.commit()
        #fecha a conexão e o cursor criados anteriormente para liberação de memória
        fechar_conexao(conexao, cursor)
        print("Tabela criada com êxito")

    except Exception as erro:
        print(f"Ocorreu um erro ao tentar criar tabela: {erro}")

def tratar_data(data):
    """
    Padroniza e valida datas passadas como string no formato 'dd/mm/yyyy'.

    Argumentos:
        data (Str): Texto contendo a data a ser tratada.

    Retorna: 
        tuple:
            - bool: True se a operação for bem-sucedida ou False se falhar.
            - str: A data formatada (se True) ou uma mensagem explicando o erro (se False).
    """
    #Filtra apenas os digitos para remover qualquer caractere estranho no argumento e os armazena em uma lista
    numeros = "".join([c for c in data if c.isdigit()])
    ano_atual = datetime.now().year
    
    #Retorna Falso caso a quantidade de dígitos ultrapasse o valor estimado para uma data
    if len(numeros) != 8:
        return False, "Data incorreta! Preencha o campo de data utilizando o padrão dd/mm/yyyy"
    
    #Transforma os valores da data em inteiros para filtrar possíveis valores inconsistentes
    dia_int = int(numeros[0:2])
    mes_int = int(numeros[2:4])
    ano_int = int(numeros[4:8])
    if dia_int > 31 or dia_int == 0: 
        return False, "Data incorreta! Dia inexistente"
    elif mes_int > 12 or mes_int == 0:
        return False, "Data incorreta! Mês inexistente"
    elif ano_int > (ano_atual - 18) or ano_int < (ano_atual - 120):
        return False, "Data incorreta! Ano insuficiente(-18) ou inexistente"
    else:
        #retorna a data em string no formato 'dd/mm/yyyy'
        dia_str = numeros[0:2]
        mes_str = numeros[2:4]
        ano_str = numeros[4:8]
        data_tratada = f"{dia_str}/{mes_str}/{ano_str}"

        return True, data_tratada

def cadastrar_usuario(nome, user_name, data_nasc, email, senha):
    """
    Registra os dados dos campos de cadastro de usuário na tabela 'usuario' do banco de dados 'db_users.db' se todos os campos estiverem preenchidos e consistentes com as regras de negócio.

    Argumentos: 
        nome (str): String com o nome registrado pelo usuário.
        user_name (str): String com o nome de usuário registrado pelo usuário.
        data_nasc (str): String com a data de nascimento registrada pelo usuário.
        email (str): String com o email registrado pelo usuário.
        senha (str): String com a senha registrada pelo usuário.

    Retorna:
        Tuple:
            - bool: True se a operação for bem-sucedida ou False se falhar.
            - str: A mensagem confirmando a operação se for bem-sucedida ou informando o erro ocorrido se falhar.
    """
    try:
        # Valida se há campos vazios ou preenchidos apenas com espaços, impedindo registros inválidos.
        if not nome.strip() or not user_name.strip() or not email.strip() or not senha.strip():
            return False, "Todos os campos devem ser preenchidos!"
        # Verifica se já possui registro no banco com o nome de usuário a ser cadastrado, impedindo registro duplicado
        if verificar_username(user_name):
            return False, "Nome de Usuário já existente, tente um novo"
        # Verifica se Já possui registro no banco com o email a ser cadastrado, impedindo registro duplicado
        if verificar_email(email):
            return False, "Email já cadastrado"
        
        #Trata a data registrada pelo usuário e desempacota os valores retornados
        sucesso, data_resultado = tratar_data(data_nasc)
        #Impede cadastro se a data registrada, após ser tratada, estiver inconsistente.
        if not sucesso:
            return False, data_resultado           
        #Atualiza a variável com a data formatada (dd/mm/yyyy) para o envio ao banco de dados
        data_nasc = data_resultado
        # Verifica o tamanho da variável senha, impedindo registro de senhas com menos de 6 caracteres
        if len(senha) < 6:
            return False, "digite pelo menos 6 caracteres"    

        # Converte a string da senha em bytes para ser processada pelo bcrypt  
        pw_crypt = senha.encode('utf-8')
        # Gera o Salt e cria o hash seguro da senha
        senha_hash = bcrypt.hashpw(pw_crypt, bcrypt.gensalt())

        # Inicia conexão com o banco de dados e cria o cursor.
        conexao, cursor = iniciar_conexao()
        # Executa o comando INSERT na tabela 'usuario' e registra os dados validados do cadastro no banco de dados
        cmd = '''INSERT INTO usuario (nome, nome_de_usuario, data_de_nascimento, email, senha) VALUES (?, ?, ?, ?, ?)'''
        cursor.execute(cmd, (nome, user_name, data_nasc, email, senha_hash))
        conexao.commit()
        # Fecha a conexão e o cursor do banco e retorna o feedback
        fechar_conexao(conexao, cursor)
        return True, "Usuário cadastrado com sucesso"              
                
    except Exception as erro:
        msg = f'''Erro ao cadastrar no banco: {erro}'''
        return False, msg
        
def verificar_email(email):
    """
    Verifica se o e-mail informado já está cadastrado na tabela 'usuario' do banco 'db_users.db'.

    Argumentos:
        email (str): O endereço de e-mail a ser consultado no banco de dados.
    
    Retorna: 
        bool: True se o e-mail for encontrado ou False caso contrário.
    """
    try:
        cmd = '''SELECT email FROM usuario WHERE email = ?'''
        #Abre conexão com o banco de dados e busca pelo email informado.
        conexao, cursor = iniciar_conexao()
        cursor.execute(cmd, (email,))

        # Recupera o primeiro resultado encontrado (retorna None se não existir).
        resultado = cursor.fetchone()

        # Garante o encerramento dos recursos antes de retornar o resultado.
        fechar_conexao(conexao, cursor)

        # Retorna True se o email estiver registrado no banco ou False se não.
        return True if resultado else False
        
    except Exception as erro:
        print(f"Ocorreu um ao verificar email: {erro}")
        return False

def verificar_username(usuario):
    #NOTA: essa função e a função 'verificar_email' irão torna-se uma única função por motivos de redundancia 
    try:
        cmd = '''SELECT nome_de_usuario FROM usuario WHERE nome_de_usuario = ?'''
        conexao, cursor = iniciar_conexao()
        cursor.execute(cmd, (usuario,))
        resultado = cursor.fetchone()
        fechar_conexao(conexao, cursor)
        return True if resultado else False    
    except Exception as erro:
        print(f"Ocorreu um erro ao verificar usuário: {erro}")
        return False
    
def verificar_login(email, senha):
    """
    Verifica se o email informado está cadastrado e valida a senha correspondente.

    Argumentos: 
        email (str): email informado para login
        senha (str): senha informada para validação

    Retorna: 
        Tuple:
            - bool: False se os dados estiverem inconsistentes ou True se as informações forem verídicas.
            - str:  Mensagem informando resultado da operação. 
    """
    #Verifica se a senha informada possui o mínimo de caracteres esperado.
    if len(senha) < 6:
        return False, "digite pelo menos 6 caracteres"
    

    try:
        #inicia conexão com o banco de dados e busca a senha do email informado.
        conexao, cursor = iniciar_conexao()
        cmd = '''SELECT senha FROM usuario WHERE email = ?'''
        cursor.execute(cmd, (email,))
        resultado = cursor.fetchone()

        # Garante encerramento dos recursos antes de processar os resultados.
        fechar_conexao(conexao, cursor)

        
        if resultado:
            # Extrai o hash da senha armazenado no banco
            senha_cryp_banco = resultado[0]
            # Converte a string da senha informada pelo usuário em bytes.
            senha_bytes = senha.encode('utf-8')

            # Compara o hash do banco com a senha digitada.
            if bcrypt.checkpw(senha_bytes, senha_cryp_banco):
                return True, "Login efetuado com sucesso!"
            else: 
                return False, "Email ou Senha incorretos"   
             
        else:
            # retorna falso se o email informado não existe no banco de dados.
            return False, "Email ou senha incorretos"
            
    except Exception as erro:
        msg = f'''Ocorreu um erro ao verificar login: {erro}'''
        return False, msg


criar_tabela()