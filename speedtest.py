import timeit

# Measure the time to initialize a number
time_taken = timeit.timeit("x = 123", number=1000000)
print(f"Time taken: {time_taken/1000000} seconds per initialization")
