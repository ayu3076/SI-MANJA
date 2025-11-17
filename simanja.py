import os
import csv 
import pandas as pd
from tabulate import tabulate
from datetime import datetime 

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
    
def validasi_tanggal(tanggal):
    try:
        datetime.strptime(tanggal, "%Y-%m-%d")
        return True
    except ValueError:
        return False

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
        '   [ 3 ] Tampilkan Data User\n'
        '   [ 4 ] Logout'
    )

    while True:
        opsi = input('Masukkan menu yang anda pilih : ').lower().strip()
        if opsi == '1' or opsi == 'registrasi manajer' :
            return df_registrasi_manajer()
        elif opsi == '2' or opsi == 'login manajer' :
            return df_login()
        elif opsi == '3' or opsi == 'tampilkan data user':
            data_user = pd.read_csv('user.csv')
            print(tabulate(data_user, headers = 'keys', tablefmt = 'grid'))
            return df_menuadmin()
        elif opsi == '4' or opsi == 'logout' :
            return df_homepage()
        else :
            print('Inputan tidak valid!')
            input('\nSilahkan tekan Enter untuk kembali ke menu sebelumnya....')
            return df_menuadmin()


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
        '   [ 1 ] Kelola Akun\n'
        '   [ 2 ] Data Spesies\n'
        '   [ 3 ] Input Data Penjualan\n'
        '   [ 4 ] Kelola Data Panen Keseluruhan\n'
        '   [ 5 ] Laporan & Rekap\n'
        '   [ 6 ] Logout'
    )
    opsi = input('Masukkan menu yang anda pilih : ').lower()
    while True:
        if opsi == '1' or opsi == 'kelola akun':
            return df_edit_akun_manajer()
        elif opsi == '2' or opsi == 'data spesies':
            return df_data_spesies()
        elif opsi == '3' or opsi == 'input data penjualan':
            return df_input_penjualan()
        elif opsi == '4' or opsi == 'kelola data panen keseluruhan':
            return df_kelola_panen_keseluruhan()
        elif opsi == '5' or opsi == 'laporan & rekap':
            return df_laporan_rekap()
        elif opsi == '6' or opsi == 'logout':
            return df_homepage()
        else :
            print('Inputan tidak valid!')
            input('\nSilahkan tekan Enter untuk kembali ke menu sebelumnya.')
            return df_menumanajer()
    



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
    print('--------------------[  MENU STAF ]--------------------')
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
        print('-------------------[  MENU PANEN ]--------------------')
        print(
            '   [ 1 ] Tampilkan Data Panen\n'
            '   [ 2 ] Tambahkan Data Panen\n'
            '   [ 3 ] Ubah Data Panen\n'
            '   [ 4 ] Hapus Data Panen\n'
            '   [ 5 ] Statistik Panen\n'
            '   [ 6 ] Kembali'
        )

        opsi = input('Masukkan menu yang anda pilih : ').lower()

        # ---- [ 1 ] TAMPILKAN DATA PANEN ----
        if opsi == '1' or opsi == 'tampilkan data panen':
                os.system('cls')
                print('╔════════════════════════════════════════╗')
                print('║-------------[ DATA PANEN ]-------------║')
                print('╚════════════════════════════════════════╝')
                print()
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
                            df_display = df_filtered.copy()
                            df_display.insert(0, "No", range(1, len(df_display) + 1))
                            print(tabulate(df_display, headers='keys', tablefmt='fancy_grid', showindex=False))
                    else:
                    # Jika manajer, tampilkan semua data
                        print('Data Panen Seluruh Akun:\n')
                        df_display = df.copy()
                        df_display.insert(0, "No", range(1, len(df_display) + 1))
                        print(tabulate(df_display, headers='keys', tablefmt='fancy_grid', showindex= False))

                input('\nTekan Enter untuk kembali...')

        # ---- [ 2 ] TAMBAH DATA PANEN ----  
        elif opsi == '2' or opsi == 'tambah data panen':
                os.system('cls')
                print('╔════════════════════════════════════════╗')
                print('║-------------[ DATA PANEN ]-------------║')
                print('╚════════════════════════════════════════╝')
                print()
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
                while True:
                    tanggal = input('Masukkan Tanggal (YYYY-MM-DD): ')
                    if validasi_tanggal(tanggal):
                        break
                    print('Format tanggal tidak valid! Gunakan YYYY-MM-DD.')

                spesies = input('Masukkan Spesies Tembakau: ')
                
                while True:
                    jumlah = input('Masukkan Jumlah Bandang: ')
                    if jumlah.isdigit() and int(jumlah) > 0 :
                        break
                    print('Jumlah harus angka!')

                while True:
                    biaya = input('Masukkan Biaya Operasional (Rp): ')
                    if biaya.isdigit() and float(biaya) >= 0:
                        break
                    print('Biaya harus angka!')

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

        # ---- [ 3 ] UBAH DATA PANEN ----         
        elif opsi == '3' or opsi == 'ubah data panen':
            os.system('cls')
            print('╔════════════════════════════════════════╗')
            print('║-------------[ DATA PANEN ]-------------║')
            print('╚════════════════════════════════════════╝')
            print()
            full_df = pd.read_csv('data_panen.csv')

            # Jika staf, hanya bisa ubah datanya sendiri
            if rolelogin.lower() == 'staf':
                df = full_df[full_df['Username'] == usernamelogin]
            else:
                df = full_df.copy()

            if df.empty:
                input('Tidak ada data yang dapat diubah. Tekan Enter untuk kembali...')
                continue

            df_display = df.copy()
            df_display.insert(0, "No", range(1, len(df_display) + 1))
            print(tabulate(df_display, headers='keys', tablefmt='fancy_grid', showindex=False))
            id_edit = input('\nMasukkan ID Panen yang ingin diubah: ').lower()

            if id_edit in df['ID Panen'].values:
                print('\nMasukkan data baru (kosongkan jika tidak ingin mengubah): ')
                while True:
                    tanggal = input('Masukkan Tanggal Baru (YYYY-MM-DD): ')
                    if validasi_tanggal(tanggal):
                        break
                    print('Format tanggal tidak valid! Gunakan YYYY-MM-DD.')

                spesies = input('Spesies baru: ')

                while True:
                    jumlah = input('Masukkan Jumlah Bandang Baru: ')
                    if jumlah.isdigit() and int(jumlah) > 0 :
                        break
                    print('Jumlah harus angka!')

                while True:
                    biaya = input('Masukkan Biaya Operasional Baru (Rp): ')
                    if biaya.isdigit() and float(biaya) >= 0:
                        break
                    print('Biaya harus angka!')

                # update data
                if tanggal: 
                    full_df.loc[full_df['ID Panen'] == id_edit, 'Tanggal'] = tanggal
                if spesies: 
                    full_df.loc[full_df['ID Panen'] == id_edit, 'Spesies'] = spesies
                if jumlah: 
                    full_df.loc[full_df['ID Panen'] == id_edit, 'Jumlah Bandang'] = jumlah
                if biaya: 
                    full_df.loc[full_df['ID Panen'] == id_edit, 'Biaya Operasional'] = biaya

                full_df.to_csv('data_panen.csv', index=False)
                input('\nData berhasil diperbarui! Tekan Enter untuk kembali....')

            else:
                input('ID Panen tidak ditemukan! Tekan Enter untuk kembali....')

        # ---- [ 4 ] HAPUS DATA PANEN ---- 
        elif opsi == '4' or opsi == 'hapus data panen':
            os.system('cls')
            print('╔════════════════════════════════════════╗')
            print('║-------------[ DATA PANEN ]-------------║')
            print('╚════════════════════════════════════════╝')
            print()
            full_df = pd.read_csv('data_panen.csv')

            # Batasi staf hanya bisa hapus datanya sendiri
            if rolelogin.lower() == 'staf':
                df = full_df[full_df['Username'] == usernamelogin]
            else:
                df = full_df.copy()

            if df.empty:
                input('Tidak ada data yang dapat dihapus. Tekan Enter untuk kembali...')
                continue

            df_display = df.copy()
            df_display.insert(0, "No", range(1, len(df_display) + 1))
            print(tabulate(df_display, headers='keys', tablefmt='fancy_grid', showindex=False))

            id_hapus = input('\nMasukkan ID Panen yang ingin dihapus: ').lower()

            if id_hapus in df['ID Panen'].values:
                full_df = full_df[full_df['ID Panen'] != id_hapus]
                full_df.to_csv('data_panen.csv', index=False)
                input('\nData berhasil dihapus! Tekan Enter untuk kembali....')
            else:
                input('ID Panen tidak ditemukan! Tekan Enter untuk kembali....')

        # ---- [ 5 ] STATISTIK PANEN ----
        elif opsi == '5' or opsi == 'statistik panen':
            return df_statistik_panen()
        
        # ---- [ 6 ] KEMBALI ----
        elif opsi == '6' or opsi == 'kembali':
            return df_menustaf() 

        else:
            input('Input tidak valid! Tekan Enter untuk coba lagi...')

