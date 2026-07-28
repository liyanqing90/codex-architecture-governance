def answer(question, agent, documentation_search, repository_search):
    return agent.run(
        question,
        tools=[documentation_search, repository_search],
        require_citations=True,
    )
