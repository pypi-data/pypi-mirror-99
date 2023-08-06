
class Contract:
    """ Represents a contract between two agents """

    def __init__(self, sender_id: int, receiver_id: int, product_name: str, delivery_interval_in_steps: int, first_delivery_time: int):
        assert product_name != ""
        if sender_id == receiver_id:
            raise ValueError(
                "sender and receiver can't have the same id {}".format(sender_id))
        self._sender_id = sender_id
        self._receiver_id = receiver_id
        self._product_name = product_name
        self._delivery_interval_in_steps = delivery_interval_in_steps
        self._first_delivery_time = first_delivery_time

    @property
    def product_name(self) -> str:
        return self._product_name

    @property
    def sender_id(self) -> int:
        return self._sender_id

    @property
    def sender_id_str(self) -> str:
        return "#{}".format(self._sender_id)

    @property
    def receiver_id(self) -> int:
        return self._receiver_id

    @property
    def receiver_id_str(self) -> str:
        return "#{}".format(self._receiver_id)

    @property
    def delivery_interval_in_steps(self) -> int:
        return self._delivery_interval_in_steps

    @property
    def first_delivery_time(self) -> int:
        return self._first_delivery_time
