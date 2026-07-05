from src.parser import parse_candump_line


def test_parse_standard_candump_line():
    frame = parse_candump_line("(1719672101.123456) can0 123#DEADBEEF")

    assert frame.timestamp == 1719672101.123456
    assert frame.interface == "can0"
    assert frame.can_id == 0x123
    assert frame.data == bytes.fromhex("DEADBEEF")
    assert frame.dlc == 4
