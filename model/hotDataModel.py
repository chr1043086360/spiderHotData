import orm
from dao.initMysql import database, metadata


class HotData(orm.Model):

    __tablename__ = "hotdata"
    __database__ = database
    __metadata__ = metadata

    id = orm.Integer(primary_key=True)
    title = orm.String(max_length=30, allow_null=False)
    info = orm.Text()
    search_num = orm.Boolean(default=False, allow_null=False)
    created_at = orm.DateTime()
