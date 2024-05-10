from LogReader.solverLog import FieldSolvingData

def test_add():
    field = FieldSolvingData(name='e')
    field.add(
        time=1, initial=1, final=0.001, nIter=10
    )
    assert field.time == [1]
    assert field.initial_residual == [1]
    assert field.final_residual == [0.001]

    field.add(
        time=2, initial=0.1, final=0.0023, nIter=7
    )

    assert field.nIterations == [10, 7]


def test__repr__():
    field = FieldSolvingData(name='e')
    field.add(
        time=2, initial=0.1, final=0.0023, nIter=7
    )
    assert field.__repr__() == '<FieldSolvingData field=e (1)>'


def test_has_valid_field():
    field = FieldSolvingData(name='e')

    valid_dict = {
        'time'              : 17,
        'e_initial_residual': [1],
        'e_final_residual'  : [10.2],
        'e_iterations'      : [7],
        'other'             : 789
    }

    multiple_dict = {
        'time'                : 17,
        'e_initial_residual'  : [1],
        'e_final_residual'    : [10.2],
        'e_iterations'        : [7],
        'rho_initial_residual': [1],
        'rho_final_residual'  : [10.2],
        'rho_iterations'      : [7],
        'other'               : 789
    }

    invalid_dict = {
        'other'            : 789
    }


    assert field.has_valid_field("", valid_dict) == True
    assert field.has_valid_field(field.name, valid_dict) == True
    assert field.has_valid_field(field.name, multiple_dict) == True
    assert field.has_valid_field(field.name, invalid_dict) == False

def test_add_from_dict():
    field = FieldSolvingData(name='e')

    valid_dict = {
        'time'              : 17,
        'e_initial_residual': [1],
        'e_final_residual'  : [10.2],
        'e_iterations'      : [7],
        'other'             : 789
    }

    field.add_from_dict(valid_dict)
    assert field.time == [17]

def test_get_field_name():

    multiple_dict = {
        'time'                : 17,
        'e_initial_residual'  : [1],
        'e_final_residual'    : [10.2],
        'e_iterations'        : [7],
        'rho_initial_residual': [1],
        'rho_final_residual'  : [10.2],
        'rho_iterations'      : [7],
        'other'               : 789
    }

    fieldNames = FieldSolvingData.get_field_names(multiple_dict)
    assert len(fieldNames) == 2
    assert 'e' in fieldNames
    assert 'rho' in fieldNames
