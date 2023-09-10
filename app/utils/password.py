from fastapi import HTTPException

# import psycopg2
import bcrypt

import logging

# def connection():
#     return psycopg2.connect(dbname='auth', user='postgres',
#                             password='pgRolefrTestPass', host='207.180.242.3')


def hash_password(pw):
    pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    return pwhash.decode('utf8')


def check_password(pw, hashed_pw):
    try:
        expected_hash = hashed_pw.encode('utf8')
        return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
    except Exception as e:
        return False
    return True


def compare_passwords(
    hashed_password: str,
    plain_password: str,
) -> bool:
    try:
        expected_hash = hashed_password.encode('utf8')
        bcrypt.checkpw(
            plain_password.encode('utf8'),
            expected_hash,
        )
    except Exception as e:
        logging.exception(e)
        return False
    return True


# class RaisableHTTPException(HTTPException):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#     def __bool__(self):
#         return False