def df_statistik_panen():
    global usernamelogin, rolelogin
    os.system('cls')

    print('-' * 30 + '[ STATISTIK PANEN ]' + '-' * 30)
    print(f'\nPengguna : {usernamelogin}\n')

    df = pd.read_csv('data_panen.csv')

    # Filter untuk staf → hanya datanya sendiri
    if rolelogin.lower() == 'staf':
        df = df[df['Username'] == usernamelogin]

    if df.empty:
        input('Belum ada data panen! Tekan Enter untuk kembali...')
        return

    # Konversi tipe data
    df['Jumlah Bandang'] = pd.to_numeric(df['Jumlah Bandang'], errors='coerce')
    df['Biaya Operasional'] = pd.to_numeric(df['Biaya Operasional'], errors='coerce')
    df['Tanggal'] = pd.to_datetime(df['Tanggal'], errors='coerce')

    # Hitungan dasar
    total_bandang = df['Jumlah Bandang'].sum()
    total_biaya = df['Biaya Operasional'].sum()
    rata_bandang = df['Jumlah Bandang'].mean()
    jumlah_entri = len(df)

    # Panen terlama & terbaru
    panen_terlama = df['Tanggal'].min().date()
    panen_terbaru = df['Tanggal'].max().date()

    # Konversi Bandang → KG
    total_kg = total_bandang * 12  # 1 bandang = 12 kg

    # ⬇ Tampilan rapi
    print(f"Total Panen (Bandang)      : {total_bandang}")
    print(f"Total Panen (Kg)            : {total_kg:,} kg")
    print(f"Total Biaya Operasional     : Rp {total_biaya:,.0f}")
    print(f"Rata-rata Jumlah Bandang    : {rata_bandang:.1f}")
    print(f"Jumlah Entri Panen          : {jumlah_entri}")
    print(f"Panen Terlama               : {panen_terlama}")
    print(f"Panen Terbaru               : {panen_terbaru}")
    print('-' * 70)

    input('\nTekan Enter untuk kembali...')
    return df_panen()




df_homepage()