import tkinter as tk
from tkinter import messagebox
#importação das funções de controle e validação do banco de dados
from versao_2.Banco_user_v2 import cadastrar_usuario, verificar_login

# ==============================================================================
# FUNÇÕES DE FEEDBACK E FLUXO DE TELAS
# ==============================================================================

# Navega para o frame de cadastro, ajusta a altura da janela e torna o layout responsivo para não quebrar ao expandir.
def ir_para_cadastro():
    frame_login.pack_forget()
    frame_cadastro.grid_columnconfigure(0, weight=1)
    frame_cadastro.pack(fill="both", expand=True)
    janela.geometry("400x550")

# Navega para o frame de login, ajusta a altura da janela e torna o layout responsivo para não quebrar ao expandir.
def ir_para_login():
    frame_cadastro.pack_forget()
    frame_login.grid_columnconfigure(0, weight=1)
    frame_login.pack(fill="both", expand=True)
    janela.geometry("400x400")


def verificar_entrada(email, senha):
    """
    Configura e exibe as pop-ups de feedback na interface gráfica de login.
    Acessa a função 'verificar_login' do módulo 'Banco_user' para validar se as credenciais informadas constam no banco de dados e exibe o resultado diretamente ao usuário através de caixas de mensagem do Tkinter.

    Argumentos: 
        email (str): Texto vindo do campo de entrada (Entry) de e-mail do frame_login.
        senha (str): Texto vindo do campo de entrada (Entry) de senha do frame_login.

    Retorna:
        None: A função não retorna valores, apenas exibe caixas de diálogo (showinfo, showwarning ou showerror) na tela.

    """
    try:
        login, msg = verificar_login(email, senha)
        if login: 
            messagebox.showinfo('Sucesso', msg)
        else: 
            messagebox.showwarning('Aviso', msg)

    except Exception as erro:
        msg = f'''Ocorreu um erro ao verificar o login: {erro}'''
        print(msg)
        messagebox.showerror('Erro', msg)

def verificar_cadastro(nome, usuario, data, email, senha):
    """
    Configura e exibe as pop-ups de feedback na interface gráfica de cadastro.
    Acessa a função 'cadastrar_usuario' do módulo 'Banco_user' para verificar e registrar no banco de dados as credenciais do novo usuário cadastrado, o resultado é exibido diretamente ao usuário através de caixas de mensagem do Tkinter

    Argumentos:
        nome (str): Texto vindo do campo de entrada (Entry) de Nome do frame_cadastro.
        usuario (str): Texto vindo do campo de entrada (Entry) de Nome de usuário do frame_cadastro.
        data (str): Texto vindo do campo de entrada (Entry) Data de nascimento do frame_cadastro.
        email (str): Texto vindo do campo de entrada (Entry) Email do frame_cadastro.
        senha (str): Texto vindo do campo de entrada (Entry) Senha do frame_cadastro.

    Retorna:
        None: A função não retorna valores, apenas exibe caixas de diálogo (showinfo, showwarning ou showerror) na tela.
    """
    try: 
        cadastrar, msg = cadastrar_usuario(nome, usuario, data, email, senha)
        if cadastrar:
            messagebox.showinfo('Sucesso', msg)
            #direciona para a página de login após cadastrar com sucesso
            ir_para_login() 
        else:
            messagebox.showwarning('Aviso', msg)
    except Exception as erro:
        msg = f'''Ocorreu um erro ao cadastrar o usuário: {erro}'''
        print(msg)
        messagebox.showerror('Erro', msg)

janela = tk.Tk()
janela.configure(bg= "#F8F9FA")
janela.title("HealCare")

# ==============================================================================
# SEÇÃO DO FRAME DE LOGIN
# ==============================================================================

frame_login = tk.Frame(janela, bg= "#F8F9FA")  

main_msg = tk.Label(
                    frame_login,
                    text = "HealCare",
                    font= ("Segoe UI", 20, "bold"),
                    fg= "#007BFF",
                    bg= "#F8F9FA"
                    )
