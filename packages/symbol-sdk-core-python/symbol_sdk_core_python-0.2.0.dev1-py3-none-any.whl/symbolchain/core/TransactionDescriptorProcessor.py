class TransactionDescriptorProcessor:
    """Processes and looks up transaction descriptor properties."""

    def __init__(self, transaction_descriptor, type_parsing_rules):
        """Creates a transaction descriptor processor."""
        self.transaction_descriptor = transaction_descriptor
        self.type_parsing_rules = type_parsing_rules or {}
        self.type_hints = {}

    def lookup_value(self, key):
        """Looks up the value for key."""
        if key not in self.transaction_descriptor:
            raise ValueError('transaction descriptor does not have attribute {}'.format(key))

        value = self.transaction_descriptor[key]

        type_hint = self.type_hints.get(key)
        if type_hint in self.type_parsing_rules:
            value = self.type_parsing_rules[type_hint](value)

        return value

    def copy_to(self, transaction, ignore_keys=None):
        """Copies all descriptor information to a transaction."""
        for key in self.transaction_descriptor.keys():
            if ignore_keys and key in ignore_keys:
                continue

            if not hasattr(transaction, key):
                raise ValueError('transaction does not have attribute {}'.format(key))

            value = self.lookup_value(key)
            if not isinstance(value, str) and not isinstance(value, bytes) and hasattr(value, '__iter__'):
                for item in value:
                    getattr(transaction, key).append(item)
            else:
                setattr(transaction, key, value)

    def set_type_hints(self, type_hints):
        """Sets type hints."""
        self.type_hints = type_hints or {}
