from redis import Redis
from typing import Optional, Union, Any
from pydantic import BaseModel
from redis.client import list_or_args

from . import models
from icecream import ic
from .models import LIST, VAL, StarterModel
from limeutils import byte_conv




class Red(Redis):
    
    def __init__(self, *args, **kwargs):
        self.pre = kwargs.pop('pre', '')
        self.ver = kwargs.pop('ver', '')
        self.ttl = kwargs.pop('ttl', -1)
        super().__init__(*args, **kwargs)
        # self.pipe = self.pipeline()

    
    def formatkey(self, key: str) -> str:
        """
        Create the final key name with prefix and/or version
        :param key: The key to format
        :return:    str
        """
        pre = self.pre.strip()
        ver = self.ver.strip()

        list_ = [pre, ver, key]
        list_ = list(filter(None, list_))
        return ":".join(list_)


    def set(self, key: str, val: Union[VAL, LIST, set], **kwargs):
        key = self.formatkey(key)
        if isinstance(val, (str, int, float, bytes)):
            return super().set(key, val, **kwargs)
        elif isinstance(val, (list, tuple)):
            direction = kwargs.pop('direction', 'rpush')
            return getattr(super(), direction)(key, *val)
        elif isinstance(val, dict):
            return super().hset(key, mapping=val)
        elif isinstance(val, set):
            return super().sadd(key, *val)
    
    
    def get(self, key: str, start: Optional[int] = 0, end: Optional[int] = -1,
            fields: Optional[Union[LIST, str]] = None):
        key = self.formatkey(key)
        datatype = byte_conv(super().type(key))
        
        if datatype == 'string':
            return byte_conv(super().get(key))
        elif datatype == 'list':
            data = super().lrange(key, start, end)
            return [byte_conv(i) for i in data]
        elif datatype == 'hash':
            if fields:
                fields = [fields] if isinstance(fields, str) else list(fields)
                data = super().hmget(key, fields)
                data = [byte_conv(i) for i in data]
                d = dict(zip(fields, data))
            else:
                data = super().hgetall(key)
                d = {byte_conv(k):byte_conv(v) for k, v in data.items()}
            # ic(d)
            return d
        elif datatype == 'set':
            data = super().smembers(key)
            return {byte_conv(v) for v in data}
            
    
    def exists(self, *keys):
        keys = [self.formatkey(i) for i in keys]
        return super().exists(*keys)
        
        # data = models.Set(key=key, val=val, xx=xx, keepttl=keepttl, ttl=ttl, pre=pre, ver=ver)
        # key = self.formatkey(data)
        # ttl = data.ttl if data.ttl is not None else self.ttl
        #
        # self.pipe.set(key, data.val, xx=data.xx, keepttl=data.keepttl)
        # self.pipe.expire(key, ttl)
        # [set_ret, _] = self.pipe.execute()
        # return set_ret

# class Redis:
#     def __init__(self, **kwargs):
#         self.conn = reds.Redis(**kwargs)
#
#
#
#
#
#     def hset(self, key: str, field: str, val: Optional[V] = '', mapping: Optional[dict] = None,
#              ttl=None, pre=None, ver=None) -> int:
#         """
#         Add a single hash field using HSET
#         :param key:     Hash key name
#         :param field:   Field in the key
#         :param val:     Value
#         :param mapping: For multiple fields
#         :param ttl:     Custom ttl
#         :param pre:     Custom prefix
#         :param ver:     Custom version
#         :return:        Number of fields set. Updating an existing field counts as 0 not 1.
#         """
#         data = models.Hset(key=key, field=field, val=val, mapping=mapping,
#                            ttl=ttl, pre=pre, ver=ver)
#         key = self.cleankey(data)
#         ttl = data.ttl if data.ttl is not None else self.ttl
#
#         self.pipe.hset(key, data.field, data.val, data.mapping)
#         self.pipe.expire(key, ttl)
#         [hset_ret, _] = self.pipe.execute()
#         return hset_ret