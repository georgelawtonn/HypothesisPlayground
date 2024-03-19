### Introduction to Hypothesis, A Python Based PBT Library
As you might have guessed from the title, I will be covering a general introduction into Hypothesis a property based testing library that can be used within Python.  Similiar to other property based testing library's from other languages, Hypothesis works by generating a range of randomized (yet constrained) tests inputs, and checking the results of the tested function. In general, by implementing the usage of Hypothesis throughout the development process, we will be able to more robustly test our functions,  more easily find bugs, and improve our code on a fundamental level.

With that said, let's dive a little deeper with an example. Seen below is a simple addition function with a basic Hypothesis tester function. As you can see quite clearly the base function essentially just adds two numbers. Now while keeping that in mind let's look at the Hypothesis function. Beginning with the first line, we see the @settings option. In this particular instance, @settings is only changing the verbosity of the test_add function. However, this specific functionality is amongst others that this library has in order to go about properly testing our function, within @settings we have the ability to modify max-example count, the deadline, as well as [other functionalities](https://hypothesis.readthedocs.io/en/latest/settings.html#hypothesis.settings). Let's now evaluate the next line, "@given(st.integers(), st.integers())", as you may be able to see @given essentially creates the constraints on what will be generated as input for the function. As we move forward with the examples you will be able to see just how @given can be modified, but as a general guideline the commas  seperate the inputs and the st._____ defines what type is generated as input. By integrating the use of Hypothesis in our development cycle we will expand our base understanding of our code, and be able to more concretely verify that a piece of code actually works as intended, rather than just pass a couple of unit tests. 

```
# Simple addition function  
def add(num1, num2):  
 return num1 + num2  
  
# Run with pytest filename.py --hypothesis-show-statistics -s (examples)  
@settings(verbosity=Verbosity.verbose)  
@given(st.integers(), st.integers())  
def test_add(num1, num2):  
  result = add(num1, num2)  
  assert(result == (num1 + num2))
  ```

Now that we have a base understanding of how the Hypothesis PBT library works, lets dive a little deeper into the features that help us as developers. In the function below we have a find_majority function that takes in a list of numbers and returns either -1 if there is no majority, or the number that is the majority if there is one. Like before we set the verbosity such that when run with "pytest file_name.py --hypothesis-show-statistics -s" with the "-s" we are able to see the generated inputs being sent into the tester function. Moving forward we recognize much of the same layout as last time, however within the @given, you may recognize that st.integers() has a filter such that the elements of the list can only be generated with integers from 0 to 10. In this particular scenario we have put this filter condition in order to generate lists with duplicates (which makes it more likely to generate a majority), however the idea that we may put filters and additional conditions is a feature that can do much more and vastly improve the capabilities/ability to perform property based testing. Another interesting feature within hypothesis that can further the completeness of testing is the assume function that is supported by Hypothesis. If you are to look below you may notice we use assume to "assume(not (result == -1))", the assume function essentially makes it so that we ignore inputs that result in -1, while still asserting that the function works properly for functions that do not (those that have a majority in this specific scenario). Through Hypothesis's support of assume, we have the ability to further the ability of our testing functions and property based testing.

```
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
@given(st.lists(st.integers().filter(lambda x: 10 > x > 0))) # Filtering to encourage duplicates  
def test_find_majority(lon): # Works the same as the prop function in Racket  
  result = find_majority(lon) # Getting result from tested func  
  assume(not (result == -1)) # Assume essentially ignores lists in which we do not have a dupe  
  
  majority_size = len(lon) / 2  
  count_of_results = sum(1 for number in lon if number == result) # Counts the number of result in lon  
  assert(count_of_results > majority_size) # Asserts that this is true to pass test
```
With this last example we'll cover some more of the features that Hypothesis offers, and then finally discuss the benefits, and weaknesses that Hypothesis has if we are to integrate it into our development process.  In this example much of the @settings, and @given are the same as we've seen with the past two examples, so these will not be covered. However what we will be covering is target, and the asserts. To begin let's cover the target feature, in this particular example target is targetting onecount, which is essentially the number of '1's post removing all words with more than three '1's within the string representation of the number. Targetting a specific value tends to make subsequent test generations have a higher value for this target, this is a beneficial tool as it allows for one to more thouroughly test cases which may appear less frequently. This functionality is highly beneficial when testing for certain edge cases, and on a general level makes testing far easier. In addition to that both targets and asserts can assert/target multiple times within a tester function. That is to say that we may target various different bounds, as well as assert multiple times, to more easily verify that a function worked as intended. 
```
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
 ```

All in all, Hypothesis offers significant advantages through its automated test case generation, helping catch edge cases that traditional unit tests might miss, and allowing the ability to specify input constraints, rather than typing out individual test cases. While we should recognize that property based testing will require a change in mindset, and understanding of code, the benefits far outweight the negatives.  Therefore, Hypothesis should be integrated within our development cycles. 


### Library Proposal: Hypothesis
As you may have heard from others within the software development team, we are considering adopting Hypothesis as a new tool for all future and present code in our codebase.  After evaluating the capabilities of our current testing enviornment, and the potential that Hypothesis offers, I highly reccomend that we integrate Hypothesis into our normal testing procedure. By integrating this library we will be able more robustly verify that our code works as intended through testing that allows for us to test functionality through properties of inputs and results, rather than just individual test cases. In other words, by using Hypothesis, we will be able to test the absolute limits of our code, covering both common and edge cases, that we simply would not be able to find through traditional testing. This improved approach to testing will most assuredly lead to a higher quality product, and a improved experience for end users.

Now assuming that you approve of this integration what would this mean for the team. Well, at a base level adopting a new technology into our development cycle means that we need time to adapt to said technology. However, to be more specific to this library, integrating Hypothesis will need a shift in our mindset that may increase time thinking about properties of code, and decrease the amount of time that would have been spent manually creating individual test cases. All, in all, this adoption of Hypothesis while daunting at first, will lead to an improved product, with minimal cost in terms of time. 

