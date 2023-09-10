import secrets
import string


def generate_secret(length: int = 64):
    alplhabet = string.ascii_letters + string.digits
    # return ''.join(secrets.choise(alplhabet)) for _ in range(length)
    result = ''
    for _ in range(length):
        result = f'{result}{secrets.choice(alplhabet)}'
    return result