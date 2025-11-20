import os
import csv 
import pandas as pd
from tabulate import tabulate
from datetime import datetime 

usernamelogin = None
rolelogin = None

# --- inisialisasi file jika belum ada ---
try:
    pd.read_csv('data_panen.csv')
except FileNotFoundError :
    df = pd.DataFrame({
        'ID Panen': [], 
        'Username': [], 
        'Tanggal': [], 
        'Spesies': [], 
        'Jumlah Bandang': [], 
        'Biaya Operasional': []
    })
    df.to_csv('data_panen.csv', index = False)

try :
    pd.read_csv('data_penjualan.csv')
except FileNotFoundError :
    df = pd.DataFrame({
        'ID Transaksi': [], 
        'Tanggal': [], 
        'ID Panen': [], 
        'Kuantitas (kg)': [],
        'Harga Jual/kg': []
    })
    df.to_csv('data_penjualan.csv', index = False)

try :
    pd.read_csv('data_spesies.csv')
except FileNotFoundError :
    df = pd.DataFrame({
        'ID Spesies': ['SP001', 'SP002', 'SP003', 'SP004'], 
        'Nama Spesies': [
            'Na-Oogst H823',
            'P1A Sumatra',
            'Conshade',
            'Cameron'
        ]
    })
    df.to_csv('data_spesies.csv', index=False)

try :
    df = pd.read_csv('user.csv')
    if 'admin' not in df['Username'].astype(str).values:
        df.loc[len(df)] = ['admin', '@Admin123', 'admin']
        df.to_csv('user.csv', index=False)
except FileNotFoundError :
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
    print('[ 1 ]  Login Admin')
    print('[ 2 ]  Login')
    print('[ 3 ]  Registrasi Staf')
    print()

    pilihan = input('Masukkan menu pilihan: ').lower()
    if pilihan == '1' or pilihan == 'login admin' :
        df_login() # role admin
    elif pilihan == '2' or pilihan == 'login' :
        df_login() # role staf
    elif pilihan == '3' or pilihan == 'registrasi staf' :
        df_registrasi()
    else :
        input('Pilihan tidak valid, tekan Enter untuk melanjutkan')
        df_homepage()


def df_registrasi():
    os.system('cls')
    print('╔════════════════════════════════════════════════════╗')
    print('║  ╔══════════════════════════════════════════════╗  ║')
    print('║  ║     Sistem Manajemen Panen dan Penjualan     ║  ║')
    print('║  ║                                              ║  ║')
    print('║  ║        --------[  SI MANJA  ]-------         ║  ║')
    print('║  ╚══════════════════════════════════════════════╝  ║')
    print('╚════════════════════════════════════════════════════╝')
    print()
    print('--------------[  MENU REGISTRASI (STAF) ]-------------')

    dfuser = pd.read_csv('user.csv')
    username = input("Masukkan username staf: ")
    if len(username) < 4 :
        input('Username minimal 4 huruf. Tekan Enter untuk melanjutkan....')
        return df_registrasi()

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
    print('╔════════════════════════════════════════════════════╗')
    print('║  ╔══════════════════════════════════════════════╗  ║')
    print('║  ║     Sistem Manajemen Panen dan Penjualan     ║  ║')
    print('║  ║                                              ║  ║')
    print('║  ║        --------[  SI MANJA  ]-------         ║  ║')
    print('║  ╚══════════════════════════════════════════════╝  ║')
    print('╚════════════════════════════════════════════════════╝')
    print()
    print('------------[  MENU REGISTRASI (MANAJER) ]------------')

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
            return df_menuadmin()
        else :
            print('Input tidak valid. Silahkan ulangi....')
                
    

def df_login():
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
        print('---------------------[  LOGIN  ]----------------------')

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
                    input('\nTekan Enter untuk mencoba lagi...')
                    return df_homepage()
                
            else:
                print('\nUsername atau password salah!')
                input('\nTekan Enter untuk mencoba lagi...')
                return df_login()


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
        '   [ 2 ] Tampilkan Data User\n' 
        '   [ 3 ] Hapus Data User\n'
        '   [ 4 ] Logout'
    )

    while True:
        opsi = input('Masukkan menu yang anda pilih : ').lower()
        if opsi == '1' or opsi == 'registrasi manajer' :
            return df_registrasi_manajer()
        
        elif opsi == '2' or opsi == 'tampilkan data user' :
            os.system('cls')
            df = pd.read_csv('user.csv')
            disp = df.copy()
            disp.insert(0, 'No', range(1, len(disp) + 1))
            print(tabulate(disp, headers = 'keys', tablefmt = 'grid', showindex=False))
            input('Tekan Enter untuk kembali...')
            return df_menuadmin()
        
        elif opsi == '3' or opsi == 'hapus data user':
            df = pd.read_csv('user.csv')
            disp = df.copy()
            disp.insert(0, 'No', range(1, len(disp) + 1))
            print(tabulate(disp, headers = 'keys', tablefmt = 'grid', showindex=False))

            usn_hapus = input('Masukkan Username yang ingin dihapus: ').strip()
            if usn_hapus in df['Username'].values:
                df = df[df['Username'] != usn_hapus]
                df.to_csv('user.csv', index=False)
                print('Akun berhasil dihapus.')
            else:
                print('Username tidak ditemukan.')
            input('Tekan Enter untuk kembali....')
            return df_menuadmin()
            
        elif opsi == '4' or opsi == 'logout' :
            return df_homepage()
        
        else :
            print('Inputan tidak valid!')
        input('\nSilahkan tekan Enter untuk kembali ke menu sebelumnya....')
        return df_homepage()


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
        '   [ 3 ] Data Penjualan\n'
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
        elif opsi == '3' or opsi == 'data penjualan':
            return df_penjualan()
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
    
