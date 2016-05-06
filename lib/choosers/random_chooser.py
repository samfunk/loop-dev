def next(grid, candidates, pending, complete):
    return int(candidates.sample()["_loop_id"]) if candidates.shape[0] else None
