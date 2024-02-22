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
        'time'             : 17,
        'e_initial_result' : 1,
        'e_final_result'   : 10.2,
        'e_iterations'     : 7,
        'other'            : 789
    }

    incomplete_dict = {
        'time'             : 17,
        'e_initial_result' : 1,
        'e_iterations'     : 7
    }

    invalid_dict = {
        'other'            : 789
    }


    assert field.has_valid_field(valid_dict) == True
    assert field.has_valid_field(incomplete_dict) == False
    assert field.has_valid_field(invalid_dict) == False

