import os
import csv 
import pandas as pd
from tabulate import tabulate 

# pengecekan FILE untuk fitur User Staf

try:
    pd.read_csv('data_panen.csv')
except FileNotFoundError :
    df = pd.DataFrame({'ID Panen': [], 'Username': [], 'Tanggal': [], 'Spesies': [], 'Jumlah Karung': [], 'Biaya Oprasional': []})
    df[['Spesies']].astype(str)
    df.to_csv('data_panen.csv', index = False)


try :
    pd.read_csv('data_penjualan.csv')
except FileNotFoundError :
    df = pd.DataFrame({'ID Transaksi': [], 'Tanggal': [], 'ID Panen': [], 'Kuantitas (kg)': [],'Harga Jual/kg': []})
    df.to_csv('data_penjualan.csv', index = False)


try :
    pd.read_csv('data_spesies.csv')
except FileNotFoundError :
    df = pd.DataFrame({'ID Spesies': [], 'Nama Spesies': []})
    df[['Nama Spesies']].astype(str)
    

try :
    pd.read_csv('user.csv')
except FileNotFoundError :
    df = pd.DataFrame({'Username': [], 'Password': [], 'Role' : []})
    df[['Nama Spesies']].astype(str)

def df_homepage():
    os.system('cls')
    print('╔════════════════════════════════════════════════════╗')
    print('║  ╔══════════════════════════════════════════════╗  ║')
    print('║  ║     Sistem Manajemen Panen dan Penjualan     ║  ║')
    print('║  ║                                              ║  ║')
    print('║  ║        --------[  SI MANJA  ]-------         ║  ║')
    print('║  ╚══════════════════════════════════════════════╝  ║')
    print('╚════════════════════════════════════════════════════╝')
    print()
    print('----------------------[  MENU  ]----------------------')
    print('[ 1 ]  Login')
    print('[ 2 ]  Registrasi')
    print()
    pilihan = input('Masukkan menu pilihan: ').lower()
    if pilihan == '1' or pilihan == 'login' :
        df_login()
    elif pilihan == '2' or pilihan == 'registrasi' :
        df_registrasi()
    else :
        input('Pilihan tidak valid, tekan Enter untuk melanjutkan')
        df_homepage()

def df_registrasi():
    os.system('cls')
    print('╔════════════════════════════════════════╗')
    print('║-------------[  REGISTER  ]-------------║')
    print('╚════════════════════════════════════════╝') 
    with open('user.csv', mode= 'r') as file :
        username_sama = {row['Username'] for row in csv.DictReader(file)}

    role = input('Daftar akun sebagai: ').lower()
    if role == 'staf lapangan' or  role == 'manajer':
        username = input('Daftarkan username anda : ')
        if len(username) < 4 :
            input('Username minimal 4 huruf. Tekan Enter untuk melanjutkan')
            df_registrasi()

        elif username in username_sama :
            print('Username sudah terdaftar!')
            input('Tekan Enter untuk melanjutkan.')
            df_registrasi()

        while True :
            password = input('Masukkan Password: ')
            if len(password) < 8 :
                print('Password minimal 8 karakter.')
                continue

            while True :
                cek = input('Apakah Username dan Password sudah sesuai? (y/t): ').lower()
                if cek == 'y' :
                    with open('user.csv', mode='a', newline='') as file :
                        writer = csv.writer(file)
                        writer.writerow([username, password, role])
                    print('Registrasi berhasil! Silahkan login.')
                    input('Tekan Enter untuk melanjutkan.')
                    df_homepage()
                elif cek == 't' :
                    input('Silahkan tekan Enter untuk melakukan registrasi ulang.')
                    df_homepage()
                else :
                    print('Input tidak valid. Silahkan ulangi.')  
    else :
        input('Input tidak valid. Silahkan tekan Enter untuk coba lagi.')
        df_registrasi()

def df_login():
    while True:
        global usernamelogin
        os.system('cls')
        print('╔════════════════════════════════════════╗')
        print('║----------------[ LOGIN ]---------------║')
        print('╚════════════════════════════════════════╝')

        while True:
            username = input('Masukkan Username : ')
            password = input('Masukkan Password : ')
            usernamelogin = username

            df = pd.read_csv('user.csv')
            Data = df[(df['Username'] == username) & (df['Password'] == password)]

            if not Data.empty:
                role = Data['Role'].iloc[0]
                if role == "staff lapangan":
                    print('    Login berhasil! Selamat datang', Data['Username'].iloc[0])
                    input('    Tekan ENTER untuk melanjutkan')
                    df_menustaf()
                elif role == "manajer":
                    print('    Login berhasil! Selamat datang', Data['Username'].iloc[0])
                    input('    Tekan ENTER untuk melanjutkan')
                    df_menumanajer()
            else:
                print('    Password atau Username salah! Silahkan Coba lagi.')
                input('    Tekan ENTER untuk melanjutkan')
                break


    # with open('user.csv', mode='r') as file:
    #     reader = csv.DictReader(file)
    #     for row in reader:
    #         if row['Username'] == username and row['Password'] == password and row['Role'] == 'staff lapangan' :
    #             df_menustaf()
    #         elif row['Username'] == username and row['Password'] == password and row['Role'] == 'manajer' :
    #             df_menumanajer()
    #         else :
    #             print('Username atau Password salah.')
    #             while True:
    #                 cek = input('Apakah anda ingin melanjutkan (y/t) : ').lower()
    #                 if cek == 'y':
    #                     df_login()  
    #                 elif cek == 't':
    #                     input('Silahkan tekan Enter untuk kembali ke menu sebelumnya')
    #                     os.system('cls')
    #                     df_homepage() 
    #                 else:
    #                     print('Inputan invalid')
                

