# Overview of Problem
## Part 1
Part 1 was to check for how many times the number increased from the previous number
## Part 2
Part 2 was to check for if the sum of the previous sliding window of size 3 was greater than the current sum of the sliding window and for checking how many times that occurred.

# My Thought Process
## Part 1
I decided to simply compare the current item and the "look ahead" item (the next item after the current item) and check if the look ahead item was greater and to check the length of that.
## Part 2
This one was a bit more complex than the first part.
I decided to create a sliding window by getting the input and a slice of it from `input[current_index:current_index+3]`
Then I just set the `prev_sum` to be the current sum of the window for the next iteration and checked if the current window had a sum greater than the previous sum, and incremented a counter by 1.

