import tkinter as tk
from Banco_user_v3 import verificar_login, cadastrar_usuario, executar_busca_referencial
from tkinter import messagebox

class TelaLogin(tk.Tk):
    """
    Interface gráfica responsável pelo login de usuários cadastrados no sistema.

    Esta classe gerencia o ciclo de vida da janela de login, valida as informações 
    preenchidas pelo usuário e faz a ponte com o módulo de banco de dados para 
    a verificação de credenciais.    
    """
    def __init__(self):
        """
        Inicializa a janela de login e configura seus componentes visuais.
        """

        super().__init__()
        self.title("HealCare - Login")
        self.geometry("400x400")
        self.configure(bg="#F8F9FA")
        # Faz com que a coluna principal se estenda dinamicamente
        self.grid_columnconfigure(0, weight=1)
        
        # Variáveis de controle de estado e navegação entre janelas
        self.ir_para_cadastro = False
        self.login_confirmado = False
        self.usuario_autenticado = ""

        self.main_msg = tk.Label(
                    self,
                    text = "HealCare",
                    font= ("Segoe UI", 20, "bold"),
                    fg= "#007BFF",
                    bg= "#F8F9FA"
                    )
        self.main_msg.grid(row = 0, column= 0, pady=(20, 5), padx= 20)

        self.sub_msg = tk.Label(
                    self,
                    text = "faça o login para prosseguirmos com o atendimento.",
                    font= ("Segoe UI", 10),
                    fg= "#6C757D",
                    bg= "#F8F9FA"
                    )
        self.sub_msg.grid(row= 1, column= 0, pady=(0, 10), padx= 20)

        #campo de email de login
        self.email_label = tk.Label(self, text= "Email:", font=("Segoe UI", 10, "bold"), fg="#212529", bg="#F8F9FA")
        self.email_label.grid(row= 2, column= 0, sticky="w", pady= (10, 2), padx= 40)
        self.email_entry = tk.Entry(self, font=("Segoe UI", 11), bd= 1, relief="solid", fg="#212529")
        self.email_entry.grid(row = 3, column = 0, ipady= 4, padx= 40, sticky="we")

        #campo de senha de login
        self.senha_label= tk.Label(self, text= "Senha:", font=("Segoe UI", 10, "bold"), fg="#212529", bg="#F8F9FA")
        self.senha_label.grid(row= 4, column= 0, sticky="w", pady= (10, 2), padx= 40)
        self.senha_entry = tk.Entry(self, font=("Segoe UI", 11), show="*", bd= 1, relief="solid", fg="#212529") #O parâmetro show="*" oculta o texto digitado para proteger a senha do usuário
        self.senha_entry.grid(row= 5, column= 0, ipady= 4, padx= 40, sticky="we")

        #botão para confirmar login
        self.login_bttn = tk.Button(
                                self,
                                text= "Entrar",
                                font=("Segoe UI", 10, "bold"),
                                bg= "#007BFF",
                                fg= "#FFFFFF",
                                activebackground="#0056B3",
                                activeforeground= "#FFFFFF",
                                bd= 0, 
                                cursor="hand2",
                                command= self.login
                                )
        self.login_bttn.grid(row= 6, column= 0, ipady= 2, ipadx= 20, padx= 40, pady=20)

        #botão para ir à janela de cadastro
        self.cadastro_bttn = tk.Button(self,
                                    text= "Não possui uma conta? Cadastre-se aqui!",
                                    font=("Segoe UI", 9, "underline"),
                                    bg="#F8F9FA",
                                    fg="#007BFF",
                                    bd=0,
                                    activebackground="#F8F9FA",
                                    activeforeground="#212529",
                                    cursor="hand2",
                                    command= self.navegar_cadastro
                                    )
        self.cadastro_bttn.grid(row= 7, column= 0)

    def navegar_cadastro(self):
        """
        Sinaliza a intenção de ir para o cadastro e destrói a tela atual.
        """
        self.ir_para_cadastro = True
        self.destroy()
        
    def login(self):
        """
        Coleta as credenciais de login, valida no banco e gerencia o estado da sessão.
        """
        email = self.email_entry.get().strip()
        senha = self.senha_entry.get().strip()

        sucesso, msg = verificar_login(email, senha)

        if sucesso: 
            self.login_confirmado = True
            # Busca o nome real do usuário para passar à tela principal
            self.usuario_autenticado = executar_busca_referencial("nome", "email", email)
            self.destroy()

        else:
            messagebox.showwarning('Falha', "Login falho: Email ou Senha incorretos! Tente novamente!")

