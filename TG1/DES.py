def circular_shift_left(binaries, shift): 
    # melakukan pergeseran sirkular ke kiri pada rangkaian biner.
    cut = binaries[:shift]
    res = binaries[shift:] + cut
    return res

def key_generator(key): 
    # menghasilkan semua subkey yang diperlukan untuk algoritma DES.

    def permutation(initial_key, perm_choice):
        # melakukan permutasi pada kunci awal.
        return [initial_key[i - 1] for i in perm_choice]

    def split_key(initial_key):
        # membagi kunci menjadi dua bagian.
        return initial_key[:28], initial_key[28:]

    def generate_sub_keys(initial_key):
        # menghasilkan subkey berdasarkan kunci awal.
        sub_keys = []
        for i in range(16):
            c, d = split_key(initial_key)
            c = circular_shift_left(c, shift_schedule[i])#pergeseran
            d = circular_shift_left(d, shift_schedule[i])
            initial_key = c + d
            sub_key = permutation(initial_key, perm_choice_2)
            sub_keys.append(sub_key)
        return sub_keys

    shift_schedule = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    perm_choice_1 = [57,49,41,33,25,17,9,       #  data 56bit
                     1,58,50,42,34,26,18,
                     10,2,59,51,43,35,27,
                     19,11,3,60,52,44,36,
                     63,55,47,39,31,23,15,
                     7,62,54,46,38,30,22,
                     14,6,61,53,45,37,29,
                     21,13,5,28,20,12,4]
    perm_choice_2 = [14,17,11,24,1,5,           #di input dan di  48
                     3,28,15,6,21,10,
                     23,19,12,4,26,8,
                     16,7,27,20,13,2,
                     41,52,31,37,47,55,
                     30,40,51,45,33,48,
                     44,49,39,56,34,53,
                     46,42,50,36,29,32]
    sub_keys = []

    #proses enkripsi Des
    key_binaries = ''.join(format(ord(char), '08b') for char in key) #mengubah binary character menjadi asci
    key_binaries = permutation(key_binaries, perm_choice_1) #Mengubah urutan bit dalam key_binaries berdasarkan tabel permutasi yang disebut perm_choice_1.
    sub_keys = generate_sub_keys(key_binaries) #hasil

    return sub_keys

def initial_permutation(binaries): 
    # melakukan permutasi awal pada blok biner.
    initial_permutation = [58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,
                           62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8,
                           57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,
                           61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7]
    result = ['a' for i in range(64)] #menyipan  64 bit pada a
    for i in range(len(initial_permutation)):
        result[i] = binaries[initial_permutation[i] - 1] #menentukan posisi
    res = ''.join(result) #digabung menjadi string
    return res

def final_permutation(binaries): 
    # melakukan permutasi akhir pada blok biner.
    final_permutation = [40,8,48,16,56,24,64,32,
                         39,7,47,15,55,23,63,31,
                         38,6,46,14,54,22,62,30,
                         37,5,45,13,53,21,61,29,
                         36,4,44,12,52,20,60,28,
                         35,3,43,11,51,19,59,27,
                         34,2,42,10,50,18,58,26,
                         33,1,41,9,49,17,57,25]
    result = ['a' for i in range(64)] 
    for i in range(len(final_permutation)):
        result[i] = binaries[final_permutation[i] - 1]
    res = ''.join(result)
    return res

