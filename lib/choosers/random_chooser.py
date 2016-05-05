def next(grid):
    candidates = grid.loc[grid._loop_status == "candidate", :]
    if not candidates.shape[0]:
        return None
    return int(candidates.sample()["_loop_id"])