class TelaCadastro(tk.Tk):
    """
    Interface gráfica responsável pelo registro de novos usuários na base de dados.

    Esta classe coleta informações cadastrais básicas, repassa para as funções 
    de persistência de dados e permite o retorno imediato à tela de login.
    """

    def __init__(self):
        """
        Inicializa a janela de cadastro e configura os campos do formulário.
        """
        super().__init__()
        self.title("HealCare - Criar Conta")
        self.geometry("400x600")
        self.configure(bg="#F8F9FA")
        self.grid_columnconfigure(0, weight=1)

        #Variavel de navegação para a janela de Login
        self.ir_para_login = False

        self.main_msg = tk.Label(
                    self,
                    text = "HealCare",
                    font=("Segoe UI", 20, "bold"),
                    fg="#007BFF",
                    bg="#F8F9FA"
                    )
        self.main_msg.grid(row = 0, column= 0, pady=(20, 5), padx= 20)

        self.sub_msg = tk.Label(
                    self,
                    text = "faça o seu cadastro para prosseguirmos com o atendimento.",
                    font=("Segoe UI", 10),
                    fg="#6C757D",
                    bg="#F8F9FA"
                    )
        self.sub_msg.grid(row= 1, column= 0, pady=(0, 10), padx= 10 )

        #campo de nome
        self.nome_cad_label = tk.Label(
                                    self,
                                    text= "Nome:",
                                    font=("Segoe UI", 10, "bold"),
                                    fg="#212529",
                                    bg="#F8F9FA"
                                    )
        self.nome_cad_label.grid(row= 2, column= 0, pady= (10, 2), sticky="w", padx= 20)

        self.nome_cad_entry = tk.Entry(self, font=("Segoe UI", 11), bd= 1, relief="solid", fg="#212529")
        self.nome_cad_entry.grid(row= 3, column= 0, ipady= 4, padx= 40, sticky="we")

        #campo de nome de usuário
        self.username_cad_label = tk.Label(self,
                                    text= "Nome de usuário:",
                                    font=("Segoe UI", 10, "bold"),
                                    fg="#212529",
                                    bg="#F8F9FA"
                                    )
        self.username_cad_label.grid(row= 4, column= 0, pady= (10, 2), sticky="w", padx= 20)

        self.username_cad_entry = tk.Entry(self, font=("Segoe UI", 11), bd= 1, relief="solid", fg="#212529")
        self.username_cad_entry.grid(row= 5, column= 0, ipady= 4, padx= 40, sticky="we")

        #campo de data de nascimento
        self.datanasc_cad_label = tk.Label(self,
                                    text= "Data de nascimento:",
                                    font=("Segoe UI", 10, "bold"),
                                    fg="#212529",
                                    bg="#F8F9FA"
                                    )
        self.datanasc_cad_label.grid(row= 6, column= 0, pady= (10, 2), sticky="w", padx= 20)

        self.datanasc_cad_entry = tk.Entry(self, font=("Segoe UI", 11), bd= 1, relief="solid", fg="#212529")
        self.datanasc_cad_entry.grid(row= 7, column= 0, ipady= 4, padx= 40, sticky="we")

        #campo de email
        self.email_cad_label = tk.Label(self,
                                    text= "Email:",
                                    font=("Segoe UI", 10, "bold"),
                                    fg="#212529",
                                    bg="#F8F9FA"
                                    )
        self.email_cad_label.grid(row= 8, column= 0, pady= (10, 2), sticky="w", padx= 20)

        self.email_cad_entry = tk.Entry(self, font=("Segoe UI", 11), bd= 1, relief="solid", fg="#212529")
        self.email_cad_entry.grid(row = 9, column = 0, ipady= 4, padx= 40, sticky="we")

        #campo de senha para cadastro
        self.senha_cad_label= tk.Label(self,
                                    text= "Senha:",
                                    font=("Segoe UI", 10, "bold"),
                                    fg="#212529",
                                    bg="#F8F9FA"
                                    )
        self.senha_cad_label.grid(row= 10, column= 0, pady= (10, 2), sticky="w", padx= 20)

        #O parâmetro show="*" oculta o texto digitado para proteger a senha do usuário
        self.senha_cad_entry = tk.Entry(self, font=("Segoe UI", 11), bd= 1, relief="solid", fg="#212529", show="*") 

        self.senha_cad_entry.grid(row= 11, column= 0, ipady= 4, padx= 40, sticky="we")

        #botão para confirmar cadastro
        self.cadastro_bttn = tk.Button(
                                    self,
                                    text= "Cadastrar",
                                    font=("Segoe UI", 10, "bold"),
                                    bg= "#007BFF",
                                    fg= "#FFFFFF",
                                    activebackground="#0056B3",
                                    activeforeground= "#FFFFFF",
                                    bd= 0, 
                                    cursor="hand2",
                                    command= self.salvar_cadastro
                                    )
        self.cadastro_bttn.grid(row= 12, column= 0, ipady= 2, ipadx= 20, padx= 40, pady=20)

        #botão para ir para a janela de login
        self.login_bttn = tk.Button(
                                self,
                                text= "Já possui um cadastro? Entre na sua conta aqui!",
                                font=("Segoe UI", 9, "underline"),
                                bg="#F8F9FA",
                                fg="#007BFF",
                                bd=0, 
                                activebackground="#F8F9FA",
                                activeforeground="#212529",
                                cursor="hand2",
                                command=self.navegar_login
                                )
        self.login_bttn.grid(row= 13, column= 0, pady= 6, padx= 2)

    def salvar_cadastro(self):
        """
        Coleta as informações dos campos do formulário e as registra no banco.
        """

        nome = self.nome_cad_entry.get()
        username = self.username_cad_entry.get()
        data = self.datanasc_cad_entry.get()
        email = self.email_cad_entry.get()
        senha = self.senha_cad_entry.get()

        sucesso, msg = cadastrar_usuario(nome, username, data, email, senha)

        if sucesso:
            messagebox.showinfo('Sucesso', msg)
            self.navegar_login()
        else:
            messagebox.showinfo('Falha', msg)

    def navegar_login(self):
        """
        Sinaliza a intenção de ir para a tela de login e destrói a tela de cadastro atual.
        """
        self.ir_para_login = True
        self.destroy()

