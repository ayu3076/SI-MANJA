# import os
# import csv 
# import pandas as pd
# from tabulate import tabulate 

# def df_user():
#     if not os.path.exists('user.csv'):
#         with open('user.csv', mode= 'w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(['Username','Password','Role'])

# def df_registrasi():
#     os.system('cls')
#     print('╔════════════════════════════════════════╗')
#     print('║-------------[  REGISTER  ]-------------║')
#     print('╚════════════════════════════════════════╝') 
#     df_user()
#     with open('user.csv', mode= 'r') as file :
#         username_sama = {row['Username'] for row in csv.DictReader(file)}

#     role = input('Daftar akun sebagai: ').lower()
#     if role == 'staf lapangan' or 'manajer':
#         username = input('Daftarkan username anda : ')
#         if len(username) < 4 :
#             input('Username minimal 4 huruf. Tekan Enter untuk melanjutkan')
#             df_registrasi()

#         elif username in username_sama :
#             print('Username sudah terdaftar!')
#             input('Tekan Enter untuk melanjutkan.')
#             df_registrasi()

#         while True :
#             password = input('Masukkan Password: ')
#             if len(password) < 8 :
#                 print('Password minimal 8 karakter.')
#                 continue

#             while True :
#                 cek = input('Apakah Username dan Password sudah sesuai? (y/t): ').lower()
#                 if cek == 'y' :
#                     with open('user.csv', mode='a', newline='') as file :
#                         writer = csv.writer(file)
#                         writer.writerow([username, password, role])
#                     print('Registrasi berhasil! Silahkan login.')
#                     input('Tekan Enter untuk melanjutkan.')
#                     df_homepage()
#                 elif cek == 't' :
#                     input('Silahkan tekan Enter untuk melakukan registrasi ulang.')
#                     df_homepage()
#                 else :
#                     print('Input tidak valid. Silahkan ulangi.')  
#     else :
#         input('Input tidak valid. Silahkan tekan Enter untuk coba lagi.')
#         df_registrasi()