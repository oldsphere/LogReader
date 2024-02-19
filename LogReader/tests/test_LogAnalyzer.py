from LogReader.LogAnalyzer import LogAnalyzer
from LogReader.LineAnalyzer import LineAnalyzer, TypeLineAnalyzer


def test_add_analyzer():
    basic = LogAnalyzer()
    liner = LineAnalyzer(name="test", condition="mimi")
    basic.add_analyzer(liner)

    assert liner in basic.analyzers


def test_add_numeric_regex():
    basic = LogAnalyzer()
    pattern = r"First number: (?P<first>\d+) Second Number: (?P<second>\d+\.?\d*)"
    basic.add_numeric_regex(pattern)

    liner = TypeLineAnalyzer(name="test", condition=pattern, conversor=(float, float))

    assert basic.analyzers[0].condition == liner.condition
    assert basic.analyzers[0].conversors == liner.conversors


def test_add_regex():
    basic = LogAnalyzer()
    pattern = r"First number: (?P<first>\d+) Second Number: (?P<second>\d+\.?\d*)"
    basic.add_regex(pattern)

    assert basic.analyzers[0].condition == pattern


def test_parse():
    basic = LogAnalyzer()
    basic.add_numeric_regex(
        r"First number: (?P<first_value>\d+)\s*,\s*Second number: (?P<second_value>\d+\.?\d*)"
    )
    basic.add_regex(r"^-\s*(?P<casename>\w+)\s*-$")
    basic.add_numeric_regex(r"Elapsed Time = (?P<elapsedTime>\d+\.?\d*) s")

    content = (
        "- my_case -\n"
        "* Computing... OK\n"
        "* Getting results\n"
        "The results obtained from the case are:\n"
        "    First number: 10 , Second number: 6328.3\n"
        "There are no more results\n"
        "Elapsed Time = 316.0 s\n"
        "- end of my_case -\n"
    )

    results = basic.parse(content)

    assert results['casename'] == ['my_case']
    assert results['first_value'] == [10]
    assert results['second_value'] == [6328.3]
    assert results['elapsedTime'] == [316.0]


def test_is_name_collision():

    collision_dict = {
        "dict1" : { 'name' : 'carlos' },
        "dict2": { 'name' : 'josé' }
    }
    non_collision_dict = {
        "dict1" : { 'name_1' : 'carlos' },
        "dict2": { 'name_2' : 'josé' }
    }

    assert LogAnalyzer.is_name_collision(collision_dict) == True
    assert LogAnalyzer.is_name_collision(non_collision_dict) == False

def test_single_results():

    basic = LogAnalyzer()
    basic.single_value_analyzers.append('test')
    out = basic.single_results({
        'test' : {
            'mimi' : [1]
        }
    })
    assert out['test']['mimi'] == 1


def test_parse_single_value_OK():
    basic = LogAnalyzer()
    basic.add_numeric_regex(r"Elapsed Time = (?P<elapsedTime>\d+\.?\d*) s", single_value=True)

    content = (
        "Elapsed Time = 316.0 s\n"
    )

    results = basic.parse(content)

    assert results['elapsedTime'] == 316.0
