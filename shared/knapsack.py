from abstractions.knapclasses import KnapSack


# Initializing global variables
def _initialize():
    global _knapsack
    _knapsack = KnapSack()


try:
    knapsack = _knapsack
except NameError:
    _initialize()
    knapsack = _knapsack
