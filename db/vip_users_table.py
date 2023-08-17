from .db_operations import get_db_connection

def get_user_tag_by_user_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    select_query = "SELECT tag FROM vip_users WHERE user_id = %s"
    cursor.execute(select_query, (user_id, ))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


def update_user_tag_by_user_id(user_id, tag):
    """
    修改vip_users中对应的用户tag
    :param user_id:
    :param tag:
    :return: int，修改的数据条数
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    update_query = "UPDATE vip_users SET tag = %s WHERE user_id = %s"
    cursor.execute(update_query, (tag, user_id))

    updated_rows = cursor.rowcount

    cursor.close()
    conn.commit()
    conn.close()

    return updated_rows