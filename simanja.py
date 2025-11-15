import os
import csv 
import pandas as pd
from tabulate import tabulate 

usernamelogin = None
rolelogin = None

# pengecekan FILE untuk fitur User Staf

try:
    pd.read_csv('data_panen.csv')
except FileNotFoundError :
    df = pd.DataFrame({'ID Panen': [], 
                       'Username': [], 
                       'Tanggal': [], 
                       'Spesies': [], 
                       'Jumlah Bandang': [], 
                       'Biaya Operasional': []})
    df[['Spesies']].astype(str)
    df.to_csv('data_panen.csv', index = False)

try :
    pd.read_csv('data_penjualan.csv')
except FileNotFoundError :
    df = pd.DataFrame({'ID Transaksi': [], 
                       'Tanggal': [], 
                       'ID Panen': [], 
                       'Kuantitas (kg)': [],
                       'Harga Jual/kg': []})
    df.to_csv('data_penjualan.csv', index = False)


try :
    pd.read_csv('data_spesies.csv')
except FileNotFoundError :
    df = pd.DataFrame({'ID Spesies': [], 
                       'Nama Spesies': []})
    df[['Nama Spesies']].astype(str)


try :
    # baca file ke df supaya kita bisa cek isinya
    df = pd.read_csv('user.csv')
    # jika admin belum ada, tambahkan
    if 'admin' not in df['Username'].astype(str).values:
        df.loc[len(df)] = ['admin', '@Admin123', 'admin']
        df.to_csv('user.csv', index=False)

except FileNotFoundError :
    # jika file belum ada, buat dengan header dan tambahkan admin
    df = pd.DataFrame({
        'Username': [],
        'Password': [],
        'Role': []
    })
    df.loc[len(df)] = ['admin', '@Admin123', 'admin']
    df.to_csv('user.csv', index=False)
    

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
    print('--------------------[  MENU HOME ]--------------------')
    print('[ 1 ]  Login sebagai Admin')
    print('[ 2 ]  Login sebagai Staf')
    print('[ 3 ]  Registrasi Staf')
    print()

    pilihan = input('Masukkan menu pilihan: ').lower()
    if pilihan == '1' or pilihan == 'login sebagai admin' :
        df_login() # role admin
    elif pilihan == '2' or pilihan == 'login sebagai staf' :
        df_login() # role staf
    elif pilihan == '3' or pilihan == 'registrasi staf' :
        df_registrasi()
    else :
        input('Pilihan tidak valid, tekan Enter untuk melanjutkan')
        df_homepage()

def df_registrasi():
    os.system('cls')
    print('╔════════════════════════════════════════╗')
    print('║-----------[  REGISTER STAF  ]----------║')
    print('╚════════════════════════════════════════╝') 

    dfuser = pd.read_csv('user.csv')
    username = input("Masukkan username staf: ")
    if len(username) < 4 :
        input('Username minimal 4 huruf. Tekan Enter untuk melanjutkan....')
        df_registrasi()

    elif username in dfuser['Username'].values:
        print("Username sudah ada!")
        input("Tekan Enter...")
        return df_homepage()  

    while True :
        password = input('Masukkan Password (password minimal 8 karakter, mengandung angka, simbol, huruf besar, dan huruf kecil): ')
        simbol = '!@#$%^&*()' # mendefinisikan karakter simbol

        if len(password) < 8:
            print('Password minimal 8 karakter.')
            continue

        ada_huruf_besar = False
        ada_huruf_kecil = False
        ada_angka = False
        ada_simbol = False

        for karakter in password:
            if karakter.isupper():
                ada_huruf_besar = True
            elif karakter.islower():
                ada_huruf_kecil = True
            elif karakter.isdigit():
                ada_angka = True


            if karakter in simbol:
                ada_simbol = True

        # Jika ada kekurangan, beri feedback spesifik
        missing = []
        if not ada_huruf_besar:
            missing.append('huruf BESAR')
        if not ada_huruf_kecil:
            missing.append('huruf kecil')
        if not ada_angka:
            missing.append('angka')
        if not ada_simbol:
            missing.append('simbol (mis. !@#$%^&*())')

        if missing:
            print('Password tidak valid — harus mengandung: ' + ', '.join(missing) + '.')
            # ulangi input password
            continue
        else: 
            print("Password valid.")
            break

        
    while True :
        cek = input('Apakah Username dan Password sudah sesuai? ( y / t ): ').lower()
        if cek == 'y' :
            dfuser.loc[len(dfuser)] = [username, password, 'staf']
            dfuser.to_csv('user.csv', index=False)
            print('Registrasi berhasil! Silahkan login.')
            input('\nTekan Enter untuk melanjutkan....')
            return df_homepage()
        elif cek == 't' :
            input('Silahkan tekan Enter untuk melakukan registrasi ulang....')
            return df_registrasi()
        else :
            print('Input tidak valid. Silahkan ulangi....')

