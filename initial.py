import hypothesis
from hypothesis import given, settings, Verbosity, strategies as st, assume, target
# Also pip install pytest


# Simple addition function
def add(num1, num2):
    return num1 + num2

# Run with pytest filename.py --hypothesis-show-statistics -s (examples)
@settings(verbosity=Verbosity.verbose)
@given(st.integers(), st.integers())
def test_add(num1, num2):
    result = add(num1, num2)
    assert(result == (num1 + num2))


def find_majority(lon):
    # Dictionary num1 : num2, num1 represents the number, num2 represents the count of number
    count_dict = {}

    # Iterating over input lon
    for number in lon:
        # Increments if exists, sets as 0 + 1 otherwise
        count_dict[number] = count_dict.get(number, 0) + 1

    for number, count in count_dict.items():
        # If the occurence count is greater than length / 2 then it is a majority element
        if count > (len(lon) / 2):
            return number

    # Returns -1 if not found
    return -1


@settings(verbosity=Verbosity.verbose)
@given(st.lists(st.integers().filter(lambda x: 10 > x > 0)))  # Filtering to encourage duplicates
def test_find_majority(lon):  # Works the same as the prop function in Racket
    result = find_majority(lon)  # Getting result from tested func
    assume(not (result == -1))  # Assume essentially ignores lists in which we do not have a dupe

    majority_size = len(lon) / 2
    count_of_results = sum(1 for number in lon if number == result)  # Counts the number of result in lon
    assert(count_of_results > majority_size)  # Asserts that this is true to pass test


def remove_triple_one_plus_strings(lon):
    result = []
    for number in lon:
        if str(number).count('1') < 3:
            result.append(number)
    return result


@settings(verbosity=Verbosity.verbose, max_examples=100)
@given(st.lists(st.integers(), max_size=10))
def test_remove_triple_one_strings(lon):
    assume(len(lon) > 0)
    results = remove_triple_one_plus_strings(lon)
    onecount = 0
    for number in results:
        onecount += str(number).count('1')
    target(onecount)
    for number in results:
        assert(3 > str(number).count('1'))
    remaining_lon = set(lon) - set(results)
    for number in remaining_lon:
        assert(3 <= str(number).count('1'))