def df_edit_akun_manajer():
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
    akun = df[df['Username'] == usernamelogin].copy()
    print('-------------------[  EDIT AKUN  ]--------------------')
    print('\nData akun anda: ')
    print(tabulate(akun, headers = 'keys', tablefmt= 'grid'))
    print(
            '   [ 1 ] Edit Username\n'
            '   [ 2 ] Edit Password\n'
            '   [ 3 ] Kembali\n'
        )
    
    opsi = input('Pilih Menu: ').strip()

    # --- EDIT USERNAME ---
    if opsi == '1' or opsi == 'edit username':
        os.system('cls')
        print('╔════════════════════════════════════════╗')
        print('║------------[ EDIT USERNAME ]-----------║')
        print('╚════════════════════════════════════════╝')
        print('\nData akun anda:')
        print(tabulate(akun, headers = 'keys', tablefmt = 'grid'))
        while True:
            new_user = input('Masukkan username baru: ').strip()
            if len(new_user) < 4:
                print('Username minimal 4 karakter.')
                continue
            if new_user in df['Username'].values:
                print('Username sudah digunakan.')
                continue

            df.loc[df['Username'] == usernamelogin, 'Username'] = new_user
            df.to_csv('user.csv', index=False)
            usernamelogin = new_user
            print('Username berhasil diubah.')
            input('Tekan Enter untuk kembali....')
            return df_menumanajer()

    # --- EDIT PASSWORD --- 
    elif opsi == '2' or opsi == 'edit password':
        os.system('cls')
        print('╔════════════════════════════════════════╗')
        print('║------------[ EDIT PASSWORD ]-----------║')
        print('╚════════════════════════════════════════╝')
        print('\nData akun anda:')
        print(tabulate(akun, headers = 'keys', tablefmt = 'grid'))
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
        print('Password berhasil diubah.')
        input('Tekan Enter untuk kembali...')
        return df_menumanajer() 

    elif opsi == '3' or opsi == 'kembali':
        return df_menuadmin()

    else:
        print('Inputan tidak valid. Tekan Enter....')
        return df_edit_akun_manajer()


def df_data_spesies():
    while True:
        os.system('cls')
        print('╔════════════════════════════════════════════════════╗')
        print('║  ╔══════════════════════════════════════════════╗  ║')
        print('║  ║     Sistem Manajemen Panen dan Penjualan     ║  ║')
        print('║  ║                                              ║  ║')
        print('║  ║        --------[  SI MANJA  ]-------         ║  ║')
        print('║  ╚══════════════════════════════════════════════╝  ║')
        print('╚════════════════════════════════════════════════════╝')
        print()
        print('------------------[  DATA SPESIES  ]------------------')
        
        df = pd.read_csv('data_spesies.csv')
        print()
        print('  [1] Tampilkan Spesies')
        print('  [2] Tambah Spesies')
        print('  [3] Ubah Spesies')
        print('  [4] Hapus Spesies')
        print('  [5] Kembali')
        opsi = input('Pilih menu: ').strip()

        if opsi == '1' or opsi == 'tampilkan spesies':
            os.system('cls')
            disp = df.copy()
            disp.insert(0, 'No', range(1, len(disp) + 1))
            print(tabulate(disp, headers='keys', tablefmt='fancy_grid', showindex=False))
            input('Tekan Enter untuk kembali....')

        elif opsi == '2' or opsi == 'tambah spesies':
            os.system('cls')
            disp = df.copy()
            disp.insert(0, 'No', range(1, len(disp) + 1))
            print(tabulate(disp, headers='keys', tablefmt='fancy_grid', showindex=False))
            if df.empty:
                new_id = 'SP001'
            else:
                last = df['ID Spesies'].iloc[-1]
                num = int(last[2:]) + 1
                new_id = f'SP{num:03d}'

            nama = input('Masukkan Nama Spesies: ')
            if not nama:
                print('Nama tidak boleh kosong.')
                continue
            df.loc[len(df)] = [new_id, nama]
            df.to_csv('data_spesies.csv', index=False)
            print('Spesies berhasil ditambahkan.')
            input('Tekan Enter untuk kembali....')

        elif opsi == '3' or opsi == 'ubah spesies':
            os.system('cls')
            disp = df.copy()
            disp.insert(0, 'No', range(1, len(disp) + 1))
            print(tabulate(disp, headers='keys', tablefmt='fancy_grid', showindex=False))
            sid = input('Masukkan ID Spesies yang ingin diubah: ').strip().upper()
            if sid in df['ID Spesies'].values:
                nama = input('Masukkan Nama Spesies baru: ')
                if nama:
                    df.loc[df['ID Spesies'] == sid, 'Nama Spesies'] = nama
                    df.to_csv('data_spesies.csv', index=False)
                    print('Spesies berhasil diperbarui.')
                else:
                    print('Nama tidak boleh kosong.')
            else:
                print('ID Spesies tidak ditemukan.')
            input('Tekan Enter untuk kembali....')

        elif opsi == '4' or opsi == 'hapus spesies':
            os.system('cls')
            disp = df.copy()
            disp.insert(0, 'No', range(1, len(disp) + 1))
            print(tabulate(disp, headers='keys', tablefmt='fancy_grid', showindex=False))
            sid = input('Masukkan ID Spesies yang ingin dihapus: ').strip().upper()
            if sid in df['ID Spesies'].values:
                df = df[df['ID Spesies'] != sid]
                df.to_csv('data_spesies.csv', index=False)
                print('Spesies berhasil dihapus.')
            else:
                print('ID Spesies tidak ditemukan.')
            input('Tekan Enter untuk kembali....')

        elif opsi == '5' or opsi == 'kembali':
            return df_menumanajer()
        
        else:
            print('Input tidak valid!')


