from abstractions.knapclasses import KnapSack


def _initialize():
    global _knapsack
    _knapsack = KnapSack()


try:
    knapsack = _knapsack
except NameError:
    _initialize()
    knapsack = _knapsack
