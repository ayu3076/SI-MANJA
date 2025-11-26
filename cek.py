#  # ---- [ 3 ] UBAH DATA PANEN ----         
#         elif opsi == '3' or opsi == 'ubah data panen':
#             os.system('cls')
#             print('╔════════════════════════════════════════╗')
#             print('║-----------[ UBAH DATA PANEN ]----------║')
#             print('╚════════════════════════════════════════╝')
#             print()
#             full_df = pd.read_csv('data_panen.csv')

#             # Jika staf, hanya bisa ubah datanya sendiri
#             if rolelogin.lower() == 'staf':
#                 df = full_df[full_df['Username'] == usernamelogin]
#             else:
#                 df = full_df.copy()

#             if df.empty:
#                 input('Tidak ada data yang dapat diubah. Tekan Enter untuk kembali...')
#                 continue

#             df_display = df.copy()
#             df_display.insert(0, "No", range(1, len(df_display) + 1))
#             print(tabulate(df_display, headers='keys', tablefmt='fancy_grid', showindex=False))
#             id_edit = input('\nMasukkan ID Panen yang ingin diubah: ').strip().upper()

#             df['ID Panen'] = df['ID Panen'].astype(str).str.upper()
#             full_df['ID Panen'] = full_df['ID Panen'].astype(str).str.upper()

#             if id_edit not in df['ID Panen'].values:
#                 input('ID Panen tidak ditemukan atau tidak dapat dihapus oleh akun ini. Tekan Enter...')
#                 continue

#             print('\nMasukkan data baru (kosongkan jika tidak ingin mengubah) ')

#             # --- TANGGAL ---
#             while True:
#                 tanggal = input('Masukkan Tanggal Baru (YYYY-MM-DD): ').strip()
#                 if tanggal == "":
#                     break
#                 if validasi_tanggal(tanggal):
#                     break
#                 print("Format tanggal tidak valid!")

#             # --- SPESIES ---
#             sp = pd.read_csv('data_spesies.csv')
#             sp.insert(0, 'No', range(1, len(sp) + 1))
#             print(tabulate(sp, headers='keys', tablefmt='fancy_grid', showindex=False))
#             spesies = input('Spesies baru: ')
#             if spesies == "":
#                 break  

#             if spesies not in sp['Nama Spesies'].values:
#                 print("Spesies tidak ditemukan di data yang ada!")
#                 input("Tekan Enter untuk mengulang...")
#                 continue

#             # --- JUMLAH BANDANG ---
#             while True:
#                 jumlah = input('Masukkan Jumlah Bandang Baru: ').strip()
#                 if jumlah == "":
#                     break
#                 if jumlah.isdigit() and int(jumlah) > 0:
#                     break
#                 print("Jumlah harus berupa angka positif!")

#             # --- BIAYA ---
#             while True:
#                 biaya = input('Masukkan Biaya Operasional Baru (Rp): ').strip()
#                 if biaya == "":
#                     break
#                 if biaya.isdigit() and int(biaya) >= 0:
#                     break
#                 print("Biaya harus angka!")

#             # --- UPDATE KE full_df ---
#             if tanggal != "":
#                 full_df.loc[full_df['ID Panen'] == id_edit, 'Tanggal'] = tanggal

#             if spesies != "":
#                 full_df.loc[full_df['ID Panen'] == id_edit, 'Spesies'] = spesies

#             if jumlah != "":
#                 jumlah_val = float(jumlah)
#                 full_df.loc[full_df['ID Panen'] == id_edit, 'Jumlah Bandang'] = jumlah_val

#             if biaya != "":
#                 biaya_val = float(biaya)
#                 full_df.loc[full_df['ID Panen'] == id_edit, 'Biaya Operasional'] = biaya_val

#             full_df.to_csv('data_panen.csv', index=False)
#             input('\nData berhasil diperbarui! Tekan Enter untuk kembali....')
