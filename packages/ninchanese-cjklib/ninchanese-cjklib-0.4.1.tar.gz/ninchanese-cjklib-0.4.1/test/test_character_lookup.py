
def test_character_lookup():
    from cjklib import characterlookup
    lookup = characterlookup.CharacterLookup('C')
    result = lookup.getDecompositionEntries('兴')
    assert(result == [['⿳', ('⺍', 0), ('一', 0), ('八', 2)]])
