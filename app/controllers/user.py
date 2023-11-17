from asyncpg import Connection

from plugins.controllers import (
    DatabaseManager as DM,
    insert_q,
    select_q_detailed,
    select_q,
    update_q,
    delete_q,
)

from app.schemas.user import (
    UserInDBProtected,
    UserInDBWithPassword,
    UserCreateProtected,
    UserUpdateProtected,
)
from app.schemas.password import (
    Password,
)


@DM.acqure_connection()
async def get_by_id(
    user_id: int,
    conn: Connection = None,
) -> UserInDBProtected:
    result = await conn.fetchrow(*select_q_detailed(
        'user_account',
        UserInDBProtected,
        id=user_id,
    ))
    if not result:
        return result
    return UserInDBProtected(**result)


@DM.acqure_connection()
async def get_by_username(
    username: str,
    conn: Connection = None,
) -> UserInDBProtected:
    result = await conn.fetchrow(*select_q_detailed(
        'user_account',
        UserInDBProtected,
        username=username,
    ))
    if not result:
        return result
    return UserInDBProtected(**result)


@DM.acqure_connection()
async def sys_get_by_username(
    username: str,
    conn: Connection = None,
) -> UserInDBWithPassword:
    result = await conn.fetchrow(*select_q(
        'user_account',
        username=username,
    ))
    if not result:
        return result
    return UserInDBWithPassword(**result)


@DM.acqure_connection()
async def save(
    user_data: UserCreateProtected,
    conn: Connection = None,
) -> UserInDBProtected:
    result = await conn.fetchrow(*insert_q(user_data, 'user_account'))
    if not result:
        return result
    user = UserInDBProtected(**result)
    return user


@DM.acqure_connection()
async def update(
    user_id: int,
    user_data: UserUpdateProtected,
    conn: Connection = None,
) -> UserInDBProtected:
    result = await conn.fetchrow(
        *update_q(user_data, 'user_account', id=user_id)
    )
    if not result:
        return result
    user = UserInDBProtected(**result)
    return user


@DM.acqure_connection()
async def update_discord_id(
    user_id: int,
    discord_id: str,
    conn: Connection = None,
) -> UserInDBProtected:
    result = await conn.fetchrow(
        'update user_account set discord_id = $1 where id = $2 returning *',
        discord_id,
        user_id,
    )
    if not result:
        return result
    user = UserInDBProtected(**result)
    return user


@DM.acqure_connection()
async def set_password(
    user_id: int,
    password: Password,
    conn: Connection = None,
) -> UserInDBProtected:
    password.hash_password()
    result = await conn.fetchrow(
        'update '
            'user_account '
        'set '
            'password = $1 '
        'where '
            'id = $2 '
        'returning * ',
        password.password.get_secret_value(),
        user_id,
    )
    if not result:
        return result
    user = UserInDBProtected(**result)
    return user


@DM.acqure_connection()
async def add_email(
    user_id: int,
    email: str,
    conn: Connection = None,
) -> UserInDBProtected:
    result = await conn.fetchrow(
        'update '
            'user_account '
        'set '
            'emails = array_append(emails, $1) '
        'where '
            'id = $2 '
        'returning *',
        email,
        user_id,
    )
    if not result:
        return result
    print(result)
    user = UserInDBProtected(**result)
    return user


@DM.acqure_connection()
async def remove_email(
    user_id: int,
    email: str,
    conn: Connection = None,
) -> UserInDBProtected:
    result = await conn.fetchrow(
        'update '
            'user_account '
        'set '
            'emails = array_remove(emails, $1) '
        'where '
            'id = $2 '
        'returning *',
        email,
        user_id,
    )
    if not result:
        return result
    user = UserInDBProtected(**result)
    return user


@DM.acqure_connection()
async def delete(
    user_id: int,
    conn: Connection = None,
) -> UserInDBProtected:
    result = await conn.fetchrow(
        *delete_q('user_account', id=user_id)
        # 'delete from user_account  '

    )
    if not result:
        return result
    user = UserInDBProtected(**result)
    return user
