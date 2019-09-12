from replacement_table import *
import re

key = "Two One Nine Two"
key_mas = [ord(c) for c in key]
print(key_mas)


def read_file_in_state(filename, size_block):
    with open(filename, 'r', encoding="utf-8") as filehandle:
        filecontent = filehandle.read()
    size_state = len(filecontent) // size_block
    if not len(filecontent) % size_block == 0:
        size_state += 1
    state = [0] * size_state
    for i in range(size_state):
        data = filecontent[size_block * i:size_block * (i + 1)]
        str = ""
        for j in range(len(data)):
            str += data[j]
        if i == size_state - 1:
            if not size_block - len(data) == 0:
                for k in range(size_block - len(data)):
                    str += " "
        state[i] = str
        # print(state[i])
        # print("/--/--/--/--/--/--/--/--/--/--/--/--/")

    return state


def write_in_file(filename, state):
    with open(filename, 'w', encoding="utf-8") as filehandle:
        for i in range(len(state)):
            for j in range(len(state[i])):
                filehandle.write(state[i][j])


def name_file_encrypt(filename):
    print(filename)
    n = len(filename)
    str = filename[0: n - 4] + "encrypt" + filename[n - 4: n]
    return str


def name_file_decrypt(filename):
    index = filename.find("encrypt")
    # print(index)
    if not index == -1:
        filename = filename[0: len(filename) - 11] + ".txt"

    n = len(filename)
    str = filename[0: n - 4] + "decrypt" + filename[n - 4: n]
    return str


# циклический сдвиг влево
def left_shift(num, n):
    if num == 0:
        return 0
    # bitsize = num.bit_length()
    bitsize = 32

    tempr = (num >> (bitsize - n))
    templ = (num << n & ((2 ** 32) - 1))

    return (templ | tempr)


# циклический сдвиг вправо
def right_shift(num, n):
    if num == 0:
        return 0

    # bitsize = num.bit_length()
    bitsize = 32

    templ = (num >> n)
    tempr = (num << (bitsize - n) & ((2 ** 32) - 1))

    return (tempr | templ)


def replacement_table(T):
    i = T & ((1 << 9) - 1)

    return int(S[i], 16)


def s0_box(A):
    i = A & ((1 << 8) - 1)

    return int(S[i], 16)


def s1_box(A):
    i = A & ((1 << 8) - 1)

    return int(S[i + 256], 16)


def generate_mask(K):
    K = bin(K)[2:]

    if len(K) < 32:
        K = '0' * (32 - len(K)) + K

    binary_string = bin(1 << 32)[3:]

    for i in re.finditer(r'0{10,}', K):
        s = i.start()
        e = i.end()
        # (i[0], i.start(), i.end())
        binary_string = binary_string[:s] + '1' * (e - s) + binary_string[e:]

    for i in re.finditer(r'1{10,}', K):
        s = i.start()
        e = i.end()
        # print(i[0], i.start(), i.end())
        binary_string = binary_string[:s] + '1' * (e - s) + binary_string[e:]

    for i in range(len(binary_string)):
        if (i < 2) or (i == 31) or (K[i] != K[i - 1]) or (K[i] != K[i + 1]) or (K[i - 1] != K[i + 1]):
            binary_string = binary_string[:i] + '0' + binary_string[i + 1:]

    binary_string = "0b" + binary_string

    return int(binary_string, 2)


def transform_data(key):
    n = len(key) * 8 // 32
    string = ' '.join(format(ord(x), 'b') for x in key)
    string = string.split()
    mas = [0] * n
    for i in range(len(string)):
        if len(string[i]) < 8:
            raz = 8 - len(string[i])
            string[i] = "0" * raz + string[i]
    for i in range(n):
        mas[i] = "0b" + string[4 * i] + string[4 * i + 1] + string[4 * i + 2] + string[4 * i + 3]
    # print(mas)
    for i in range(len(mas)):
        mas[i] = int(mas[i], 2)
    # print(mas)
    return mas