def df_penjualan():
    while True: 
        os.system('cls')
        print('╔════════════════════════════════════════════════════╗')
        print('║  ╔══════════════════════════════════════════════╗  ║')
        print('║  ║     Sistem Manajemen Panen dan Penjualan     ║  ║')
        print('║  ║                                              ║  ║')
        print('║  ║        --------[  SI MANJA  ]-------         ║  ║')
        print('║  ╚══════════════════════════════════════════════╝  ║')
        print('╚════════════════════════════════════════════════════╝')
        print()
        print('-----------------[  DATA PENJUALAN  ]-----------------')
        print(
                    '[1] Tampilkan Data Penjualan\n'
                    '[2] Tambah Data Penjualan\n'
                    '[3] Ubah Data Penjualan\n'
                    '[4] Hapus Data Penjualan\n'
                    '[5] Kembali'
        )

        opsi = input('Masukkan menu yang anda pilih : ').lower()

         # ---- [ 1 ] TAMPILKAN DATA PENJUALAN ----
        if opsi == '1' or opsi == 'tampilkan data penjualan':
            os.system('cls')
            print('╔════════════════════════════════════════╗')
            print('║------[ TAMPILKAN DATA PENJUALAN ]------║')
            print('╚════════════════════════════════════════╝')
            print()
            df = pd.read_csv('data_penjualan.csv')
            if df.empty:
                print('Belum ada data penjualan.')
            else:
                print('Data Penjualan Seluruhnya.')
                df_display = df.copy()
                df_display.insert(0, 'No', range(1, len(df_display) + 1))
                print(tabulate(df_display, headers='keys', tablefmt='fancy_grid', showindex=False))
            input('Tekan Enter untuk kembali....')

        # ---- [ 2 ] TAMBAH DATA PANEN ----  
        elif opsi == '2' or opsi == 'tambah data panen':
            os.system('cls')
            print('╔════════════════════════════════════════╗')
            print('║-------[ TAMBAH DATA PENJUALAN ]--------║')
            print('╚════════════════════════════════════════╝')
            print()
            panen_all = pd.read_csv('data_panen.csv')
            df_pen = pd.read_csv('data_penjualan.csv')

            # buat id transaksi otomatis
            if df_pen.empty:
                new_id = 'TR001'
            else:
                last = df_pen['ID Transaksi'].iloc[-1]
                num = int(last[2:]) + 1
                new_id = f'TR{num:03d}'

            # tampilkan panen untuk referensi
            if panen_all.empty:
                print('Belum ada panen. Tidak dapat melakukan transaksi.')
                input('Tekan Enter untuk kembali....')
                return df_menumanajer()
            else:
                disp = panen_all.copy()
                disp.insert(0, 'No', range(1, len(disp) + 1))
                print('Referensi Data Panen: ')
                print(tabulate(disp[['No', 'ID Panen', 'Username', 'Tanggal', 'Spesies', 'Jumlah Bandang']], headers='keys', tablefmt='fancy_grid', showindex=False))

            idpanen = input('\nMasukkan ID Panen yang akan dijual: ').strip().upper()
            if idpanen not in panen_all['ID Panen'].values:
                print('ID Panen tidak ditemukan.')
                input('Tekan Enter untuk kembali....')
                return df_menumanajer()

            row = panen_all[panen_all['ID Panen'] == idpanen].iloc[0]
            bandang = pd.to_numeric(row['Jumlah Bandang'], errors='coerce')
            if pd.isna(bandang):
                print('Jumlah Bandang tidak valid pada data panen.')
                input('Tekan Enter untuk kembali....')
                return df_menumanajer()
            
            available_kg = bandang * 12

            while True:
                qty = input(f'Masukkan kuantitas (kg) (tersedia {int(available_kg)} kg): ').strip()
                try:
                    qty_val = float(qty)
                    if qty_val <= 0:
                        print('Kuantitas harus lebih dari 0.')
                        continue
                    if qty_val > available_kg:
                        print('Kuantitas melebihi stok tersedia.')
                        continue
                    break
                except ValueError:
                    print('Masukkan angka untuk kuantitas.')

            while True:
                harga = input('Masukkan Harga Jual per kg (Rp): ').strip()
                if harga.replace('.', '', 1).isdigit() and float(harga) >= 0:
                    harga_val = float(harga)
                    break
                else:
                    print('Harga harus angka >= 0.')

            while True:
                tanggal = input('Masukkan Tanggal Baru (YYYY-MM-DD): ').strip()
                if tanggal == '':
                    tanggal = datetime.today().strftime("%Y-%m-%d")
                    break
                if tanggal == '' or validasi_tanggal(tanggal):
                    break
                print('Format tanggal tidak valid! Gunakan YYYY-MM-DD.')

            pendapatan = qty_val * harga_val
            if 'Pendapatan' not in df_pen.columns:
                df_pen['Pendapatan'] = 0.0

            new_tr = {
                'ID Transaksi': new_id,
                'Tanggal': tanggal,
                'ID Panen': idpanen,
                'Kuantitas (kg)': qty_val,
                'Harga Jual/kg': harga_val,
                'Pendapatan': pendapatan
            }

            df_pen = pd.concat([df_pen, pd.DataFrame([new_tr])], ignore_index=True)
            df_pen.to_csv('data_penjualan.csv', index=False)
            print('\nTransaksi berhasil dicatat:')

            df_panen = pd.read_csv("data_panen.csv")
            df_panen["Jumlah Bandang"] = pd.to_numeric(df_panen["Jumlah Bandang"], errors="coerce")

            # cari data panen sesuai ID
            row_index = df_panen[df_panen["ID Panen"] == idpanen].index
            if not row_index.empty:
                idx = row_index[0]

                bandang_awal = df_panen.loc[idx, "Jumlah Bandang"]
                stok_awal_kg = bandang_awal * 12

                stok_sisa_kg = stok_awal_kg - qty_val
                if stok_sisa_kg < 0:
                    stok_sisa_kg = 0

                bandang_sisa = stok_sisa_kg / 12

                # update kembali
                df_panen.loc[idx, "Jumlah Bandang"] = round(bandang_sisa, 3)
                if stok_sisa_kg == 0:
                    df_panen = df_panen.drop(idx)
                    df_panen = df_panen.reset_index(drop=True)

                df_panen.to_csv("data_panen.csv", index=False)
            
            input("\nTransaksi berhasil dicatat! Tekan Enter untuk kembali...")
            return df_penjualan()
        
        # ---- [ 3 ] UBAH DATA PENJUALAN ----         
        elif opsi == '3' or opsi == 'ubah data penjualan':
            os.system('cls')
            print('╔════════════════════════════════════════╗')
            print('║---------[ UBAH DATA PENJUALAN ]--------║')
            print('╚════════════════════════════════════════╝')
            print()
            full_df = pd.read_csv('data_penjualan.csv')

            if full_df.empty:
                print('Tidak ada data penjualan.')
                input('Tekan Enter untuk kembali...')
                continue

            disp = full_df.copy()
            disp.insert(0, 'No', range(1, len(disp) + 1))
            print(tabulate(disp, headers='keys', tablefmt='fancy_grid', showindex=False))
            id_edit = input('\nMasukkan ID Penjualan yang ingin diubah: ').strip().upper()
            if id_edit not in full_df['ID Transaksi'].values:
                print('ID Transaksi tidak deitemukan')
                input('Tekan Enter untuk kembali....')
                return df_penjualan()
            
            if id_edit in full_df['ID Transaksi'].values:
                print('\nMasukkan data baru (kosongkan jika tidak ingin mengubah) ')
                while True:
                    tanggal = input('Masukkan Tanggal Baru (YYYY-MM-DD): ').strip()
                    if tanggal == "":
                        break
                    if validasi_tanggal(tanggal):
                        break
                    print("Format tanggal tidak valid! Gunakan format YYYY-MM-DD!")
                while True:
                    kuantitas = input('Masukkan kuantitas baru (kg): ')
                    if kuantitas == '':
                        break
                    try:
                        kuantitas_val = float(kuantitas)
                        if kuantitas_val > 0:
                            break
                        print("Kuantitas harus lebih dari 0!")
                    except:
                        print("Kuantitas harus berupa angka!")
                while True: 
                    harga = input('Masukkan Harga jual baru (per kg): ')
                    if harga == '':
                        break
                    try:
                        harga_val = float(harga)
                        if harga_val >= 0:
                            break
                        print("Harga harus >= 0!")
                    except:
                        print("Harga harus berupa angka!")
            
            
                # update data
                if tanggal != '': 
                    full_df.loc[full_df['ID Transaksi'] == id_edit, 'Tanggal'] = tanggal
                if kuantitas != '':
                    kuantitas_val = float(kuantitas)
                    full_df.loc[full_df['ID Transaksi'] == id_edit, 'Kuantitas (kg)'] = kuantitas_val
                if harga != '':
                    harga_val = float(harga)
                    full_df.loc[full_df['ID Transaksi'] == id_edit, 'Harga Jual/kg'] = harga_val

                # hitung ulang pendapatan
                row = full_df[full_df['ID Transaksi'] == id_edit].iloc[0]
                qty_now = float(row['Kuantitas (kg)'])
                harga_now = float(row['Harga Jual/kg'])
                pendapatan_now = qty_now * harga_now

                full_df.loc[full_df['ID Transaksi'] == id_edit, 'Pendapatan'] = pendapatan_now
                    
                full_df.to_csv('data_penjualan.csv', index=False)
                input('\nData berhasil diperbarui! Tekan Enter untuk kembali....')

            else:
                input('ID Penjualan tidak ditemukan! Tekan Enter untuk kembali....')
            

         # ---- [ 4 ] HAPUS DATA PENJUALAN ---- 
        elif opsi == '4' or opsi == 'hapus data penjualan':
            os.system('cls')
            print('╔════════════════════════════════════════╗')
            print('║--------[ HAPUS DATA PENJUALAN ]--------║')
            print('╚════════════════════════════════════════╝')
            print()
            full_df = pd.read_csv('data_penjualan.csv')
            if full_df.empty:
                print('Tidak ada data panen.')
                input('Tekan Enter...')
                continue

            disp = full_df.copy()
            disp.insert(0, 'No', range(1, len(disp) + 1))
            print(tabulate(disp, headers='keys', tablefmt='fancy_grid', showindex=False))

            id_hapus = input('\nMasukkan ID Transaksi yang ingin dihapus: ').strip().upper()
            if id_hapus in full_df['ID Transaksi'].values:
                full_df = full_df[full_df['ID Transaksi'] != id_hapus]
                full_df.to_csv('data_penjualan.csv', index=False)
                input('\nData berhasil dihapus! Tekan Enter untuk kembali....')
            else:
                input('ID Transaksi tidak ditemukan! Tekan Enter untuk kembali....')

        # ---- [ 5 ] KEMBALI ----
        elif opsi == '5' or opsi == 'kembali':
            return df_menumanajer()
        
        else: 
            print('Input tidak valid.')
            input('Tekan Enter untuk kembali...')
            return df_penjualan()