main_msg.grid(row = 0, column= 0, pady=(20, 5), padx= 20)

sub_msg = tk.Label(
                    frame_login,
                    text = "faça o login para prosseguirmos com o atendimento.",
                    font= ("Segoe UI", 10),
                    fg= "#6C757D",
                    bg= "#F8F9FA"
                    )
sub_msg.grid(row= 1, column= 0, pady=(0, 10), padx= 20)

#campo de email de login
email_label = tk.Label(frame_login, text= "Email:", font=("Segoe UI", 10, "bold"), fg="#212529", bg="#F8F9FA")
email_label.grid(row= 2, column= 0, sticky="w", pady= (10, 2), padx= 40)
email_entry = tk.Entry(frame_login, font=("Segoe UI", 11), bd= 1, relief="solid", fg="#212529")
email_entry.grid(row = 3, column = 0, ipady= 4, padx= 40, sticky="we")

#campo de senha de login
senha_label= tk.Label(frame_login, text= "Senha:", font=("Segoe UI", 10, "bold"), fg="#212529", bg="#F8F9FA")
senha_label.grid(row= 4, column= 0, sticky="w", pady= (10, 2), padx= 40)
senha_entry = tk.Entry(frame_login, font=("Segoe UI", 11), show="*", bd= 1, relief="solid", fg="#212529") #O parâmetro show="*" oculta o texto digitado para proteger a senha do usuário
senha_entry.grid(row= 5, column= 0, ipady= 4, padx= 40, sticky="we")

#botão para confirmar login
login_bttn = tk.Button(
                        frame_login,
                        text= "Entrar",
                        font=("Segoe UI", 10, "bold"),
                        bg= "#007BFF",
                        fg= "#FFFFFF",
                        activebackground="#0056B3",
                        activeforeground= "#FFFFFF",
                        bd= 0, 
                        cursor="hand2",
                        command=lambda: verificar_entrada(email_entry.get(), senha_entry.get()) #obtem os valores dos campos somente quando o botão é acionado
                        )
login_bttn.grid(row= 6, column= 0, ipady= 2, ipadx= 20, padx= 40, pady=20)

#botão para ir à janela de cadastro
cadastro_bttn = tk.Button(frame_login,
                            text= "Não possui uma conta? Cadastre-se aqui!",
                            font=("Segoe UI", 9, "underline"),
                            bg="#F8F9FA",
                            fg="#007BFF",
                            bd=0,
                            activebackground="#F8F9FA",
                            activeforeground="#212529",
                            cursor="hand2",
                            command= ir_para_cadastro
                            )
cadastro_bttn.grid(row= 7, column= 0)

# ==============================================================================
# SEÇÃO DO FRAME DE CADASTRO
# ==============================================================================

frame_cadastro = tk.Frame(janela, bg="#F8F9FA")

main_msg = tk.Label(
                    frame_cadastro,
                    text = "HealCare",
                    font=("Segoe UI", 20, "bold"),
                    fg="#007BFF",
                    bg="#F8F9FA"
                    )
main_msg.grid(row = 0, column= 0, pady=(20, 5), padx= 20)

sub_msg = tk.Label(
                    frame_cadastro,
                    text = "faça o seu cadastro para prosseguirmos com o atendimento.",
                    font=("Segoe UI", 10),
                    fg="#6C757D",
                    bg="#F8F9FA"
                    )
sub_msg.grid(row= 1, column= 0, pady=(0, 10), padx= 10 )

#campo de nome
nome_cad_label = tk.Label(
                            frame_cadastro,
                            text= "Nome:",
                            font=("Segoe UI", 10, "bold"),
                            fg="#212529",
                            bg="#F8F9FA"
                            )
nome_cad_label.grid(row= 2, column= 0, pady= (10, 2), sticky="w", padx= 20)

nome_cad_entry = tk.Entry(frame_cadastro, font=("Segoe UI", 11), bd= 1, relief="solid", fg="#212529")
nome_cad_entry.grid(row= 3, column= 0, ipady= 4, padx= 40, sticky="we")