def key_expansion(key):
    T = [0] * 15
    K = [0] * 40
    B = ['0xa4a8d57b', '0x5b5d193b', '0xc8a8309b', '0x73f9a978']
    n = int(len(key) * 8 / 32)

    data = transform_data(key)
    for i in range(n):
        T[i] = data[i]
    T[n] = n
    # print(T)

    for j in range(4):
        for i in range(15):
            T[i] = T[i] ^ left_shift(T[(i - 7) % 15] ^ T[(i - 2) % 15], 3) ^ (4 * i + j)

        for k in range(4):
            for i in range(15):
                T[i] = left_shift((T[i] + replacement_table(T[(i - 1) % 15])) % 2 ** 32, 9)

        for n in range(10):
            K[10 * j + n] = T[4 * n % 15]

    for i in range(5, 36, 2):
        j = K[i] & ((1 << 2) - 1)
        w = K[i] | ((1 << 2) - 1)

        M = generate_mask(w)

        five_bits = K[i - 1] & ((1 << 5) - 1)

        K[i] = w ^ (left_shift(int(B[j], 16), five_bits) & M)

    return K


def func_e(A, key1, key2):
    M = (A + key1) % 2 ** 32
    R = ((left_shift(A, 13)) * key2) % 2 ** 32
    L = replacement_table(M)
    R = left_shift(R, 5)
    M = left_shift(M, (R & ((1 << 5) - 1)))
    L = (L ^ R)
    R = left_shift(R, 5)
    L = L ^ R
    L = left_shift(L, (R & ((1 << 5) - 1)))
    return [L, M, R]


def encrypt(plaintext, key):
    round_keys = key_expansion(key)
    text = transform_data(plaintext)

    A = (text[0] + round_keys[0]) % 2 ** 32
    B = (text[1] + round_keys[1]) % 2 ** 32
    C = (text[2] + round_keys[2]) % 2 ** 32
    D = (text[3] + round_keys[3]) % 2 ** 32

    # прямое перемешивание
    for i in range(8):

        B = B ^ s0_box(A)
        B = (B + s1_box(right_shift(A, 8))) % 2 ** 32
        C = (C + s0_box(right_shift(A, 16))) % 2 ** 32
        D = D ^ s1_box(right_shift(A, 24))
        A = right_shift(A, 24)

        if (i == 0) or (i == 4):
            A = (A + D) % 2 ** 32

        if (i == 1) or (i == 5):
            A = (A + B) % 2 ** 32

        D, C, B, A = A, D, C, B

    # криптографическое ядро
    for i in range(16):
        eout = func_e(A, round_keys[2 * i + 4], round_keys[2 * i + 5])
        A = left_shift(A, 13)
        C = (C + eout[1]) % 2 ** 32
        # прямое криптопреобразование
        if i < 8:
            B = (B + eout[0]) % 2 ** 32
            D = D ^ eout[2]
        # обратное криптопреобразование
        else:
            D = (D + eout[0]) % 2 ** 32
            B = B ^ eout[2]

        D, C, B, A = A, D, C, B

    # обратное перемешивание
    for i in range(8):
        if (i == 2) or (i == 6):
            A = (A - D) % 2 ** 32

        if (i == 3) or (i == 7):
            A = (A - B) % 2 ** 32

        B = B ^ s1_box(A)
        A = left_shift(A, 8)

        C = (C - s0_box(A)) % 2 ** 32
        A = left_shift(A, 8)

        D = (D - s1_box(A)) % 2 ** 32
        A = left_shift(A, 8)
        D = D ^ s0_box(A)

        D, C, B, A = A, D, C, B

    A = (A - round_keys[36]) % 2 ** 32
    B = (B - round_keys[37]) % 2 ** 32
    C = (C - round_keys[38]) % 2 ** 32
    D = (D - round_keys[39]) % 2 ** 32

    # print(A, B, C, D)
    mas = [A, B, C, D]
    return mas