def df_registrasi_manajer():
    os.system('cls')
    print('╔════════════════════════════════════════╗')
    print('║---------[  REGISTER MANAJER ]----------║')
    print('╚════════════════════════════════════════╝') 

    dfuser = pd.read_csv('user.csv')
    username = input("Masukkan username manajer: ")
    if len(username) < 4 :
        input('Username minimal 4 huruf. Tekan Enter untuk melanjutkan....')
        df_registrasi_manajer()

    elif username in dfuser['Username'].values:
        print("Username sudah ada!")
        input("Tekan Enter...")
        return df_menuadmin()  

    while True :
        password = input('Masukkan Password (password minimal 8 karakter, mengandung angka, simbol, huruf besar, dan huruf kecil): ')
        simbol = '!@#$%^&*()' # mendefinisikan karakter simbol

        if len(password) < 8:
            print('Password minimal 8 karakter.')
            continue

        ada_huruf_besar = False
        ada_huruf_kecil = False
        ada_angka = False
        ada_simbol = False

        for karakter in password:
            if karakter.isupper():
                ada_huruf_besar = True
            elif karakter.islower():
                ada_huruf_kecil = True
            elif karakter.isdigit():
                ada_angka = True


            if karakter in simbol:
                ada_simbol = True

        # Jika ada kekurangan, beri feedback spesifik
        missing = []
        if not ada_huruf_besar:
            missing.append('huruf BESAR')
        if not ada_huruf_kecil:
            missing.append('huruf kecil')
        if not ada_angka:
            missing.append('angka')
        if not ada_simbol:
            missing.append('simbol (mis. !@#$%^&*())')

        if missing:
            print('Password tidak valid — harus mengandung: ' + ', '.join(missing) + '.')
            # ulangi input password
            continue
        else: 
            print("Password valid.")
            break
        

    while True :
        cek = input('Apakah Username dan Password sudah sesuai? ( y / t ): ').lower()
        if cek == 'y' :
            dfuser.loc[len(dfuser)] = [username, password, 'manajer']
            dfuser.to_csv('user.csv', index=False)
            print('Registrasi berhasil! Silahkan login.')
            input('\nTekan Enter untuk melanjutkan....')
            return df_menuadmin()
        elif cek == 't' :
            input('Silahkan tekan Enter untuk melakukan registrasi ulang....')
            return df_registrasi_manajer()
        else :
            print('Input tidak valid. Silahkan ulangi....')
                
    

