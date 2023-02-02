from infi.clickhouse_orm import Database

from application import settings


def get_click_house_pool(db_name: str = None, timeout: int = 120):
    """
    获取ck 连接
    :param db_name: 数据库名
    :return:
    """
    db_name = f'{settings.CLICK_HOUSE_DB_PREFIX}_{db_name}'
    print(1,db_name)
    if db_name in settings.HISTORY_CLICK_HOUSE_DB_POOLS:
        return settings.HISTORY_CLICK_HOUSE_DB_POOLS[db_name]
    pool = Database(db_name,
                    db_url=settings.CLICK_HOUSE_DB_URL,
                    username=settings.CLICK_HOUSE_DB_USERNAME,
                    password=settings.CLICK_HOUSE_DB_PASSWORD,
                    timeout=timeout)
    settings.HISTORY_CLICK_HOUSE_DB_POOLS[db_name] = pool
    return pool
