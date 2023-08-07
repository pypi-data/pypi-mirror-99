import pytest

from unittest import mock

from click.testing import CliRunner

from midiroute.cli import list_ports, run


@pytest.fixture
def stream_mock():
    with mock.patch("midiroute.midiutils.stream", new_callable=mock.AsyncMock) as s:
        yield s


@pytest.fixture
def io_names_mock():
    with mock.patch("midiroute.midiutils.list_input_port_names") as i:
        with mock.patch("midiroute.midiutils.list_output_port_names") as o:
            yield i, o


class TestRun:
    def test_starts_stream_with_given_ports(self, stream_mock):
        input_port = "input"
        output_ports = "out1,out2"

        CliRunner().invoke(run, ["-i", input_port, "-o", output_ports])

        stream_mock.assert_called_once_with(
            input_port, output_ports.split(","), *stream_mock.call_args.args[2:]
        )

    def test_starts_stream_with_monitoring(self, stream_mock):
        input_port = "input"
        output_ports = "out1,out2"

        res = CliRunner().invoke(run, ["-i", input_port, "-o", output_ports, "-m"])

        assert res.exit_code == 0
        stream_mock.assert_called_once_with(*stream_mock.call_args.args[:2], True)


class TestListPorts:
    def test_lists_input_and_output_ports(self, io_names_mock):
        i, o = io_names_mock
        i.return_value = ["input"]
        o.return_value = ["out1", "out2"]

        res = CliRunner().invoke(list_ports)

        assert res.exit_code == 0
        assert all(v in res.output for v in o.return_value)
        assert all(v in res.output for v in i.return_value)
