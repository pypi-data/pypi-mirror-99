import pytest
from limeutils.utils import byte_conv
from icecream import ic

# from limeutils import Red
# from limeutils.redis.models import StarterModel
#
#
#












param = ['abc', 123, 12.5, 0, 'foo', 'foo', '']
@pytest.mark.parametrize('k', param)
# @pytest.mark.focus
def test_set(red, k):
    assert red.set('sam', k)
    assert red.get('sam') == k
    

# @pytest.mark.focus
def test_list(red):
    red.delete(red.formatkey('many'))
    red.set('many', ['a'])
    red.set('many', ['b'])
    red.set('many', ['c'], direction='lpush')
    red.set('many', ['d'], direction='lpush')
    assert red.llen(red.formatkey('many')) == 4
    assert (red.get('many')) == ['d', 'c', 'a', 'b']
    red.set('many', ['foo', 'bar'])
    assert red.llen(red.formatkey('many')) == 6
    assert (red.get('many')) == ['d', 'c', 'a', 'b', 'foo', 'bar']
    red.set('many', ['', 'meh'])
    assert red.llen(red.formatkey('many')) == 8
    assert (red.get('many')) == ['d', 'c', 'a', 'b', 'foo', 'bar', '', 'meh']


# @pytest.mark.focus
def test_hash(red):
    red.delete(red.formatkey('user'))
    red.set('user', dict(age=34, username='enchance', gender='m'))
    assert red.get('user') == dict(age=34, username='enchance', gender='m')
    assert red.get('user', fields='username') == dict(username='enchance')
    assert red.get('user', fields=['age', 'gender']) == dict(age=34, gender='m')


# @pytest.mark.focus
def test_set_data(red):
    red.delete(red.formatkey('norepeat'))
    red.set('norepeat', {'b', 'a', 'c', 'd', 'a'})
    assert red.get('norepeat') == {'d', 'a', 'b', 'c'}   # unordered of course


# @pytest.mark.focus
def test_exists(red):
    red.set('one', 432.5)
    red.set('two', ['b'])
    red.set('three', dict(age=34, username='enchance', gender='m'))
    assert red.exists('one')
    assert red.exists('one', 'two', 'three')

# param = [('football', 'team', 'chelsea', 1), ('football', 'team', 'barca', 0),
#          ('football', '', '', 1)]
# @pytest.mark.parametrize('k, f, v, out', param)
# def test_hset(red, k, f, v, out):
#     assert red.hset(k, f, v) == out






# param = [(dict(bbb=2, ccc=42), 2), (dict(aaa=1, bbb=2), 1), (dict(bbb=54, ccc=42), 0), ({}, 0)]
# @pytest.mark.parametrize('m, o', param)
# def test_hmset(r, m, o):
#     assert r.hmset('foobar', mapping=m) == o
#
#
# param = [('foo', 4, 'bar'), ('fed', 4, 23), ('', 4, 4), ('zoom', 4, 4), ('nonexistent', 4, 4),
#          ('nothing', 4, 0)]
# @pytest.mark.parametrize('f, v, o', param)
# def test_hget(r, f, v, o):
#     assert r.hget('abra', f, v) == o
#
#
# param = [(['foo', 'fed'], dict(foo='bar', fed=23)), (['nothing'], dict(nothing=0)),
#          ([], {}), (None, dict(foo='bar', fed=23, meh=5.2, nothing=0, zoom=''))]
# @pytest.mark.parametrize('k, o', param)
# def test_hmget(r, k, o):
#     assert r.hmget('abra', k) == o
#
#
# param = [('ccc', 1), ('xxx', 0), (['aaa', 'bbb'], 2), (['ddd', 'zzz'], 1)]
# @pytest.mark.parametrize('k, out', param)
# def test_hdel(r, k, out):
#     assert r.hdel('mustard', k) == out
#
#
# param = [('aaa1', 1), (['aaa2', 'aaa3'], 2), ('aaa3', 0), (['aaa5'], 1), ('', 0),
#          (['xxx', 'aaa4'], 1)]
# @pytest.mark.parametrize('k, out', param)
# def test_delete(r, k, out):
#     assert r.delete(k) == out
#
#

#
#
# param = [('qqq', 789, 'abc'), ('www', 789, 123), ('rrr', 789, 789), ('lll', 789, 789),
#          ('lll', None, '')]
# @pytest.mark.parametrize('k, v, out', param)
# # @pytest.mark.focus
# def test_get(r, k, v, out):
#     if v is not None:
#         assert r.get(k, v) == out
#     else:
#         assert r.get(k) == out
#
# @pytest.mark.focus
# def test_exists(r):
#     # ic(r.fullkey('aaa'))
#     try:
#         # ic(type(r), r)
#         # x = r.fullkey('apples')
#         # ic(x)
#         # data = StarterModel(key='apples', pre=r.pre, ver=r.ver)
#         # x = r.cleankey(data)
#         # ic(x)
#         pass
#     except Exception as e:
#         ic(e)
#     # assert r.conn.exists('MALICE:apples')
#     # r.set('apples', 'to lemons')
#     # assert r.conn.exists()
