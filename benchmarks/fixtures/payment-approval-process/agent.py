pending = {}


def request_payment(task_id, model, approver, payment_tool):
    proposal = model.propose_payment()
    pending[task_id] = proposal
    if approver.wait_for_approval(task_id):
        final_parameters = model.propose_payment()
        return payment_tool.charge(**final_parameters)