def transform_to_text(mas):
    temp = [0] * len(mas)
    for i in range(len(mas)):
        temp[i] = bin(mas[i])[2:]
    for i in range(len(temp)):
        if len(temp[i]) < 32:
            raz = 32 - len(temp[i])
            temp[i] = "0" * raz + temp[i]
    string = [0] * 16
    for i in range(len(temp)):
        for j in range(len(temp[i]) // 8):
            string[4 * i + j] = int("0b" + temp[i][8 * j: 8 * (j + 1)], 2)
    print(string)
    encrypt_text = ""
    for i in range(len(string)):
        encrypt_text += chr(string[i])

    return encrypt_text


def decrypt(encrypt_text, key):
    round_keys = key_expansion(key)
    massiv = transform_data(encrypt_text)

    A = massiv[0]
    B = massiv[1]
    C = massiv[2]
    D = massiv[3]

    A = (A + round_keys[36]) % 2 ** 32
    B = (B + round_keys[37]) % 2 ** 32
    C = (C + round_keys[38]) % 2 ** 32
    D = (D + round_keys[39]) % 2 ** 32

    for i in range(7, -1, -1):
        D, C, B, A = C, B, A, D

        A = right_shift(A, 24)

        D = D ^ s0_box(right_shift(A, 8))
        D = (D + s1_box(right_shift(A, 16))) % 2 ** 32
        C = (C + s0_box(right_shift(A, 24))) % 2 ** 32
        B = B ^ s1_box(A)

        if (i == 2) or (i == 6):
            A = (A + D) % 2 ** 32

        if (i == 3) or (i == 7):
            A = (A + B) % 2 ** 32

    for i in range(15, -1, -1):
        # A, B, C, D = D, A, B, C
        D, C, B, A = C, B, A, D

        A = right_shift(A, 13)
        eout = func_e(A, round_keys[2 * i + 4], round_keys[2 * i + 5])
        C = (C - eout[1]) % 2 ** 32
        if i < 8:
            B = (B - eout[0]) % 2 ** 32
            D = D ^ eout[2]
        else:
            D = (D - eout[0]) % 2 ** 32
            B = B ^ eout[2]

    for i in range(7, -1, -1):
        D, C, B, A = C, B, A, D

        if (i == 0) or (i == 4):
            A = (A - D) % 2 ** 32

        if (i == 1) or (i == 5):
            A = (A - B) % 2 ** 32

        A = left_shift(A, 24)

        D = D ^ s1_box(right_shift(A, 24))
        C = (C - s0_box(right_shift(A, 16))) % 2 ** 32
        B = (B - s1_box(right_shift(A, 8))) % 2 ** 32
        B = B ^ s0_box(A)

    A = (A - round_keys[0]) % 2 ** 32
    B = (B - round_keys[1]) % 2 ** 32
    C = (C - round_keys[2]) % 2 ** 32
    D = (D - round_keys[3]) % 2 ** 32

    # print(A, B, C, D)
    mas = [A, B, C, D]
    return mas


def electronic_code_book_encrypt(mas, key):
    encrypt_msg = [0] * len(mas)

    for i in range(len(mas)):
        encrypt_msg[i] = transform_to_text(encrypt(mas[i], key))
        # print(to_string(encrypt_msg[i]))

    return encrypt_msg


def electronic_code_book_decrypt(encrypt_msg, key):
    decrypt_msg = [0] * len(encrypt_msg)

    for i in range(len(encrypt_msg)):
        decrypt_msg[i] = transform_to_text(decrypt(encrypt_msg[i], key))
        # print(to_string(decrypt_msg[i]))

    return decrypt_msg


def xor_element_mas(mas1, mas2):
    n = len(mas1)
    temp = [0] * n
    for i in range(n):
        temp[i] = mas1[i] ^ mas2[i]

    return temp


def xor_str(str1, str2):
    mas_str1 = [0] * len(str1)
    mas_str2 = [0] * len(str1)
    mas_str = [0] * len(str1)
    for i in range(len(str1)):
        mas_str1[i] = ord(str1[i])
        mas_str2[i] = ord(str2[i])

    mas_str = xor_element_mas(mas_str1, mas_str2)

    str = ''
    for i in range(len(mas_str)):
        str += chr(mas_str[i])
    return str


def cipher_block_chaining_encrypt(mas, key, IV):
    encrypt_msg = [0] * len(mas)

    for i in range(len(mas)):
        if i == 0:
            plaintext = xor_str(mas[0], IV)
            encrypt_msg[i] = transform_to_text(encrypt(plaintext, key))
        else:
            plaintext = xor_str(mas[i], encrypt_msg[i - 1])
            encrypt_msg[i] = transform_to_text(encrypt(plaintext, key))
        # print(encrypt_msg[i])

    return encrypt_msg


def cipher_block_chaining_decrypt(encrypt_msg, key, IV):
    # IV = "Thats my Kung Fu"

    decrypt_str = [0] * len(encrypt_msg)

    for i in range(len(encrypt_msg)):
        if i == 0:
            plaintext = transform_to_text(decrypt(encrypt_msg[i], key))
            decrypt_str[i] = xor_str(plaintext, IV)
        else:
            plaintext = transform_to_text(decrypt(encrypt_msg[i], key))
            decrypt_str[i] = xor_str(plaintext, encrypt_msg[i - 1])
        # print(decrypt_str[i])

    return decrypt_str


def output_feedback_encrypt(mas, key, IV):
    encrypt_msg = [0] * len(mas)

    x = IV

    for i in range(len(mas)):
        if i == 0:
            y = transform_to_text(encrypt(IV, key))
            encrypt_msg[i] = xor_str(mas[i], y)
            x = y
        else:
            y = transform_to_text(encrypt(x, key))
            encrypt_msg[i] = xor_str(mas[i], y)
            x = y
        # print(encrypt_msg[i])

    return encrypt_msg


def output_feedback_decrypt(encrypt_msg, key, IV):
    # IV = "Thats my Kung Fu"

    decrypt_msg = [0] * len(encrypt_msg)

    for i in range(len(encrypt_msg)):
        if i == 0:
            y = transform_to_text(encrypt(IV, key))
            decrypt_msg[i] = xor_str(encrypt_msg[i], y)
            x = y
        else:
            y = transform_to_text(encrypt(x, key))
            decrypt_msg[i] = xor_str(encrypt_msg[i], y)
            x = y
        # print(decrypt_msg[i])

    return decrypt_msg


def ciper_feedback_encrypt(mas, key, IV):

    encrypt_msg = [0] * len(mas)

    for i in range(len(mas)):
        if i == 0:
            y = transform_to_text(encrypt(IV, key))
            encrypt_msg[i] = xor_str(mas[i], y)
        else:
            y = transform_to_text(encrypt(encrypt_msg[i - 1], key))
            encrypt_msg[i] = xor_str(mas[i], y)
        # print(encrypt_msg[i])

    return encrypt_msg


def ciper_feedback_decrypt(encrypt_msg, key, IV):
    # IV = "Thats my Kung Fu Nine Two Nine Tw"

    decrypt_msg = [0] * len(encrypt_msg)

    for i in range(len(encrypt_msg)):
        if i == 0:
            y = transform_to_text(encrypt(IV, key))
            decrypt_msg[i] = xor_str(encrypt_msg[i], y)
        else:
            y = transform_to_text(encrypt(encrypt_msg[i - 1], key))
            decrypt_msg[i] = xor_str(encrypt_msg[i], y)
        # print(decrypt_msg[i])

    return decrypt_msg


def mars_encrypt(filename, mode, key, IV):
    plaintext = read_file_in_state(filename, 16)

    if mode == 1:
        encrypt_text = electronic_code_book_encrypt(plaintext, key)
    elif mode == 2:
        encrypt_text = cipher_block_chaining_encrypt(plaintext, key, IV)
    elif mode == 3:
        encrypt_text = output_feedback_encrypt(plaintext, key, IV)
    elif mode == 4:
        encrypt_text = ciper_feedback_encrypt(plaintext, key, IV)

    print(encrypt_text)
    file_encrypt = name_file_encrypt(filename)
    write_in_file(file_encrypt, encrypt_text)


def mars_decrypt(filename, mode, key, IV):
    plaintext = read_file_in_state(filename, 16)

    if mode == 1:
        decrypt_text = electronic_code_book_decrypt(plaintext, key)
    elif mode == 2:
        decrypt_text = cipher_block_chaining_decrypt(plaintext, key, IV)

    elif mode == 3:
        decrypt_text = output_feedback_decrypt(plaintext, key, IV)
    elif mode == 4:
        decrypt_text = ciper_feedback_decrypt(plaintext, key, IV)

    print(decrypt_text)
    file_decrypt = name_file_decrypt(filename)
    write_in_file(file_decrypt, decrypt_text)
