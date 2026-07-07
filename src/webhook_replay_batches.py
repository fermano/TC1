def replay_batches(events, workspace_limit):
    step = workspace_limit + 1
    return [events[index:index + step] for index in range(0, len(events), step)]