# def login():
#     global usernamelogin
#     os.system('cls')
#     print('╔════════════════════════════════════════╗')
#     print('║------------[ MANAJER LOGIN ]-----------║')
#     print('╚════════════════════════════════════════╝')
#     df_user()
#     username = input('Masukkan Username : ')
#     password = input('Masukkan Password : ')
    

#     with open('user.csv', mode='r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             if row['Username'] == username and row['Password'] == password and row['Role'] == 'staff lapangan' :
#                 usernamelogin = username
#                 df_estaf()
                
                
            

# def df_loginstaf():
#     global usernamelogin
#     os.system('cls')
#     print('╔════════════════════════════════════════╗')
#     print('║-------------[ STAF LOGIN ]-------------║')
#     print('╚════════════════════════════════════════╝')
#     df_user()
#     username = input('Masukkan Username : ')
#     password = input('Masukkan Password : ')

#     loginsukses = False
#     with open('user.csv', mode='r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             if row['Username'] == username and row['Password'] == password :
#                 loginsukses = True
#                 break

    # if loginsukses :
    #     usernamelogin = username
    #     print('Login berhasil.')
    #     input('Tekan Enter untuk melanjutkan.')
    #     os.system('cls')
    #     menustaf()
    # else :
    #     print('Username atau Password salah.')
    #     while True:
    #         cek = input('Apakah anda ingin melanjutkan (y/t) : ').lower()
    #         if cek == 'y':
    #             df_loginstaf()  
    #         elif cek == 't':
    #             input('Silahkan tekan Enter untuk kembali ke menu sebelumnya')
    #             os.system('cls')
    #             df_homepage() 
    #         else:
    #             print('Inputan invalid')




def df_menustaf():
    global usernamelogin
    os.system('cls')
    print('╔════════════════════════════════════════╗')
    print(f'║---[ Selamat Datang {usernamelogin} ]---║')
    print('╚════════════════════════════════════════╝')
    print()
    print(' Pilih menu anda : ')
    print(
        '   [ 1 ] Kelola Akun\n'
        '   [ 2 ] Kelola Data Panen\n'
        '   [ 3 ] Logout'
    )
    while True :
        opsi = input('Masukkan menu yang anda pilih : ').lower()
        if opsi == '1' or opsi == 'kelola akun' :
            os.system('cls')
            df_kelolaakun()
        elif opsi == '2' or opsi == 'kelola data panen' :
            os.system('cls')
            df_panen()
        elif opsi == '3' or opsi == 'logout' :
            exit()
        else :
            print('Inputan tidak valid!')
            input('Silahkan tekan Enter untuk kembali ke menu sebelumnya.')
            df_menustaf()

def df_kelolaakun():
    pass
# def data_panen():
#     if not os.path.exists('data_panen.csv') :
#         with open('data_panen.csv', mode = 'w', newline = '') as file:
#             writer = csv.writer(file)
#             writer.writerow(['ID Panen', 'Username', 'Tanggal', 'Spesies', 'Jumlah Karung', 'Biaya Oprasional'])
            

def df_panen():
    global usernamelogin
    os.system('cls')
    print('╔════════════════════════════════════════╗')
    print('║-----------[ Selamat Datang ]-----------║')
    print('╚════════════════════════════════════════╝')
    print(' Pilih menu anda : ')
    print(
        '   [ 1 ] Tampilkan Data Panen\n'
        '   [ 2 ] Tambahkan Data Panen\n'
        '   [ 3 ] Ubah Data Panen\n'
        '   [ 4 ] Hapus Data Panen\n'
        '   [ 5 ] Kembali'
    )
    while True:
        opsi = input('Masukkan menu yang anda pilih : ').lower()
        if opsi == '1' or opsi == 'tampilkan data panen':
            os.system('cls')
            df = pd.read_csv('data_panen.csv')
            print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
        elif opsi == '2' or opsi == 'tambah data panen':
            os.system('cls')
            df = pd.read('data_panen.csv')
            print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
            id_panen = input('Masukkan ID Panen : ')










def df_menumanajer():
    print('Udalogin')



df_homepage()