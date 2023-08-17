from db.db_operations import get_db_connection

def get_orders_from_db(selected_columns=None, order_by=None, **filters):
    """
   从vip_orders中获取指定的订单信息
   :param selected_columns: [], 表示取的列，例如 ['order_id', 'create_time']。
                            如果为None或为空，则默认为所有列（*）。
   :param order_by: 字典{}，表示数据排序规则，例如 {"create_time": "DESC", "order_id": "ASC"}。
                            默认为None
   :param filters: 动态参数**kwargs，用于筛选结果的过滤条件（= %s）。
   :return: [{}, ]
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    columns = "*" if not selected_columns else ", ".join(selected_columns)

    base_query = f"SELECT {columns} FROM vip_orders"

    params = []
    if filters:
        where_conditions = [f"{key} = %s" for key in filters]
        params.extend(list(filters.values()))
        base_query += " WHERE " + " AND ".join(where_conditions)

    if order_by:
        order_conditions = " ORDER BY "
        order_fragments = [f"{colume} {direction}" for colume, direction in order_by.items()]
        base_query += order_conditions + ", ".join(order_fragments)

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


def update_order(columns_to_update={}, **filters):
    """
    从vip_orders中修改指定的订单信息
    :param columns_to_update: 字典{}, 修改的数据列
    :param filters: 动态参数**kwargs，用于筛选结果的过滤条件。
    :return: int，修改的数据条数
    """

    if not columns_to_update:
        raise ValueError("字典columns_to_update不能为空")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    update_query = "UPDATE vip_orders"

    set_conditions = [f"{key}=%s" for key in columns_to_update]
    params = list(columns_to_update.values())

    update_query += " SET " + ", ".join(set_conditions)

    if filters:
        where_conditions = [f"{key}=%s" for key in filters]
        params.extend(list(filters.values()))
        update_query += " WHERE " + " AND ".join(where_conditions)

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


if __name__ == '__main__':
    re = get_orders_from_db(selected_columns=["id", "create_time"])
    print(re)