#campo de nome de usuário
username_cad_label = tk.Label(frame_cadastro,
                            text= "Nome de usuário:",
                            font=("Segoe UI", 10, "bold"),
                            fg="#212529",
                            bg="#F8F9FA"
                            )
username_cad_label.grid(row= 4, column= 0, pady= (10, 2), sticky="w", padx= 20)

username_cad_entry = tk.Entry(frame_cadastro, font=("Segoe UI", 11), bd= 1, relief="solid", fg="#212529")
username_cad_entry.grid(row= 5, column= 0, ipady= 4, padx= 40, sticky="we")

#campo de data de nascimento
datanasc_cad_label = tk.Label(frame_cadastro,
                            text= "Data de nascimento:",
                            font=("Segoe UI", 10, "bold"),
                            fg="#212529",
                            bg="#F8F9FA"
                            )
datanasc_cad_label.grid(row= 6, column= 0, pady= (10, 2), sticky="w", padx= 20)

datanasc_cad_entry = tk.Entry(frame_cadastro, font=("Segoe UI", 11), bd= 1, relief="solid", fg="#212529")
datanasc_cad_entry.grid(row= 7, column= 0, ipady= 4, padx= 40, sticky="we")

#campo de email
email_cad_label = tk.Label(frame_cadastro,
                            text= "Email:",
                            font=("Segoe UI", 10, "bold"),
                            fg="#212529",
                            bg="#F8F9FA"
                            )
email_cad_label.grid(row= 8, column= 0, pady= (10, 2), sticky="w", padx= 20)

email_cad_entry = tk.Entry(frame_cadastro, font=("Segoe UI", 11), bd= 1, relief="solid", fg="#212529")
email_cad_entry.grid(row = 9, column = 0, ipady= 4, padx= 40, sticky="we")

#campo de senha para cadastro
senha_cad_label= tk.Label(frame_cadastro,
                            text= "Senha:",
                            font=("Segoe UI", 10, "bold"),
                            fg="#212529",
                            bg="#F8F9FA"
                            )
senha_cad_label.grid(row= 10, column= 0, pady= (10, 2), sticky="w", padx= 20)

senha_cad_entry = tk.Entry(frame_cadastro, font=("Segoe UI", 11), bd= 1, relief="solid", fg="#212529", show="*") #O parâmetro show="*" oculta o texto digitado para proteger a senha do usuário
senha_cad_entry.grid(row= 11, column= 0, ipady= 4, padx= 40, sticky="we")

#botão para confirmar cadastro
cadastro_bttn = tk.Button(
                            frame_cadastro,
                            text= "Cadastrar",
                            font=("Segoe UI", 10, "bold"),
                            bg= "#007BFF",
                            fg= "#FFFFFF",
                            activebackground="#0056B3",
                            activeforeground= "#FFFFFF",
                            bd= 0, 
                            cursor="hand2",
                            command=lambda: verificar_cadastro(nome_cad_entry.get(), username_cad_entry.get(), datanasc_cad_entry.get(), email_cad_entry.get(), senha_cad_entry.get()))
cadastro_bttn.grid(row= 12, column= 0, ipady= 2, ipadx= 20, padx= 40, pady=20)

#botão para ir para a janela de login
login_bttn = tk.Button(
                        frame_cadastro,
                        text= "Já possui um cadastro? Entre na sua conta aqui!",
                        font=("Segoe UI", 9, "underline"),
                        bg="#F8F9FA",
                        fg="#007BFF",
                        bd=0, 
                        activebackground="#F8F9FA",
                        activeforeground="#212529",
                        cursor="hand2",
                        command=ir_para_login
                        )
login_bttn.grid(row= 13, column= 0, pady= 6, padx= 2)

# ==============================================================================
# SEÇÃO DE INICIALIZAÇÃO DO SISTEMA
# ==============================================================================

# Define a tela de login como o ponto de partida padrão
frame_login.grid_columnconfigure(0, weight=1)
frame_login.pack(fill="both", expand=True)
janela.geometry("400x400")

janela.mainloop() # Inicia o loop de eventos da interface gráfica