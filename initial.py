from hypothesis import given, settings, Verbosity, strategies as st, assume
# Also pip install pytest


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


@settings(verbosity=Verbosity.verbose)  # Run with pytest filename.py -s to see examples
@given(st.lists(st.integers().filter(lambda x: 10 > x > 0)))  # Filtering to encourage duplicates
def test_find_majority(lon):  # Works the same as the prop function in Racket
    result = find_majority(lon)  # Getting result from tested func
    assume(not (result == -1))  # Assume essentially ignores lists in which we do not have a dupe

    majority_size = len(lon) / 2
    count_of_results = sum(1 for number in lon if number == result)  # Counts the number of result in lon
    assert(count_of_results > majority_size)  # Asserts that this is true to pass test








