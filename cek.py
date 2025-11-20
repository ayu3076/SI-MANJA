import os
import csv 
import pandas as pd
from tabulate import tabulate
from datetime import datetime 


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
                spesies = input('Masukkan Spesies Tembakau: ').strip()
                if spesies:
                    break
                print('Spesies tidak boleh kosong!')
                            
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
            spesies = input('Spesies baru: ').strip()

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

            yakin = input(f'Anda yakin ingin menghapus {id_hapus}? ( y / t ): ').lower().strip()
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

            id_hapus = input('Masukkan ID Panen yang ingin dihapus: ').strip()
            if id_hapus in full_df['ID Panen'].values:
                full_df = full_df[full_df['ID Panen'] != id_hapus]
                full_df.to_csv('data_panen.csv', index=False)
                input('\nData berhasil dihapus! Tekan Enter untuk kembali....')
            else:
                input('ID Panen tidak ditemukan! Tekan Enter untuk kembali....')

