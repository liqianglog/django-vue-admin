from infi.clickhouse_orm import Database

from application import settings


def get_click_house_pool(brand_owner_id: int = None, timeout: int = 120, db_name=None):
    """
    获取ck 连接
    :param brand_owner_id: 品牌商ID
    :return:
    """
    if brand_owner_id in settings.HISTORY_CLICK_HOUSE_DB_POOLS:
        return settings.HISTORY_CLICK_HOUSE_DB_POOLS[brand_owner_id]
    if not db_name:
        db_name = f'{settings.CLICK_HOUSE_DB_PREFIX}_code_{brand_owner_id}'
    pool = Database(db_name,
                    db_url=settings.CLICK_HOUSE_DB_URL,
                    username=settings.CLICK_HOUSE_DB_USERNAME,
                    password=settings.CLICK_HOUSE_DB_PASSWORD,
                    timeout=timeout)
    settings.HISTORY_CLICK_HOUSE_DB_POOLS[brand_owner_id] = pool
    return pool
