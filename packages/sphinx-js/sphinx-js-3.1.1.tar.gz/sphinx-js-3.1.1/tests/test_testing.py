from tests.testing import dict_where, NO_MATCH


def test_dict_where():
    json = {'hi': 'there', 'more': {'mister': 'zangler', 'and': 'friends'}}
    assert dict_where(json, mister='zangler') == {'mister': 'zangler', 'and': 'friends'}
    assert dict_where(json, mister='zangler', fee='foo') == NO_MATCH
    assert dict_where(json, hi='there') == json
