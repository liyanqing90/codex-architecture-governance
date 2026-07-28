def process(job, store, renderer) -> None:
    if store.has_result(job.id):
        return
    result = renderer.render(job.payload)
    store.commit_result_once(job.id, result)
