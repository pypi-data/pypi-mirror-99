from abc import abstractmethod


class AddressTestDescriptor:
    # pylint: disable=too-few-public-methods

    def __init__(self, address_class, encoded_address, decoded_address):
        self.address_class = address_class
        self.encoded_address = encoded_address
        self.decoded_address = decoded_address


class BasicAddressTest:
    # pylint: disable=no-member

    def test_can_create_from_encoded_address(self):
        # Arrange:
        test_descriptor = self.get_test_descriptor()

        # Act:
        address = test_descriptor.address_class(test_descriptor.encoded_address)

        # Assert:
        self.assertEqual(test_descriptor.decoded_address, address.bytes)
        self.assertEqual(test_descriptor.encoded_address, str(address))

    def test_can_create_from_decoded_address(self):
        # Arrange:
        test_descriptor = self.get_test_descriptor()

        # Act:
        address = test_descriptor.address_class(test_descriptor.decoded_address)

        # Assert:
        self.assertEqual(test_descriptor.decoded_address, address.bytes)
        self.assertEqual(test_descriptor.encoded_address, str(address))

    @abstractmethod
    def get_test_descriptor(self):
        pass
