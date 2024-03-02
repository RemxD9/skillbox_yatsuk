# Errors Found and Fixed in Person Class

1. In the `set_name` method, corrected the assignment of the name: `self.name = name` instead of `self.name = self.name`.

2. In the `set_address` method, corrected the assignment of the address: `self.address = address` instead of `self.address == address`.

3. In the `is_homeless` method, corrected the check for homelessness: `self.address == ''` instead of `address is None`.

