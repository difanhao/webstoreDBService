import logging
import mysql.connector.pooling

from config import DB_CONFIG


logger = logging.getLogger(__name__)

# 创建数据库连接池
db_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="my_pool",
    pool_size=5,
    **DB_CONFIG
)

def _full_sql_query(base_query, paras):
    for para in paras:
        base_query = base_query.replace("%s", str(para), 1)

    return base_query

def get_db_connection():
    return db_pool.get_connection()

def fetchall_from_single_table(table_name, selected_columns=None, order_by=None, **filters):
    """
   从单表中获取指定的数据
    :param table_name: 表名
   :param selected_columns: [], 表示取的列，例如 ['id', 'openid']。
                            如果为None或为空，则默认为所有列（*）。
   :param order_by: 字典{}，表示数据排序规则，例如 {"id": "DESC", }。
                            默认为None
   :param filters: 动态参数**kwargs，用于筛选结果的过滤条件（= %s）。
   :return: [{}, ]
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    columns = "*" if not selected_columns else ", ".join(selected_columns)

    base_query = f"SELECT {columns} FROM {table_name}"

    params = []
    if filters:
        where_conditions = [f"{key} = %s" for key in filters]
        params.extend(list(filters.values()))
        base_query += " WHERE " + " AND ".join(where_conditions)

    if order_by:
        order_conditions = " ORDER BY "
        order_fragments = [f"{colume} {direction}" for colume, direction in order_by.items()]
        base_query += order_conditions + ", ".join(order_fragments)

    logger.info(_full_sql_query(base_query, params))

    try:
        cursor.execute(base_query, params)
        result = cursor.fetchall()
    except Exception as e:
        # TODO:添加异常处理
        raise e
    finally:
        cursor.close()
        conn.close()

    return result


def update_single_table(table_name, columns_to_update={}, **filters):
    """
    修改制定表的数据
    :param table_name: 表名
    :param columns_to_update: 字典{}, 修改的数据列
    :param filters: 动态参数**kwargs，用于筛选结果的过滤条件。
    :return: int，修改的数据条数
    """

    if not columns_to_update:
        raise ValueError("字典columns_to_update不能为空")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    update_query = f"UPDATE {table_name}"

    set_conditions = [f"{key}=%s" for key in columns_to_update]
    params = list(columns_to_update.values())

    update_query += " SET " + ", ".join(set_conditions)

    if filters:
        where_conditions = [f"{key}=%s" for key in filters]
        params.extend(list(filters.values()))
        update_query += " WHERE " + " AND ".join(where_conditions)

    logger.info(_full_sql_query(update_query, params))

    try:
        cursor.execute(update_query, params)
        updated_rows = cursor.rowcount
    except Exception as e:
        # TODO:添加任何必要的异常处理代码
        raise e
    finally:
        cursor.close()
        conn.commit()
        conn.close()

    return updated_rows


def delete_from_single_table(table_name, **filters):
    """
    从指定表中删除数据
    :param table_name: 表名
    :param filters: 动态参数**kwargs，用于筛选要删除的数据的过滤条件。
    :return: int，删除的数据条数
    """
    # 若未提供任何过滤条件，则抛出异常以防止误删除整个表的数据
    if not filters:
        raise ValueError("至少需要提供一个过滤条件以确保数据安全")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    delete_query = f"DELETE FROM {table_name}"

    where_conditions = [f"{key}=%s" for key in filters]
    params = list(filters.values())
    delete_query += " WHERE " + " AND ".join(where_conditions)

    logger.info(_full_sql_query(delete_query, params))

    try:
        cursor.execute(delete_query, params)
        deleted_rows = cursor.rowcount
    except Exception as e:
        # TODO:添加任何必要的异常处理代码
        raise e
    finally:
        cursor.close()
        conn.commit()
        conn.close()

    return deleted_rows


def insert_into_single_table(table_name, columns_to_insert={}):
    """
    向指定表中插入数据
    :param table_name: 表名
    :param columns_to_insert: 字典{}, 插入的数据列和值
    :return: int，插入的数据条数
    """
    if not columns_to_insert:
        raise ValueError("字典 columns_to_insert 不能为空")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    insert_query = f"INSERT INTO {table_name} "

    column_names = ", ".join(columns_to_insert.keys())
    column_values = ", ".join(["%s"] * len(columns_to_insert))

    insert_query += f"({column_names}) VALUES ({column_values})"

    params = list(columns_to_insert.values())

    logger.info(_full_sql_query(insert_query, params))

    try:
        cursor.execute(insert_query, params)
        inserted_rows = cursor.rowcount
    except Exception as e:
        # TODO: 添加任何必要的异常处理代码
        raise e
    finally:
        cursor.close()
        conn.commit()
        conn.close()

    return inserted_rows


#TODO
def direct_fetchall(query):
    logger.info(query)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except Exception as e:
        # TODO:添加异常处理
        raise e
    finally:
        cursor.close()
        conn.close()

    return result

