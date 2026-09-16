from astra.logic.adder import ripple_carry_adder

class Incrementer4Bit:
    """
    A combinational 4-bit incrementer.

    Adds 1 to a 4-bit input using the existing 4-bit ripple-carry
    adder. The result is limited to 4 bits, so values wrap around
    from 1111 to 0000.
    """

    def increment(
        self,
        value: tuple[int, int, int, int]
    ) -> tuple[int, int, int, int]:
        """
        Increment a 4-bit value by 1.

        Args:
            value: A 4-bit tuple representing the input value.

        Returns:
            A 4-bit tuple representing value + 1.

        Example:
            0111 -> 1000
            1111 -> 0000
        """
        result, _ = ripple_carry_adder(
            value,
            (0, 0, 0, 1)
        )

        return result