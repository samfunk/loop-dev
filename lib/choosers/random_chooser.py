def next(grid, candidates, pending, complete, completed_values, minimize):
    random_row = int(npr.randint(candidates.shape[0], size=1))
    return (random_row, grid)
