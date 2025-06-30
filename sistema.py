from time import sleep
import os
import getpass
import sqlite3
from datetime import datetime
# Área pra importar as bibliotecas necessárias

# --------------------------------------------
con = sqlite3.connect('sistemabanco.db')
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS banco(nome, data_nascimento, usuario, senha, saldo)')
# Fazemos a conexão com o BD e criamos o cursor, logo após, criamos a tabela se ela não existir.
# --------------------------------------------
os.system('cls')

def Menu():
    global opçao
    print('\033[1;34mSEJA BEM VINDO AO BANCO PGB\033[m')
    print('''\033[1;36m[ 1 ] - Entrar
[ 2 ] - Cadastrar
[ 3 ] - Sair\033[m''')

    while True:
        opçao = input('O que deseja fazer ?: ')
        opçoesPermitidas = ['1', '2', '3']
        if opçao not in opçoesPermitidas:
            print('\033[1;31mOpção Inválida, tente novamente\033[m')
            sleep(1)
            continue

        elif opçao == '1':
            Entrar()
            break

        elif opçao == '2':
            Cadastrar()
            break

        elif opçao == '3':
            print('\033[1;32mObrigado por acessar o nosso banco, tenha um ótimo dia !\033[m')
            break    
        # Damos ao usuário as opções disponíveis, Entrar, Cadastrar e Sair.

def Entrar():
    global resultado
    global usuario
    global senha
    print('\nPOR GENTILEZA, DIGITE SEU USUÁRIO E SENHA: ')
    
    while True:
        try:
            usuario = input('Usuário: ')
            senha = getpass.getpass('Senha: ')

            cur.execute('SELECT * FROM banco WHERE usuario = ? AND senha = ?', (usuario, senha))
            resultado = cur.fetchone()
            # Solicitamos o usuario e senha e verificamos se os dados estão presentes no BD.

            if resultado:
                os.system('cls')
                print(f'\n✅ Login efetuado com sucesso! Bem-vindo(a), {resultado[0]}')
                Utilidades()
                break
                # Se estiver presente, fazemos o login do usuário.
            
            else:
                print('\n❌ Usuário ou senha incorretos. Tente novamente.')
                voltar = input('Deseja retornar ? [Digite 0]\n: ')
                print()
                # Se não, damos ao usuário a opção de voltar.
                if voltar == '0':
                    Menu()
                    continue
    
        except Exception as e:
            print('Erro ao tentar fazer login:', e)


def Utilidades():
    global saldo

    cur.execute('SELECT * FROM banco WHERE usuario = ?', (usuario,))
    resultado = cur.fetchone()
    saldo = resultado[4]
    # Aqui estamos atualizando a lista resultado, pra sempre estar com o valor certo
    print('''\033[1;34m
[ 1 ] - VER SALDO
[ 2 ] - SACAR
[ 3 ] - DEPOSITAR
[ 4 ] - SAIR\033[m''')
    opçaoAposEntrar = input('O que deseja fazer ?\n:')
    opçoesPermitidas = ['1', '2', '3', '4']
    if opçaoAposEntrar not in opçoesPermitidas:
        print('Digite uma opção válida !')
        sleep(2.5)
        os.system('cls')
        Utilidades()

    elif opçaoAposEntrar == '1':
        print(f'O saldo da conta de {resultado[0]} é R${saldo:.2f}')
        sleep(2.5)
        os.system('cls')
        Utilidades()
        # Aqui mostramos ao usuário o saldo da sua conta

    elif opçaoAposEntrar == '2':
        try:
            saque = float(input('Quanto deseja sacar ?\n:R$'))
            if saque > saldo:
                print('Digite um valor de saque menor ou igual ao saldo da sua conta !')
                sleep(2.5)
                os.system('cls')
            elif saque == 0:
                print(f'Saque de R${saque} é impossível fazer')
                sleep(2.5)
                os.system('cls')
            else:
                saldo -= saque
                print(f'Saque de R${saque:.2f} feito com sucesso\nAgora o seu saldo é de R${saldo:.2f}')
                sleep(2.5)
                os.system('cls')
            # Aqui é a área de saque

        except (ValueError, TypeError):
            print('Digite um valor numérico válido para o saque !')
            sleep(2.5)
            os.system('cls')
            Utilidades()
        
        else:
            cur.execute('UPDATE banco SET saldo = ? WHERE usuario = ?', (saldo, usuario))
            con.commit()
            Utilidades()
            # Atualizamos o valor do saldo do usuario.

    elif opçaoAposEntrar == '3':
        deposito = float(input('Quanto deseja Depositar?\n:R$'))
        if deposito >= 5000:
            print(f'Valor R${deposito:.2f} de depósito muito alto,deposite um valor menor !')
        else:
            saldo += deposito

            print(f'O seu saldo atualizado após o Depósito de R${deposito:.2f} é de R${saldo:.2f}')
            sleep(2.5)
            os.system('cls')

            cur.execute('UPDATE banco SET saldo = ? WHERE usuario = ?', (saldo, usuario))
            con.commit()
            Utilidades()
            # Depositamos o valor que o usuario digitar [abaixo de R$5000]

    elif opçaoAposEntrar == '4':
        print(f'\033[1;32mObrigado {resultado[0]} pela confiança, até mais !\033[m')
        # Opção de Sair

    
def Cadastrar():
    print('''\033[1;35mVAMOS FAZER O SEU CADASTRO\nINFORME OS SEUS DADOS:\033[m''')   

    while True:
        nome = input('Nome: ')
        if nome == '0':
            break
        try:
            dia, mes, ano = input('Data de Nascimento [dd/mm/yyyy]: ').split('/')
        except (UnboundLocalError, ValueError):
            print('\033[1;31mData Inválida, Tente Novamente\n[DIGITE 0 PARA SAIR]\033[m')
            continue
            # Solicitamos o nome e a data de nascimento, se a data de nascimento tiver um erro, ela volta pro incio da repetição
        else:
            dia, mes, ano = int(dia), int(mes), int(ano)
            data_nascimento = f'{dia:02d}/{mes:02d}/{ano}'

            if dia > 31 or dia < 1 or mes > 12 or mes < 1 or ano > datetime.now().year or ano < 1900:
                print(f'\033[1;31mDATA: {data_nascimento} Inválida!\n[DIGITE 0 PARA SAIR]\033[m')
                continue
            # Verificamos se a data de nascimento não passa dos limites
                

            print('\033[1;36mAGORA DIGITE O SEU NOME DE USUÁRIO E A SUA SENHA DO BANCO\033[m')
            usuario = input('Usuário: ')
            senha = getpass.getpass('Senha: ')
            saldo = 0
            # Aqui criamos o usuario e a sua senha

            cur.execute('SELECT * FROM banco WHERE usuario = ?', (usuario,))
            existe = cur.fetchone()
            # Verificamos se o usuário já existe

            if existe:
                print('❌ Erro: Este usuário já está cadastrado.')
                sleep(2.5)
                os.system('cls')
                
            else:
                try:
                    cur.execute('INSERT INTO banco (nome, data_nascimento, usuario, senha, saldo) VALUES (?, ?, ?, ?, ?)',
                                (nome, data_nascimento, usuario, senha, saldo))
                    con.commit()
                    print('\033[1;32m✅ Cadastro realizado com sucesso!\033[m')
                    # Adicionamos os dados do cliente no nosso BD
                    sleep(2.5)
                    os.system('cls')
                    break
                    
                except Exception as e:
                    print('\033[1;31m❌ Erro ao cadastrar:\033[m', e)
                    sleep(2.5)
                    os.system('cls')                 