class TelaPrincipal(tk.Tk):
    """
    Painel Principal do sistema.
    
    Exibido logo após o sucesso da autenticação do usuário.
    """
    def __init__(self, nome_usuario):
        """
        Inicializa o painel principal.

        Argumentos:
            nome_usuario (str): Nome do usuário autenticado vindo do banco de dados.
        """

        super().__init__()
        self.title("HealCare - Home")
        self.geometry("800x500")
        self.configure(bg="#F8F9FA")
        self.grid_columnconfigure(0, weight=1)

        label_boas_vindas = tk.Label(self, text=f"Bem-vindo(a), {nome_usuario}!", font=("Segoe UI", 20, "bold"), background="#F8F9FA", foreground="#007BFF")
        label_boas_vindas.pack(pady=50, fill="both", expand=True)

# =====================================================================
# GERENCIADOR DE JANELAS
# =====================================================================        

if __name__ == "__main__":
    usuario_final = ""
    login_sucesso = False

    # Loop de Controle: Permite alternar entre telas de login e cadastro sem quebrar a memória
    while True:
        app_login = TelaLogin()
        app_login.mainloop()

        # Se o usuário fechou a janela de login, interrompe a execução do sistema
        if not app_login.login_confirmado and not app_login.ir_para_cadastro:
            break

        # Se o login foi bem-sucedido, extrai o nome do usuário e quebra o loop para abrir o painel principal
        if app_login.login_confirmado:
            usuario_final = app_login.usuario_autenticado
            login_sucesso = True
            break
        
        if app_login.ir_para_cadastro:
            app_cadastro = TelaCadastro()
            app_cadastro.mainloop() 

        # Se o usuário fechou a janela de cadastro, encerra o programa
        if not app_cadastro.ir_para_login:
            break
    
    if login_sucesso:
        app_sistema = TelaPrincipal(nome_usuario=app_login.usuario_autenticado)
        app_sistema.mainloop()