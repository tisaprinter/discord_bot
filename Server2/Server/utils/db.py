
import aiomysql
import mysql.connector
from cfg import DATABASE

def cmd(cmd, value=None, database=DATABASE['NAME'],):
    # print("==>%s: %s", cmd, DATABASE['NAME'])
    conn = mysql.connector.connect(
    host=DATABASE['HOST'],
    user=DATABASE['USER'],
    password=DATABASE['PASS'],
    database=database
    )

    c = conn.cursor()
    if type(value) is tuple:
        value = value
    elif value is not None:
        value = (value,)

    c.execute(cmd, value)

    conn.commit()
    conn.close()

def get_value(target, table="", search_filter=None, value=None, order=None, limit=None, arr=False, database=DATABASE['NAME'],):
    conn = mysql.connector.connect(
    host=DATABASE['HOST'],
    user=DATABASE['USER'],
    password=DATABASE['PASS'],
    database=database
    )

    c = conn.cursor()

    sql = f"SELECT {target} from {table}"
    if search_filter is not None:
        sql += f" WHERE {search_filter}=%s"

    if order is not None:
        sql += f" ORDER BY {order}"

    if limit is not None:
        sql += f" LIMIT {limit}"

    if type(value) is tuple:
        c.execute(sql, value)
    elif not value:
        c.execute(sql)
    else:
        c.execute(sql, (value,))

    if arr:
        res = c.fetchall()
    else:
        res = c.fetchone()
    try:
        conn.commit()
    except:
        pass
    conn.close()
    if not res and not arr:
        return None

    elif not res and arr:
        return []

    if arr:
        if target == "*":
            return res
        return [row[0] for row in res]
    return res[0]



async def async_cmd(cmd, value=None, database=DATABASE['NAME']):
    conn = await aiomysql.connect(
    host=DATABASE['HOST'],
    user=DATABASE['USER'],
    password=DATABASE['PASS'],
    db=database
    )
    c = await conn.cursor()
    if type(value) is tuple:
        value = value
    elif value is not None:
        value = (value,)
    await c.execute(cmd, value)
    await conn.commit()


async def async_get_value(target, database=DATABASE['NAME'], table="", searchFilter=None, value=None, order=None, limit=None, arr=False):
    conn = await aiomysql.connect(
    host=DATABASE['HOST'],
    user=DATABASE['USER'],
    password=DATABASE['PASS'],
    db=database
    )

    c = await conn.cursor()

    sql = f"SELECT {target} from {table}"
    if searchFilter is not None:
        sql += f" WHERE {searchFilter}=%s"

    if order is not None:
        sql += f" ORDER BY {order}"

    if limit is not None:
        sql += f" LIMIT {limit}"

    if type(value) is tuple:
        await c.execute(sql, value)
    elif not value:
        await c.execute(sql)
    else:
        await c.execute(sql, (value,))

    if arr:
        res = await c.fetchall()
    else:
        res = await c.fetchone()

    await conn.commit()

    if not res and not arr:
        return None

    elif not res and arr:
        return []

    if arr:
        if target == "*":
            return res
        return [row[0] for row in res]
    return res[0]


