import os
import sqlite3
from sqlite3 import Error

def ConexaoBanco():
    try:
        con = sqlite3.connect("C:/Users/avare/OneDrive/Documentos/projeto-agenda/agenda.db")
        print("Conexão bem-sucedida!")
    except Error as ex:
        print(ex)
    
    return con

vcon = ConexaoBanco()

def query(conexao, sql):
    try:
        c = conexao.cursor()
        c.execute(sql)
        conexao.commit()
        print("Feito!")
    except Error as ex:
        print(ex)

def consultar(conexao, sql):
    c = conexao.cursor()
    c.execute(sql)
    res = c.fetchall()
    return res


def menuPrincipal():
    while True:
        os.system('cls')
        print("""
        1 - Novo contato
        2 - Excluir
        3 - Atualizar
        4 - Listar todos os contatos
        5 - Pesquisar por nome
        6 - Sair
        """)
        opc = input("Escolha uma opção: ")

        match opc:
            case "1":
                adicionar()
            case "2":
                excluir()
            case "3":
                atualizar()
            case "4":
                listar()
            case "5":
                pesquisarNome()
            case "6":
                os.system('cls')
                print("Programa finalizado")
                break
            case _:
                print("ERRO - Valor invalido!")

def adicionar():
    os.system('cls')
    nome = input("Nome do novo contato: ")
    tel = input("Telefone: ")
    email = input("E-mail (opcional): ")
    vsql = f"""INSERT INTO tb_contatos(T_NOMECONTATO, T_TELEFONE, T_EMAIL)
            VALUES('{nome}', '{tel}', '{email}');"""

    query(vcon, vsql)

def excluir():
    os.system('cls')
    id = input("ID do contato a ser excluido (ou ENTER para consultar os ID's): ")
    if id == "":
        listar()
    else:
        vsql = f"DELETE FROM tb_contatos WHERE N_IDCONTATO={id}"
        query(vcon, vsql)
        print("Contato removido")

def atualizar():
    os.system('cls')
    id = input("ID do contato a ser atualizado: ")
    r = consultar(vcon, f"SELECT * FROM tb_contatos WHERE N_IDCONTATO={id}")
    rnome = r[0][1]
    rtel = r[0][2]
    remail = r[0][3]
    
    nome = input("Nome (ENTER para manter igual): ")
    tel = input("Telefone (ENTER para manter igual): ")
    email = input("E-mail (ENTER para manter igual): ")
    
    if len(nome) == 0:
        nome = rnome
    if len(tel) == 0:
        tel = rtel
    if len(email) == 0:
        email = remail
    
    vsql = f"UPDATE tb_contatos SET T_NOMECONTATO='{nome}', T_TELEFONE='{tel}', T_EMAIL='{email}' WHERE N_IDCONTATO={id}"
    query(vcon, vsql)

def listar():
    os.system('cls')
    try:
        lista = consultar(vcon, f"SELECT * FROM tb_contatos")
        for i in lista:
            print(f"ID: {i[0]} --- Nome: {i[1]} --- Telefone: {i[2]} --- E-mail: {i[3]}")
        os.system('pause')
    except Error as ex:
        print(ex)

def pesquisarNome():
    os.system('cls')
    nome = input("Nome: ")
    try:
        lista = consultar(vcon, f"SELECT * FROM tb_contatos WHERE T_NOMECONTATO LIKE '%{nome}%'")
        for i in lista:
            print(f"ID: {i[0]} --- Nome: {i[1]} --- Telefone: {i[2]} --- E-mail: {i[3]}")
        os.system('pause')
    except Error as ex:
        print(ex)
                
menuPrincipal()
vcon.close()