def df_kelola_panen_keseluruhan():
    while True:
        os.system('cls')
        print('╔════════════════════════════════════════════════════╗')
        print('║  ╔══════════════════════════════════════════════╗  ║')
        print('║  ║     Sistem Manajemen Panen dan Penjualan     ║  ║')
        print('║  ║                                              ║  ║')
        print('║  ║        --------[  SI MANJA  ]-------         ║  ║')
        print('║  ╚══════════════════════════════════════════════╝  ║')
        print('╚════════════════════════════════════════════════════╝')
        print()
        print('----------[  KELOLA DATA PANEN (MANAJER)  ]-----------')
        print(
                '[1] Tampilkan Semua Data Panen\n'
                '[2] Tambah Data Panen\n'
                '[3] Ubah Data Panen\n'
                '[4] Hapus Data Panen\n'
                '[5] Kembali'
            )
    
        opsi = input('Pilih menu: ').strip()

        # ---- [ 1 ] TAMPILKAN DATA PANEN ----
        if opsi == '1' or opsi == 'tampilkan semua data panen':
            os.system('cls')
            print('╔════════════════════════════════════════╗')
            print('║--------[ TAMPILKAN DATA PANEN ]--------║')
            print('╚════════════════════════════════════════╝')
            print()
            df = pd.read_csv('data_panen.csv')
            if df.empty:
                print('Belum ada data panen.')
            else:
                disp = df.copy(); disp.insert(0, 'No', range(1, len(disp) + 1))
                print(tabulate(disp, headers='keys', tablefmt='fancy_grid', showindex=False))
            input('Tekan Enter untuk kembali...')

        # ---- [ 2 ] TAMBAH DATA PANEN ----  
        elif opsi == '2' or opsi == 'tambah data panen':
            os.system('cls')
            print('╔════════════════════════════════════════╗')
            print('║---------[ TAMBAH DATA PANEN ]----------║')
            print('╚════════════════════════════════════════╝')
            print()
            df = pd.read_csv('data_panen.csv')
            if df.empty:
                new_id = 'PN001'
            else:
                last = df['ID Panen'].iloc[-1]
                num = int(last[2:]) + 1
                new_id = f'PN{num:03d}'

            df_user = pd.read_csv('user.csv')
            df_staf = df_user[df_user['Role'].str.lower() == 'staf']
            df_staf_display = df_staf.copy()
            df_staf_display.insert(0, 'No', range(1, len(df_staf_display) + 1))
            print(tabulate(df_staf_display, headers='keys', tablefmt='fancy_grid', showindex=False))
            username = input('Masukkan username pemilik data panen: ').strip()
            if username not in df_user['Username'].values:
                print('Username tidak ditemukan di data yang ada. ')
                input('Tekan Enter untuk mengulang')
                continue

            while True:
                tanggal = input('Masukkan Tanggal (YYYY-MM-DD): ').strip()
                if not tanggal:
                    print("Tanggal tidak boleh kosong!")
                    continue
                if validasi_tanggal(tanggal):
                    break
                print("Format tanggal tidak valid! Gunakan YYYY-MM-DD.")
            
            while True:
                sp = pd.read_csv('data_spesies.csv')
                sp.insert(0, 'No', range(1, len(sp) + 1))
                print(tabulate(sp, headers='keys', tablefmt='fancy_grid', showindex=False))
                spesies = input('Masukkan Spesies Tembakau: ')
                if spesies not in sp['Nama Spesies'].values:
                    print('Spesies tidak ditemukan di data yang ada. ')
                    input('Tekan Enter untuk mengulang')
                    continue
                if spesies in sp['Nama Spesies'].values:
                    break

            while True:
                jumlah = input('Masukkan Jumlah Bandang: ').strip()
                if not jumlah:
                    print("Jumlah bandang tidak boleh kosong!")
                    continue
                if jumlah.isdigit() and int(jumlah) > 0:
                    break
                print("Jumlah harus berupa angka positif!")
            
            while True:
                biaya = input('Masukkan Biaya Operasional (Rp): ')
                if not biaya:
                    print("Biaya operasional tidak boleh kosong!")
                    continue
                if biaya == '' or (biaya.replace('.', '', 1).isdigit() and float(biaya) >= 0):
                    break
                print('Biaya harus angka!')
            
            new_row = {'ID Panen': new_id, 
                       'Username': username, 
                       'Tanggal': tanggal,
                       'Spesies': spesies, 
                       'Jumlah Bandang': jumlah, 
                       'Biaya Operasional': biaya
                    }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv('data_panen.csv', index=False)
            print('Data panen berhasil ditambahkan.')
            input('Tekan Enter untuk kembali...')
        
        # ---- [ 3 ] UBAH DATA PANEN ----   
        elif opsi == '3' or opsi == 'ubah data panen':
            os.system('cls')
            print('╔════════════════════════════════════════╗')
            print('║-----------[ UBAH DATA PANEN ]----------║')
            print('╚════════════════════════════════════════╝')
            print()
            full_df = pd.read_csv('data_panen.csv')
            if full_df.empty:
                print('Tidak ada data panen.')
                input('Tekan Enter untuk kembali...')
                continue

            disp = full_df.copy()
            disp.insert(0, 'No', range(1, len(disp) + 1))
            print(tabulate(disp, headers='keys', tablefmt='fancy_grid', showindex=False))
            id_edit = input('Masukkan ID Panen yang ingin diubah: ').strip().upper()
            if id_edit not in full_df['ID Panen'].values:
                print('ID Panen tidak ditemukan.')
                input('Tekan Enter untuk kembali...')
                continue

            if id_edit in full_df['ID Panen'].values:
                print('\nMasukkan data baru (kosongkan jika tidak ingin mengubah)')
                # --- TANGGAL ---
                while True:
                    tanggal = input('Masukkan Tanggal Baru (YYYY-MM-DD): ').strip()
                    if tanggal == "":
                        break
                    if validasi_tanggal(tanggal):
                        break
                    print("Format tanggal tidak valid!")

                
                # --- SPESIES ---
                while True:
                    sp = pd.read_csv('data_spesies.csv')
                    sp.insert(0, 'No', range(1, len(sp) + 1))
                    print(tabulate(sp, headers='keys', tablefmt='fancy_grid', showindex=False))
                    spesies = input('Spesies baru: ')
                    if spesies == "":
                        break  

                    if spesies not in sp['Nama Spesies'].values:
                        print("Spesies tidak ditemukan di data yang ada!")
                        input("Tekan Enter untuk mengulang...")
                        continue
                    break

                # --- JUMLAH BANDANG ---
                while True:
                    jumlah = input('Masukkan Jumlah Bandang Baru: ').strip()
                    if jumlah == "":
                        break
                    if jumlah.isdigit() and int(jumlah) > 0:
                        break
                    print("Jumlah harus berupa angka positif!")

                # --- BIAYA ---
                while True:
                    biaya = input('Masukkan Biaya Operasional Baru (Rp): ').strip()
                    if biaya == "":
                        break
                    if biaya.isdigit() and int(biaya) >= 0:
                        break
                    print("Biaya harus angka!")

                # update data
                if tanggal != '': 
                    full_df.loc[full_df['ID Panen'] == id_edit, 'Tanggal'] = tanggal
                if spesies != '': 
                    full_df.loc[full_df['ID Panen'] == id_edit, 'Spesies'] = spesies
                if jumlah != '':
                    jumlah_val = float(jumlah) 
                    full_df.loc[full_df['ID Panen'] == id_edit, 'Jumlah Bandang'] = jumlah_val
                if biaya != '':
                    biaya_val = float(biaya) 
                    full_df.loc[full_df['ID Panen'] == id_edit, 'Biaya Operasional'] = biaya_val

                full_df.to_csv('data_panen.csv', index=False)
                input('\nData berhasil diperbarui! Tekan Enter untuk kembali....')

            else:
                input('ID Panen tidak ditemukan! Tekan Enter untuk kembali....')
        
        # ---- [ 4 ] HAPUS DATA PANEN ---- 
        elif opsi == '4' or opsi == 'hapus data panen':
            os.system('cls')
            print('╔════════════════════════════════════════╗')
            print('║----------[ HAPUS DATA PANEN ]----------║')
            print('╚════════════════════════════════════════╝')
            print()
            full_df = pd.read_csv('data_panen.csv')
            if full_df.empty:
                print('Tidak ada data panen.')
                input('Tekan Enter...')
                continue

            disp = full_df.copy()
            disp.insert(0, 'No', range(1, len(disp) + 1))
            print(tabulate(disp, headers='keys', tablefmt='fancy_grid', showindex=False))

            id_hapus = input('Masukkan ID Panen yang ingin dihapus: ').strip().upper()
            if id_hapus in full_df['ID Panen'].values:
                full_df = full_df[full_df['ID Panen'] != id_hapus]
                full_df.to_csv('data_panen.csv', index=False)
                input('\nData berhasil dihapus! Tekan Enter untuk kembali....')
            else:
                input('ID Panen tidak ditemukan! Tekan Enter untuk kembali....')

        # ---- [ 5 ] KEMBALI ----
        elif opsi == '5' or opsi == 'kembali':
            return df_menumanajer()
        
        else: 
            print('Input tidak valid.')
            input('Tekan Enter untuk kembali...')
            return df_kelola_panen_keseluruhan()


