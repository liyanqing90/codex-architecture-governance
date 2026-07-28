def charge(command, payment_provider, processed_commands):
    if processed_commands.contains(command.id):
        return processed_commands.result(command.id)
    result = payment_provider.charge(command.card, command.amount)
    processed_commands.record(command.id, result)
    return result
