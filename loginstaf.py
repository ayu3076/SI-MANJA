# import os
# import csv 
# import pandas as pd
# from tabulate import tabulate 

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

#     if loginsukses :
#         usernamelogin = username
#         print('Login berhasil.')
#         input('Tekan Enter untuk melanjutkan.')
#         os.system('cls')
#         df_menustaff()
#     else :
#         print('Username atau Password salah.')
#         while True:
#             cek = input('Apakah anda ingin melanjutkan (y/t) : ').lower()
#             if cek == 'y':
#                 df_loginstaf()  
#             elif cek == 't':
#                 input('Silahkan tekan Enter untuk kembali ke menu sebelumnya')
#                 os.system('cls')
#                 df_homepage() 
#             else:
#                 print('Inputan invalid')