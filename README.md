```markdown
# HealCare - Sistema de Autenticação Clínica

O HealCare é um sistema desktop para registro e autenticação de usuários do sistema de uma clínica fictícia. Desenvolvido em Python, o projeto simula a camada inicial de controle de acesso da plataforma, garantindo a segurança dos dados sensíveis desde o momento do login.

O principal objetivo deste projeto foi consolidar conceitos fundamentais de Programação Orientada a Objetos (POO) na construção de interfaces gráficas e na persistência segura de dados.

---

## 🚀 Funcionalidades

* **Interface Modular:** Telas de Login e Cadastro estruturadas de forma independente através de classes.
* **Navegação Inteligente:** Loop de controle de eventos que gerencia o ciclo de vida das janelas (evitando vazamento de memória).
* **Segurança de Credenciais:** Persistência de senhas criptografadas no banco de dados utilizando algoritmos de hash robustos.
* **Busca Referencial Dinâmica:** Sistema automatizado para recuperar dados associados ao usuário logado e exibi-los na Dashboard de Boas-Vindas.

---

## 🛠️ Tecnologias e Arquitetura

Para manter o projeto leve, performático e independente de dependências externas complexas, foi utilizada a biblioteca padrão do ecossistema Python para a estrutura principal:

* **[Python](https://www.python.org/) (v3.13+)** - Linguagem base do sistema.
* **Tkinter** - Biblioteca nativa para a construção da interface gráfica (GUI) baseada em gerenciamento por `Grid`.
* **SQLite3** - Banco de dados relacional embutido para armazenamento local das informações de cadastro.
* **Bcrypt** - Biblioteca de criptografia de terceiros utilizada para gerar hashes seguros das senhas.

---

## 🧠 Aprendizados e Tomadas de Decisão

1. **Foco nos Fundamentos com Tkinter Puro:** Optei por explorar ao máximo o Tkinter tradicional para entender o funcionamento bruto de gerenciadores de layout, empacotamento, dimensionamento responsivo e herança direta de componentes de janela (`tk.Tk`) através da POO.
2. **Tratamento Rigoroso de Exceções:** Todas as funções que interagem com o banco de dados utilizam blocos `try/except/finally` para garantir que conexões e cursores nunca fiquem travados na memória.
3. **Persistência de Dados Profissional:** Em vez de salvar senhas em formato de texto limpo, o sistema utiliza criptografia de nível de produção antes de enviar os dados ao SQLite, salvando-os como bytes puros.

---

## 💻 Como Executar o Projeto

### Pré-requisitos
Certifique-se de ter o **Python 3** instalado na sua máquina. O `Tkinter` e o `SQLite3` já vêm instalados por padrão na maioria das distribuições do Python.

### 1. Clonar o repositório

```bash
git clone [https://github.com/LukasDev-net/HealCare.git](https://github.com/LukasDev-net/HealCare.git)
cd HealCare
```

### 2. Configurar o Ambiente Virtual

Para isolar as dependências do projeto de forma limpa, crie e ative o ambiente virtual:

* **No Windows:**

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

* **No Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

Com o ambiente virtual `.venv` ativado no seu terminal, instale todas as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 4. Iniciar o Sistema

```bash
python App_Tela_Login.py
```
```