def s_box(binaries):
    # melakukan substitusi dengan tabel S-box sesuai dengan algoritma DES.
    s_boxes = [
        [
            [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
            [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
            [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
            [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
        ],
        [
            [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
            [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
            [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
            [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
        ],
        [
            [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
            [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
            [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
            [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
        ],
        [
            [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
            [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
            [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
            [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
        ],
        [
            [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
            [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
            [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
            [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
        ],
        [
            [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
            [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
            [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
            [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
        ],
        [
            [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
            [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
            [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
            [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
        ],
        [
            [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
            [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
            [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
            [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
        ]
    ]

    result = ''
    for i in range(0, len(binaries), 6):
        tmp = binaries[i:i + 6]
        row = int(tmp[0] + tmp[5], 2)
        col = int(tmp[1:5], 2)
        temp = bin(s_boxes[i//6][row][col])[2:]
        if len(temp) == 4:
            result += temp
        else:
            result += (4 - len(temp) % 4) * '0' + temp
    return result

def feistel(binaries, rounds):
    # mewakili putaran Feistel pada algoritma DES.
    expansion_table = [32,1,2,3,4,5,
                       4,5,6,7,8,9,
                       8,9,10,11,12,13,
                       12,13,14,15,16,17,
                       16,17,18,19,20,21,
                       20,21,22,23,24,25,
                       24,25,26,27,28,29,
                       28,29,30,31,32,1]
    straight_permutation_table = [16,7,20,21,29,12,28,17,
                                  1,15,23,26,5,18,31,10,
                                  2,8,24,14,32,27,3,9,
                                  19,13,30,6,22,11,4,25]
    expanded = ['a' for i in range(48)]
    for i in range(len(expansion_table)):
        expanded[i] = binaries[expansion_table[i] - 1]
    expanded_binaries = ''.join(expanded)
    tmp = ''
    for i in range(len(expanded_binaries)):
        tmp += str(ord(expanded_binaries[i]) ^ ord(sub_keys[rounds][i]))
    temp = s_box(tmp)
    res = ['a' for i in range(32)] #hasil dilakukan permutation
    for i in range(len(straight_permutation_table)):
        res[i] = temp[straight_permutation_table[i] - 1]
    result = ''.join(res)
    return result

def DES_encrypt(text):
    # melakukan enkripsi DES pada teks input.
    binaries = ''.join(format(ord(char), '08b') for char in text)
    binaries = initial_permutation(binaries) #emanggilan fungsi initial_permutation dengan parameter binaries
    left = binaries[:32]
    right = binaries[32:]
    for i in range(16):
        temp_right = right
        right = feistel(right, i) #Menggunakan fungsi feistel untuk mengenkripsi bagian right berdasarkan putaran ke-i.
        right2 = ''.join(str(ord(left[j]) ^ ord(right[j])) for j in range(len(right)))
        left = temp_right
        right = right2
    final = right + left
    result = final_permutation(final)
    return result

    # mengubah biner ke string.
    #ciphertext = ''.join([chr(int(result[i:i + 8], 2)) for i in range(0, len(result), 8)])
    # return ciphertext

def PKCS7_padding(text):
    # melakukan padding teks sesuai dengan PKCS7.
    pad_length = 8 - (len(text) % 8) #mengitung panjang
    padded_text = text + chr(pad_length) * pad_length #menambahkan padd
    return padded_text

def DES_decrypt(ciphertext, sub_keys, is_padded=True):
    # melakukan dekripsi DES pada teks input.
    # binaries = list(ciphertext)  # mengonversi ke list karakter

    binaries = ''.join(format(ord(char), '08b') for char in ciphertext)
    binaries = initial_permutation(binaries)
    left = binaries[:32]
    right = binaries[32:]
    for i in range(15, -1, -1):
        temp_right = right
        right = feistel(right, i)
        right2 = ''.join(str(ord(left[j]) ^ ord(right[j])) for j in range(len(right)))
        left = temp_right
        right = right2
    final = right + left
    result = final_permutation(final)#unutk mendapatkan hasil descrypt
    # return result
    # mengonversi hasil dekripsi ke teks
    decrypted_text = ''.join([chr(int(''.join(result[i:i + 8]), 2)) for i in range(0, len(result), 8)])

    # if is_padded:
        # menghapus padding
        # decrypted_text = PKCS7_depadding(result)
    
    return decrypted_text

def PKCS7_depadding(text):
    # menghapus PKCS7 padding dari teks yang sudah didekripsi
    pad_length = ord(text[-1])
    return text[:-pad_length]

list_of_key = ['' for x in range(16)]
list_of_plaintext = ['' for x in range(100)]

print("Pilih mode:")
print("1. Enkripsi")
print("2. Dekripsi")
choice = int(input("Masukkan pilihan (1/2): "))

if choice == 1:
    print("Masukan plaintext: ")
    plaintext = input()
    print("Masukan key (8 karakter): ")
    key = input()
    sub_keys = key_generator(key)

    if len(plaintext) % 8 != 0: #Mengubah panjang teks agar bisa diproses dalam blok 8 karakter
        plaintext += ' ' * (8 - len(plaintext) % 8)
    for i in range(0, len(plaintext), 8):  #Memudahkan proses enkripsi dan dekripsi dengan memecah plaintext menjadi blok yang lebih kecil.
        list_of_plaintext[i//8] = plaintext[i:i+8]

    ciphertext = ''
    for i in range(len(plaintext)//8):
        tmp = DES_encrypt(list_of_plaintext[i]) #melakukan enkripsi blok ke i dari list_..
        for j in range(0, len(tmp), 8): #mengkonversi menjadi karakter
            ciphertext += chr(int(tmp[j:j+8], 2))
    print("Ciphertext: " + ciphertext)
    print("Ciphertext hex encoded: " + ciphertext.encode('utf-8').hex())

    # if len(plaintext) % 8 != 0:
        # plaintext = PKCS7_padding(plaintext)

    # ciphertext = DES_encrypt(plaintext)
    # print("Ciphertext: " + ciphertext)

elif choice == 2:
    print("Masukan ciphertext: ")
    ciphertext = input()
    print("Masukan key (8 karakter): ")
    key = input()
    sub_keys = key_generator(key)

    if len(ciphertext) % 8 != 0: #Pemeriksaan dan Penambahan Padding
        ciphertext += ' ' * (8 - len(ciphertext) % 8)

    list_of_ciphertext = ['' for x in range(len(ciphertext) // 8)]  #Inisialisasi List untuk Ciphertext

    for i in range(0, len(ciphertext), 8): #Pemecahan Ciphertext Menjadi Blok
        list_of_ciphertext[i // 8] = ciphertext[i:i + 8]

    decrypted_text = ''
    for chunk in list_of_ciphertext:  #Iterasi Melalui Ciphertext:
        decrypted_chunk = DES_decrypt(chunk, sub_keys) #Dekripsi Setiap Blok
        decrypted_text += decrypted_chunk.rstrip(' ')  # menghapus spasi yang mungkin ditambahkan pada enkripsi
        
#chunk: blok ciphertext yang ingin didekripsi.
#sub_keys: daftar kunci sub yang dihasilkan dari kunci awal dan digunakan selama proses enkripsi dan dekripsi DES.
#Fungsi DES_decrypt akan mengembalikan blok plaintext yang didekripsi dari ciphertext tersebut dan menyimpannya dalam variabel decrypted_chunk.

    # decrypted_text = DES_decrypt(ciphertext, sub_keys)
    print("Plaintext yang sudah didekripsi:", decrypted_text)