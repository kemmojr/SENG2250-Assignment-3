import base64
import binascii
import math
import random
import hashlib
import socket


def mod_exponentiation(base, exponent, modulus):
    if modulus == 1:
        return 0

    result = 1
    while exponent > 0:
        if (exponent & 1) == 1:  # Is the number odd
            result = (result * base) % modulus

        exponent = exponent >> 1
        base = (base * base) % modulus

    return result


def get_rsa_prime():
    bit_size = 1024
    early_primes_list = {
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67,
        71, 73, 79, 83, 89, 97, 101, 103,
        107, 109, 113, 127, 131, 137, 139,
        149, 151, 157, 163, 167, 173, 179,
        181, 191, 193, 197, 199, 211, 223,
        227, 229, 233, 239, 241, 251, 257,
        263, 269, 271, 277, 281, 283, 293,
        307, 311, 313, 317, 331, 337, 347, 349}

    prime_candidate = 0
    condition = False
    while not condition:
        # Low level primality test that checks if the generated number is not divisible by the early prime numbers
        prime_candidate = get_n_bit_number(bit_size)

        for div in early_primes_list:
            if prime_candidate % div == 0:
                break
            else:
                condition = True

        if rabin_miller_test(prime_candidate):
            break
        else:
            condition = True

    return prime_candidate


def rabin_miller_test(rabin_miller_testing):
    # does 20 rounds of the rabin-miller primality test. this code is from:
    # https://www.geeksforgeeks.org/how-to-generate-large-prime-numbers-for-rsa-algorithm/
    max_divisions_by_two = 0
    ec = rabin_miller_testing - 1
    while ec % 2 == 0:
        ec >>= 1
        max_divisions_by_two += 1
    assert(2**max_divisions_by_two * ec == rabin_miller_testing -1)

    def trial_test(tester):
        if mod_exponentiation(tester, ec, rabin_miller_testing) == 1:
            return False
        for i in range(max_divisions_by_two):
            if mod_exponentiation(tester, 2**i * ec, rabin_miller_testing) == rabin_miller_testing -1:
                return False
        return True

    number_of_tests = 20
    for i in range(number_of_tests):
        round_test = random.randrange(2, rabin_miller_testing)
        if trial_test(round_test):
            return False
    return True


def get_n_bit_number(size):
    return random.randrange(2 ** (size - 1) + 1, 2 ** size - 1)


def euclidean_alg(a, b): # gets the GCD of a and b
    if a == 0:
        return b
    elif b == 0:
        return a

    q = int(a/b)
    r = a % b
    return euclidean_alg(b, r)


def extended_euclidean_alg(base, mod, i):
    if i == 0 or i == 1:
        p = i
    else:
        p = 2
    p = 0
    rem = mod % base
    n_mod = base
# p = get_rsa_prime()
# q = get_rsa_prime()
p = 3
q = 11
# e = 65537  # public key
e = 7
n = p*q
m = (p-1)*(q-1)
d1 = (1 % m)/e
d = 1/e
# X - plaintext, Y - ciphertext
# Encryption Y = X**e % n
# Decryption X = Y**d % n
X = binascii.hexlify(b"This is the plaintext")
X = int(X, 16)
M = 6
encrypt = M**e % n
decrypt = encrypt**d % n
# Y = mod_exponentiation(X, e, n)
# decrypted = mod_exponentiation(Y, d, n)
# print(decrypted)
# print(mod_exponentiation(crypt, 7, 26))

h1 = hashlib.sha256(b"Thing to be hashed")
h2 = hashlib.sha256(b"Thing to be hashed")


HOST = ''
PORT = 60051

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:  # send all the communication that is on the server side of the SSL handshake
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data: break
            if data == b'Client Hello':
                print("message recieved! message information:\n")
                conn.sendall(b'Server Continue')
                data = conn.recv(1024)
                print(str(data))
                conn.sendall(b'Server Hello')
                data = conn.recv(1024)
                conn.sendall(b'SSL version that the server and client support\\'
                             b'Timestamp\\nonce\\Session ID\\Selected cipher\\Selected compression method')
                data = conn.recv(1024)
                conn.sendall(b'Server Hello Done')
                # Server finished - changes it's cipher spec and responds finished

                # conn.sendall(b'Server finished')
            elif data == b'Client Finished':
                conn.sendall(b'Server finished')
                print("Server has Finished")
            else:
                conn.sendall(data)
                print("Received "+str(data))


