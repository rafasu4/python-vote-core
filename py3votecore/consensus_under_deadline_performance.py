import random
import time
import matplotlib.pyplot as plt
from consensus_under_deadline import mdvr

TOTAL_VOTERS = 250
TOTAL_ALTERNATIVES = 26
CHARS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def measure_running_time(func, *args):
    start_time = time.perf_counter()
    func(*args)
    end_time = time.perf_counter()
    return end_time - start_time

def create_random_alternatives_preference(size):
    # Create a list of characters to choose from
  
    arr = []

    for i in range(size):
        arr.append(CHARS[i])

       # Choose n random characters without replacement
    preference = random.sample(arr, size)

    return preference
#voters: tuple, voters_type: tuple, alternatives: tuple, voters_preferences: list,
         #default_alternative: str, remaining_rounds: int, random_selection: bool

running_times = []
input_sizes = []
for i in range (1, TOTAL_VOTERS):
    input_sizes.append(i)
    voters = tuple([x + 1 for x in range(i)])
    voters_type = [random.randint(0, 1) for k in range(i)]
    alternatives_preferences = []
    default_alternative = 'null'
    remaining_rounds = int(TOTAL_VOTERS)
    random_selection = False
    alternative_size = len(CHARS)
    alters = tuple(CHARS[:alternative_size])
    for j in range(i):
        alternatives_preferences.append(create_random_alternatives_preference(alternative_size))
    elapsed_time = measure_running_time(mdvr, voters, voters_type, alters, alternatives_preferences, default_alternative, remaining_rounds, remaining_rounds )
    running_times.append(elapsed_time)
    
print(len(input_sizes))
print(running_times)

plt.plot(input_sizes, running_times)
plt.xlabel("voters size")
plt.ylabel("Running time (seconds)")
plt.show()