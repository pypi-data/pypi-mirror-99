from logging import LogRecord


def get_data_record(record: LogRecord) -> tuple:
    order_action = getattr(record, 'order_action', {})
    order_id = order_action.get('order_id')
    action_id = order_action.get('action_id')
    graph_id = order_action.get('graph_id')
    node = getattr(record, 'node', None)
    action_type = getattr(record, 'action_type', None)
    orchestrator_id = getattr(record, 'orchestrator_id', None)
    return order_id, action_id, graph_id, node, action_type, orchestrator_id
