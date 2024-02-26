from src.app import main


def test_output_is_the_same():
    with open('golden.txt', 'r', encoding='utf-8') as f:
        expected = f.read()
    actual = main()
    assert actual == expected