def df_laporan_rekap():
    while True:
        os.system('cls')
        print('╔════════════════════════════════════════════════════╗')
        print('║  ╔══════════════════════════════════════════════╗  ║')
        print('║  ║     Sistem Manajemen Panen dan Penjualan     ║  ║')
        print('║  ║                                              ║  ║')
        print('║  ║        --------[  SI MANJA  ]-------         ║  ║')
        print('║  ╚══════════════════════════════════════════════╝  ║')
        print('╚════════════════════════════════════════════════════╝')
        print()
        print('-----------------[  LAPORAN & REKAP  ]----------------')
        print(
            '[1] Laporan Transaksi (urut berdasarkan Pendapatan)\n'
            '[2] Laporan Transaksi (urut berdasarkan Tanggal)\n'
            '[3] Cari Transaksi (ID Transaksi)\n'
            '[4] Rekap Per Spesies (pendapatan / total kuantitas)\n'
            '[5] Kembali'
        )
        opsi = input('Pilih menu: ').strip()
        if opsi == '1' or opsi == 'laporan transaksi urut berdasarkan pendapatan':
            # sorting menggunakan pandas (quick/merge sort tergantung pandas impl.)
            os.system('cls')
            df_tr = pd.read_csv('data_penjualan.csv')
            if df_tr.empty:
                print('Belum ada transaksi.')
            else:
                if 'Pendapatan' not in df_tr.columns:
                    df_tr['Pendapatan'] = df_tr['Kuantitas (kg)'] * df_tr['Harga Jual/kg']
                df_sorted = df_tr.sort_values(by='Pendapatan', ascending=False)
                df_sorted.insert(0, 'No', range(1, len(df_sorted) + 1))
                print(tabulate(df_sorted, headers='keys', tablefmt='fancy_grid', showindex=False))
            input('Tekan Enter untuk kembali...')

        elif opsi == '2' or opsi == 'laporan transaksi urut berdasarkan tanggal':
            os.system('cls')
            df_tr = pd.read_csv('data_penjualan.csv')
            if df_tr.empty:
                print('Belum ada transaksi.')
            else:
                # memastikan tanggal jadi datetime
                df_tr['Tanggal'] = pd.to_datetime(df_tr['Tanggal'], errors='coerce')
                df_sorted = df_tr.sort_values(by='Tanggal', ascending=False)
                df_sorted.insert(0, 'No', range(1, len(df_sorted) + 1))
                print(tabulate(df_sorted, headers='keys', tablefmt='fancy_grid', showindex=False))
            input('Tekan Enter untuk kembali....')

        elif opsi == '3' or opsi == 'cari transaksi' :
            os.system('cls')
            # df = pd.read_csv('data_penjualan.csv')
            # disp = df.copy()
            # disp.insert(0, 'No', range(1, len(disp) + 1))
            # print(tabulate(disp, headers='keys', tablefmt='fancy_grid', showindex=False))
            cari = input('Masukkan ID Transaksi yang dicari: ').strip().upper()
            df_tr = pd.read_csv('data_penjualan.csv')
            found = []

            for _, r in df_tr.iterrows():
                if str(r.get('ID Transaksi', '')).strip() == cari:
                    found.append(r)
            if found:
                print(tabulate(pd.DataFrame(found), headers='keys', tablefmt='fancy_grid', showindex=False))
            else:
                print('Transaksi tidak ditemukan.')
            input('Tekan Enter untuk kembali....')

        elif opsi == '4' or opsi == 'rekap per spesies' :
            os.system('cls')
            df_tr = pd.read_csv('data_penjualan.csv')
            df_pn = pd.read_csv('data_panen.csv')
            if df_tr.empty or df_pn.empty:
                print('Data belum lengkap')
                input('Tekan Enter....')  
                continue
            # memastikan ada pendapatan
            if 'Pendapatan' not in df_tr.columns:
                df_tr['Pendapatan'] = df_tr['Kuantitas (kg)'] * df_tr['Harga Jual/kg']
            # merge transaksi dengan panen untuk mendapatkan spesies
            merged = pd.merge(df_tr, df_pn[['ID Panen', 'Spesies']], left_on='ID Panen', right_on='ID Panen', how='left')
            # group by spesies 
            regroup = merged.groupby('Spesies').agg({
                'Kuantitas (kg)': 'sum',
                'Pendapatan': 'sum'
            }).reset_index()
            if regroup.empty:
                print('Tidak ada data untul rekap.')
            else:
                regroup.insert(0, 'No', range(1, len(regroup) + 1))
                print(tabulate(regroup, headers='keys', tablefmt='fancy_grid', showindex=False))
            input('Tekan Enter untuk kembali....')

        elif opsi == '5' or opsi == 'kembali':
            return df_menumanajer()
        else:
            print('Input tidak valid.')
            

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
        print('Password berhasil diubah.')
        input('Tekan Enter untuk kembali...')
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
            print('║--------[ TAMPILKAN DATA PANEN ]--------║')
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
            print('║---------[ TAMBAH DATA PANEN ]----------║')
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
                tanggal = input('Masukkan Tanggal (YYYY-MM-DD): ').strip()
                if not tanggal:
                    print("Tanggal tidak boleh kosong!")
                    continue
                if validasi_tanggal(tanggal):
                    break
                print("Format tanggal tidak valid! Gunakan YYYY-MM-DD.")

            while True:
                sp = pd.read_csv('data_spesies.csv')
                sp.insert(0, 'No', range(1, len(sp) + 1))
                print(tabulate(sp, headers='keys', tablefmt='fancy_grid', showindex=False))
                spesies = input('Masukkan Spesies Tembakau: ')
                if spesies not in sp['Nama Spesies'].values:
                    print('Spesies tidak ditemukan di data yang ada. ')
                    input('Tekan Enter untuk mengulang')
                    continue
                if spesies in sp['Nama Spesies'].values:
                    break
                            
            while True:
                jumlah = input('Masukkan Jumlah Bandang: ').strip()
                if not jumlah:
                    print("Jumlah bandang tidak boleh kosong!")
                    continue
                if jumlah.isdigit() and int(jumlah) > 0:
                    break
                print("Jumlah harus berupa angka positif!")

            while True:
                biaya = input('Masukkan Biaya Operasional (Rp): ')
                if not biaya:
                    print("Biaya operasional tidak boleh kosong!")
                    continue
                if biaya == '' or (biaya.replace('.', '', 1).isdigit() and float(biaya) >= 0):
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
            print('║-----------[ UBAH DATA PANEN ]----------║')
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
            id_edit = input('\nMasukkan ID Panen yang ingin diubah: ').strip().upper()

            df['ID Panen'] = df['ID Panen'].astype(str).str.upper()
            full_df['ID Panen'] = full_df['ID Panen'].astype(str).str.upper()

            if id_edit not in df['ID Panen'].values:
                input('ID Panen tidak ditemukan atau tidak dapat dihapus oleh akun ini. Tekan Enter...')
                continue

            print('\nMasukkan data baru (kosongkan jika tidak ingin mengubah) ')

            # --- TANGGAL ---
            while True:
                tanggal = input('Masukkan Tanggal Baru (YYYY-MM-DD): ').strip()
                if tanggal == "":
                    break
                if validasi_tanggal(tanggal):
                    break
                print("Format tanggal tidak valid!")

            # --- SPESIES ---
            while True:
                sp = pd.read_csv('data_spesies.csv')
                sp.insert(0, 'No', range(1, len(sp) + 1))
                print(tabulate(sp, headers='keys', tablefmt='fancy_grid', showindex=False))
                spesies = input('Spesies baru: ')
                if spesies == "":
                    break  

                if spesies not in sp['Nama Spesies'].values:
                    print("Spesies tidak ditemukan di data yang ada!")
                    input("Tekan Enter untuk mengulang...")
                    continue
                break

            # --- JUMLAH BANDANG ---
            while True:
                jumlah = input('Masukkan Jumlah Bandang Baru: ').strip()
                if jumlah == "":
                    break
                if jumlah.isdigit() and int(jumlah) > 0:
                    break
                print("Jumlah harus berupa angka positif!")

            # --- BIAYA ---
            while True:
                biaya = input('Masukkan Biaya Operasional Baru (Rp): ').strip()
                if biaya == "":
                    break
                if biaya.isdigit() and int(biaya) >= 0:
                    break
                print("Biaya harus angka!")

            # --- UPDATE KE full_df ---
            if tanggal != "":
                full_df.loc[full_df['ID Panen'] == id_edit, 'Tanggal'] = tanggal

            if spesies != "":
                full_df.loc[full_df['ID Panen'] == id_edit, 'Spesies'] = spesies

            if jumlah != "":
                jumlah_val = float(jumlah)
                full_df.loc[full_df['ID Panen'] == id_edit, 'Jumlah Bandang'] = jumlah_val

            if biaya != "":
                biaya_val = float(biaya)
                full_df.loc[full_df['ID Panen'] == id_edit, 'Biaya Operasional'] = biaya_val

            full_df.to_csv('data_panen.csv', index=False)
            input('\nData berhasil diperbarui! Tekan Enter untuk kembali....')

        # ---- [ 4 ] HAPUS DATA PANEN ---- 
        elif opsi == '4' or opsi == 'hapus data panen':
            os.system('cls')
            print('╔════════════════════════════════════════╗')
            print('║----------[ HAPUS DATA PANEN ]----------║')
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
            df_display.insert(0, 'No', range(1, len(df_display) + 1))
            print(tabulate(df_display, headers='keys', tablefmt='fancy_grid', showindex=False))

            id_hapus = input('\nMasukkan ID Panen yang ingin dihapus: ').strip().upper()

            df['ID Panen'] = df['ID Panen'].astype(str).str.upper()
            full_df['ID Panen'] = full_df['ID Panen'].astype(str).str.upper()

            if id_hapus not in df['ID Panen'].values:
                input('ID Panen tidak ditemukan atau tidak dapat dihapus oleh akun ini. Tekan Enter...')
                continue

            yakin = input(f'Anda yakin ingin menghapus {id_hapus}? (y/n): ').lower().strip()
            if yakin != 'y':
                input('Dibatalkan. Tekan Enter untuk kembali...')
                continue

            full_df = full_df[full_df['ID Panen'] != id_hapus]
            full_df.to_csv('data_panen.csv', index=False)

            input('\nData berhasil dihapus! Tekan Enter untuk kembali....')

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
    print('╔════════════════════════════════════════════════════╗')
    print('║  ╔══════════════════════════════════════════════╗  ║')
    print('║  ║     Sistem Manajemen Panen dan Penjualan     ║  ║')
    print('║  ║                                              ║  ║')
    print('║  ║        --------[  SI MANJA  ]-------         ║  ║')
    print('║  ╚══════════════════════════════════════════════╝  ║')
    print('╚════════════════════════════════════════════════════╝')
    print('-----------------[ STATISTIK PANEN ]------------------')
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
    tmin = df['Tanggal'].min()
    tmax = df['Tanggal'].max()
    panen_terlama = tmin.date() if pd.notnull(tmin) else 'N/A'
    panen_terbaru = tmax.date() if pd.notnull(tmax) else 'N/A'

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