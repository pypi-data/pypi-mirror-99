from pollination.honeybee_radiance.sky import AddRemoveSkyMatrix, \
    GenSkyWithCertainIllum, CreateSkyDome, CreateSkyMatrix

from queenbee.plugin.function import Function


def test_add_remove_sky_matrix():
    function = AddRemoveSkyMatrix().queenbee
    assert function.name == 'add-remove-sky-matrix'
    assert isinstance(function, Function)


def test_gen_sky_with_certain_illum():
    function = GenSkyWithCertainIllum().queenbee
    assert function.name == 'gen-sky-with-certain-illum'
    assert isinstance(function, Function)


def test_create_sky_dome():
    function = CreateSkyDome().queenbee
    assert function.name == 'create-sky-dome'
    assert isinstance(function, Function)


def test_create_sky_matrix():
    function = CreateSkyMatrix().queenbee
    assert function.name == 'create-sky-matrix'
    assert isinstance(function, Function)
