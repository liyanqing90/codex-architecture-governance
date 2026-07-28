def run(user_query, retriever, model, payment_tool):
    retrieved = retriever.search(user_query)
    instructions = "Follow policy.\n" + retrieved
    action = model.decide(instructions, tools=[payment_tool])
    return action.execute()