def df_login():
    while True:
        global usernamelogin, rolelogin 
        os.system('cls')
        print('╔════════════════════════════════════════╗')
        print('║----------------[ LOGIN ]---------------║')
        print('╚════════════════════════════════════════╝')

        while True:
            username = input('Masukkan Username : ').strip()
            password = input('Masukkan Password : ')

            loginsukses = False

            with open('user.csv', mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # gunakan strip() untuk menghindari spasi tak terduga
                    if str(row.get('Username', '')).strip() == username and str(row.get('Password', '')).strip() == password:
                        usernamelogin = row.get('Username').strip()   # simpan username global
                        rolelogin = row.get('Role').strip().lower()  # simpan role global (lower biar konsisten)
                        loginsukses = True
                        break

            if loginsukses:
                print(f"\nLogin berhasil! Selamat datang, {usernamelogin} ({rolelogin})")
                input('\nTekan Enter untuk melanjutkan...')
                # arahkan ke menu sesuai role
                if rolelogin == 'staf':
                    return df_menustaf()
                elif rolelogin == 'manajer':
                    return df_menumanajer()
                elif rolelogin == 'admin':
                    return df_menuadmin()
                else:
                    print("Role tidak dikenali, kembali ke halaman utama...")
                    input('\nTekan Enter untuk melanjutkan...')
                    return df_homepage()
                
            else:
                print('\nUsername atau password salah!')
                input('\nTekan Enter untuk mencoba lagi...')
                continue

def df_menumanajer():
    global usernamelogin
    os.system('cls')
    print('╔════════════════════════════════════════════════════╗')
    print('║  ╔══════════════════════════════════════════════╗  ║')
    print('║  ║     Sistem Manajemen Panen dan Penjualan     ║  ║')
    print('║  ║                                              ║  ║')
    print('║  ║        --------[  SI MANJA  ]-------         ║  ║')
    print('║  ╚══════════════════════════════════════════════╝  ║')
    print('╚════════════════════════════════════════════════════╝')
    print()
    print('------------------[  MENU MANAJER  ]------------------')
    print(
        '   [ 1 ] Registrasi Manajer\n'
        '   [ 2 ] Login Manajer\n'
        '   [ 3 ] Logout'
    )


def df_menuadmin():
    global usernamelogin
    os.system('cls')
    print('╔════════════════════════════════════════════════════╗')
    print('║  ╔══════════════════════════════════════════════╗  ║')
    print('║  ║     Sistem Manajemen Panen dan Penjualan     ║  ║')
    print('║  ║                                              ║  ║')
    print('║  ║        --------[  SI MANJA  ]-------         ║  ║')
    print('║  ╚══════════════════════════════════════════════╝  ║')
    print('╚════════════════════════════════════════════════════╝')
    print()
    print('-------------------[  MENU ADMIN  ]-------------------')
    print(
        '   [ 1 ] Registrasi Manajer\n'
        '   [ 2 ] Login Manajer\n'
        '   [ 3 ] Logout'
    )

    while True:
        opsi = input('Masukkan menu yang anda pilih : ').lower().strip()
        if opsi == '1' or opsi == 'registrasi manajer' :
            return df_registrasi_manajer()
        elif opsi == '2' or opsi == 'login manajer' :
            return df_login()
        elif opsi == '3' or opsi == 'logout' :
            return df_homepage()
        else :
            print('Inputan tidak valid!')
            input('\nSilahkan tekan Enter untuk kembali ke menu sebelumnya....')
            return df_menuadmin()


def df_menustaf():
    global usernamelogin
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
    print(
        '   [ 1 ] Kelola Akun\n'
        '   [ 2 ] Kelola Data Panen\n'
        '   [ 3 ] Logout'
    )
    while True :
        opsi = input('Masukkan menu yang anda pilih : ').lower()
        if opsi == '1' or opsi == 'kelola akun' :
            os.system('cls')
            df_kelolaakunpribadi()
        elif opsi == '2' or opsi == 'kelola data panen' :
            os.system('cls')
            df_panen()
        elif opsi == '3' or opsi == 'logout' :
            return df_homepage()
        else :
            print('Inputan tidak valid!')
            input('\nSilahkan tekan Enter untuk kembali ke menu sebelumnya.')
            return df_menustaf()

def df_kelolaakunpribadi() :
    global usernamelogin, rolelogin
    os.system('cls')
    print('╔════════════════════════════════════════════════════╗')
    print('║  ╔══════════════════════════════════════════════╗  ║')
    print('║  ║     Sistem Manajemen Panen dan Penjualan     ║  ║')
    print('║  ║                                              ║  ║')
    print('║  ║        --------[  SI MANJA  ]-------         ║  ║')
    print('║  ╚══════════════════════════════════════════════╝  ║')
    print('╚════════════════════════════════════════════════════╝')
    print()
    df = pd.read_csv('user.csv')
    data_user = df[df['Username'] == usernamelogin]
    print('-------------------[  EDIT AKUN  ]--------------------')
    print('\nData akun anda:')
    print(tabulate(data_user, headers = 'keys', tablefmt = 'grid'))
    print(
            '   [ 1 ] Edit Username\n'
            '   [ 2 ] Edit Password\n'
            '   [ 3 ] Kembali\n'
        )
    opsi = input('Pilih menu: ').lower()

    # --- EDIT USERNAME ---
    if opsi == '1' or opsi == 'edit username':
        os.system('cls')
        print('╔════════════════════════════════════════╗')
        print('║------------[ EDIT USERNAME ]-----------║')
        print('╚════════════════════════════════════════╝')
        print('\nData akun anda:')
        print(tabulate(data_user, headers = 'keys', tablefmt = 'grid'))
        while True:

            new_user = input('Masukkan username baru: ')

            # cek username sudah ada atau belum
            if new_user in df['Username'].values:
                print('Username sudah digunakan!')
                continue
            elif len(new_user) < 4:
                input('Username minimal 4 huruf. Tekan Enter untuk melanjutkan....')
                continue
            else:
                df.loc[df['Username'] == usernamelogin, 'Username'] = new_user
                df.to_csv('user.csv', index = False)

                usernamelogin = new_user # update global username
                print('Username berhasil diubah!')
                return df_kelolaakunpribadi()
            
    # --- EDIT PASSWORD ---   
    elif opsi == '2' or opsi == 'edit password':
        os.system('cls')
        print('╔════════════════════════════════════════╗')
        print('║------------[ EDIT PASSWORD ]-----------║')
        print('╚════════════════════════════════════════╝')
        print('\nData akun anda:')
        print(tabulate(data_user, headers = 'keys', tablefmt = 'grid'))

        while True: 
            new_pass = input('Masukkan Password (password minimal 8 karakter, mengandung angka, simbol, huruf besar, dan huruf kecil): ')
            simbol = '!@#$%^&*()' # mendefinisikan karakter simbol

            if len(new_pass) < 8:
                print('Password minimal 8 karakter.')
                continue

            ada_huruf_besar = False
            ada_huruf_kecil = False
            ada_angka = False
            ada_simbol = False

            for karakter in new_pass:
                if karakter.isupper():
                    ada_huruf_besar = True
                elif karakter.islower():
                    ada_huruf_kecil = True
                elif karakter.isdigit():
                    ada_angka = True


                if karakter in simbol:
                    ada_simbol = True

            # Jika ada kekurangan, beri feedback spesifik
            missing = []
            if not ada_huruf_besar:
                missing.append('huruf BESAR')
            if not ada_huruf_kecil:
                missing.append('huruf kecil')
            if not ada_angka:
                missing.append('angka')
            if not ada_simbol:
                missing.append('simbol (mis. !@#$%^&*())')

            if missing:
                print('Password tidak valid — harus mengandung: ' + ', '.join(missing) + '.')
                # ulangi input password
                continue
            else: 
                print("Password valid.")
                break

        df.loc[df['Username'] == usernamelogin, 'Password'] = new_pass
        df.to_csv('user.csv', index = False)
        return df_kelolaakunpribadi()
    
    elif opsi == '3' or opsi == 'kembali':
        return df_menustaf()
    
    else:
        print('Inputan tidak valid. Tekan Enter....')
        return df_kelolaakunpribadi()



# def df_kelolaakun():
#     while True:
#         global usernamelogin, rolelogin
#         os.system('cls')
#         print('╔════════════════════════════════════════════════════╗')
#         print('║  ╔══════════════════════════════════════════════╗  ║')
#         print('║  ║     Sistem Manajemen Panen dan Penjualan     ║  ║')
#         print('║  ║                                              ║  ║')
#         print('║  ║        --------[  SI MANJA  ]-------         ║  ║')
#         print('║  ╚══════════════════════════════════════════════╝  ║')
#         print('╚════════════════════════════════════════════════════╝')
#         print()
#         print('----------------------[  MENU  ]----------------------')
#         print(
#             '   [ 1 ] Tampilkan Data Akun\n'
#             '   [ 2 ] Ubah Username\n'
#             '   [ 3 ] Ubah Password\n'
#             '   [ 4 ] Ubah Role\n'
#             '   [ 5 ] Kembali'
#         )
#         menu = input('Pilih menu: ').lower()
#         if menu == '1' or menu == 'tampilkan data akun' :
#             os.system('cls')
#             df = pd.read_csv('user.csv')
#             print(tabulate(df[['Username', 'Role']], headers = 'keys', tablefmt='fancy_grid'))
#             input('Tekan Enter untuk kembali!')
#             return df_kelolaakun()

#         elif menu == '2' or menu == 'ubah username' :
#             os.system('cls')
#             df = pd.read_csv('user.csv')
#             df = df[['Username', 'Role']]
#             print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
#             username = input('Masukkan username yang ingin diubah: ')
#             if username in df['Username'].values: 
#                 while True:
#                     username_baru = input('Masukkan Username Baru: ')
#                     if username_baru not in df['Username'].values:
#                         df.loc[df['Username'] == username, 'Username'] = username_baru
#                         df.to_csv('user.csv', index = False)
#                         input('Username berhasil diubah!')
#                         return df_kelolaakun()
#                     else :
#                         print('Username sudah digunakan, silahkan pilih username lain!')
#                         continue

#         elif menu == '3' or menu == 'ubah password' :
#             os.system('cls')
#             df = pd.read_csv('user.csv')
#             df = df[['Username', 'Role']]
#             print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
#             username = input('Masukkan username yang ingin diubah passswordnya: ')
#             if username in df['Username'].values:
#                 while True:
#                     password_baru = input('Masukkan Password Baru (min. 8 karakter)')
#                     # validasi panjang password
#                     if len(password_baru) >= 8:
#                         df.loc[df['Username'] == username, 'Password'] = password_baru
#                         df.to_csv('user.csv', index = False)
#                         input('Password berhasil diubah! Tekan Enter untuk kembali....')
#                         return df_kelolaakun()
#                     else :
#                         print('Password terlalu pendek! Minimal 8 karakter!')
#             else :
#                 print('Username tidak ditemukan!')
#                 input('Tekan Enter untuk kembali....')
#                 return df_kelolaakun()
            
#         elif menu == '4' or menu == 'ubah role' :
#             os.system('cls')
#             df = pd.read_csv('user.csv')
#             df = df[['Username', 'Role']]
#             print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
#             username = input('Masukkan username yang ingin diubah passswordnya: ')
#             if username in df['Username'].values:
#                 while True:
#                     role_baru = input('Masukkan Role Baru: (Staf / Manajer)')
#                     if role_baru in ['staf', 'manajer']:
#                         df.loc[df['Username'] == username, 'Role'] = role_baru
#                         df.to_csv('user.csv', index = False)
#                         input('Role berhasil diubah! Tekan Enter untuk kembali....')
#                         return df_kelolaakun()
#                     else : 
#                         print('Role tidak valid! Masukkan hanya "staf" atau "manajer". ')
#             else :
#                 print('Username tidak ditemukan!')
#                 input('Tekan Enter untuk kembali....')
#                 return df_kelolaakun() 
            
#         elif menu == '5' or menu == 'keluar':
#             os.system('cls')
#             df_menustaf()

#         else:
#             print('Input tidak valid!')
#             input('Tekan Enter untuk kembali....')
#             break
         

def df_panen():
    while True:
        global usernamelogin, rolelogin
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
        print(
            '   [ 1 ] Tampilkan Data Panen\n'
            '   [ 2 ] Tambahkan Data Panen\n'
            '   [ 3 ] Ubah Data Panen\n'
            '   [ 4 ] Hapus Data Panen\n'
            '   [ 5 ] Kembali'
        )
        opsi = input('Masukkan menu yang anda pilih : ').lower()
        if opsi == '1' or opsi == 'tampilkan data panen':
                os.system('cls')
                df = pd.read_csv('data_panen.csv')
                if df.empty:
                    print('Belum ada data panen.')
                else:
                    if rolelogin.lower() == 'staf':
                        df_filtered = df[df['Username'] == usernamelogin]
                        if df_filtered.empty:
                            print('Belum ada data panen untuk akun ini.')

                        else:
                            print(f"Data Panen untuk pengguna: {usernamelogin}\n")
                            print(tabulate(df_filtered, headers='keys', tablefmt='fancy_grid'))
                    else:
                    # Jika manajer, tampilkan semua data
                        print('Data Panen Seluruh Akun:\n')
                        print(tabulate(df, headers='keys', tablefmt='fancy_grid'))

                input('\nTekan Enter untuk kembali...')

            
        elif opsi == '2' or opsi == 'tambah data panen':
                os.system('cls')
                df = pd.read_csv('data_panen.csv')
                
                # buat ID otomatis
                if df.empty:
                    new_id = 'PN001'
                else:
                    last_id = df['ID Panen'].iloc[-1]
                    num = int(last_id[2:]) + 1
                    new_id = f'PN{num:03d}'

                # ambil username dari login
                username = usernamelogin
                tanggal = input('Masukkan Tanggal (YYYY-MM-DD): ')
                spesies = input('Masukkan Spesies Tembakau: ')
                jumlah = input('Masukkan Jumlah Bandang: ')
                biaya = input('Masukkan Biaya Operasional (Rp): ')

                # Tambahkan data baru ke DataFrame
                new_data = {
                    'ID Panen': new_id,
                    'Username': username,
                    'Tanggal': tanggal,
                    'Spesies': spesies,
                    'Jumlah Bandang': jumlah,
                    'Biaya Operasional': biaya
                }
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                df.to_csv('data_panen.csv', index=False)
                input('\nData Penen berhasil ditambahkan! Tekan Enter untuk kembali....')
        elif opsi == '3' or opsi == 'ubah data panen':
            os.system('cls')
            df = pd.read_csv('data_panen.csv')

            # Jika staf, hanya bisa ubah datanya sendiri
            if rolelogin.lower() == 'staf':
                df = df[df['Username'] == usernamelogin]

            if df.empty:
                input('Tidak ada data yang dapat diubah. Tekan Enter untuk kembali...')
                continue

            print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
            id_edit = input('\nMasukkan ID Panen yang ingin diubah: ')

            if id_edit in df['ID Panen'].values:
                idx = df.index[df['ID Panen'] == id_edit][0]
                print('\nData saat ini: ')
                print(df.loc[idx])
                print('\nMasukkan data baru (kosongkan jika tidak ingin mengubah): ')
                tanggal = input('Tanggal baru: ')
                spesies = input('Spesies baru: ')
                jumlah = input('Jumlah Bandang baru: ')
                biaya = input('Biaya Operasional baru: ')

                if tanggal: df.at[idx, 'Tanggal'] = tanggal
                if spesies: df.at[idx, 'Spesies'] = spesies
                if jumlah: df.at[idx, 'Jumlah Bandang'] = jumlah
                if biaya: df.at[idx, 'Biaya Operasional'] = biaya

                full_df = pd.read_csv('data_panen.csv')
                full_df.update(df)
                full_df.to_csv('data_panen.csv', index=False)
                input('\nData berhasil diperbarui! Tekan Enter untuk kembali....')
            else:
                input('ID Panen tidak ditemukan! Tekan Enter untuk kembali....')

        elif opsi == '4' or opsi == 'hapus data panen':
            os.system('cls')
            df = pd.read_csv('data_panen.csv')

            # Batasi staf hanya bisa hapus datanya sendiri
            if rolelogin.lower() == 'staf':
                df = df[df['Username'] == usernamelogin]

            if df.empty:
                input('Tidak ada data yang dapat dihapus. Tekan Enter untuk kembali...')
                continue

            print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
            id_hapus = input('\nMasukkan ID Panen yang ingin dihapus: ')

            if id_hapus in df['ID Panen'].values:
                df = df[df['ID Panen'] != id_hapus]
                df.to_csv('data_panen.csv', index=False)
                input('\nData berhasil dihapus! Tekan Enter untuk kembali....')
            else:
                input('ID Panen tidak ditemukan! Tekan Enter untuk kembali....')

        elif opsi == '5' or opsi == 'kembali':
            break

        else:
            input('Input tidak valid! Tekan Enter untuk coba lagi...')





df_homepage()