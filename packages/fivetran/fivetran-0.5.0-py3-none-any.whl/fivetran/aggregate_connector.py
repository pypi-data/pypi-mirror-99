class AggregateConnector:
    def __init__(self, state: dict, connectors: dict):
        self._state = state
        self._connectors = connectors

    @property
    def state(self) -> dict:
        state = {}
        for connector_id, connector_obj in self._connectors.items():
            state[connector_id] = connector_obj.state
        return state

    @property
    def insert(self) -> dict:
        insert_dict = {}
        for connector in self._connectors.values():
            connector_insert = connector.insert
            for table, records in connector_insert.items():
                if table in insert_dict:
                    insert_dict[table].extend(records)
                else:
                    insert_dict[table] = []
                    insert_dict[table].extend(records)
        return insert_dict

    @property
    def delete(self) -> dict:
        delete_dict = {}
        for connector in self._connectors.values():
            connector_delete = connector.delete
            for table, records in connector_delete.items():
                if table in delete_dict:
                    delete_dict[table].extend(records)
                else:
                    delete_dict[table] = []
                    delete_dict[table].extend(records)
        return delete_dict

    @property
    def schema(self) -> dict:
        schema_dict = {}
        for connector in self._connectors.values():
            connector_schema = connector.schema
            for table, schema in connector_schema.items():
                if table not in schema_dict:
                    schema_dict[table] = schema
        return schema_dict

    @property
    def has_more(self) -> bool:
        for connector in self._connectors.values():
            if connector.has_more:
                return True
        return False

    @property
    def response(self) -> dict:
        return {
            "state": self.state,
            "insert": self.insert,
            "delete": self.delete,
            "schema": self.schema,
            "hasMore": self.has_more,
        }

    def get_records(self) -> None:
        if self.has_more():
            for connector in self._connectors.values():
                connector.get_records()

    def reset_state(self) -> None:
        for connector in self._connectors.values():
            connector.reset_state()
