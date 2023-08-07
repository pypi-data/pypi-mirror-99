"""Tests for MIDI utils."""

import asyncio

from unittest import mock

import pytest

from midiroute import midiutils


@pytest.fixture
def mock_get_input_port_names():
    with mock.patch("midiroute.midiutils.mido.get_input_names") as m:
        yield m


@pytest.fixture
def mock_get_output_port_names():
    with mock.patch("midiroute.midiutils.mido.get_output_names") as m:
        yield m


@pytest.fixture
def mock_open_input():
    with mock.patch("midiroute.midiutils.mido.open_input") as m:
        yield m


@pytest.fixture
def mock_open_output():
    with mock.patch("midiroute.midiutils.mido.open_output") as m:
        yield m


@pytest.fixture
def mock_input_port(mock_open_input, mock_get_input_port_names):
    with mock.patch("midiroute.midiutils.mido.ports.BaseInput") as port:
        p = port()
        p.name = "testinput"
        mock_get_input_port_names.return_value = [p.name]
        mock_open_input.return_value = p
        yield p


@pytest.fixture
def mock_output_port(mock_open_output, mock_get_output_port_names):
    with mock.patch("midiroute.midiutils.mido.ports.BaseOutput") as port:
        p = port()
        p.name = "testoutput"
        p.closed = mock.PropertyMock(side_effect=(False, True))
        mock_get_output_port_names.return_value = [p.name]
        mock_open_output.return_value.__enter__.return_value = p
        yield p


pytestmark = pytest.mark.asyncio


class TestInputStream:
    @pytest.mark.parametrize("port_name", ("p", "alpha", "beta", "g", "gamma", "delta"))
    async def test_raises_on_invalid_port_name(
        self, mock_input_port, port_name
    ) -> None:
        with pytest.raises(midiutils.InvalidPortName):
            async with midiutils.input_port_stream(port_name, []):
                pass

    async def test_yields_input_port_with_name(self, mock_input_port) -> None:
        async with midiutils.input_port_stream(mock_input_port.name, []) as ins:
            assert ins.name == mock_input_port.name

    async def test_closes_port_when_scope_ends(self, mock_input_port) -> None:
        async with midiutils.input_port_stream(mock_input_port.name, []):
            pass

        mock_input_port.close.assert_called_once()


class TestOutputStream:
    @pytest.mark.parametrize("port_name", ("p", "g", "gamma" "delta"))
    async def test_raises_on_invalid_port_name(
        self, mock_output_port, port_name
    ) -> None:
        with pytest.raises(midiutils.InvalidPortName):
            await midiutils.output_port_stream(port_name, asyncio.Queue())

    async def test_opens_output_port_with_name(
        self, mock_output_port, mock_open_output
    ) -> None:
        port = mock_output_port

        await midiutils.output_port_stream(port.name, asyncio.Queue())

        mock_open_output.assert_called_once_with(port.name)


class TestListPortNames:
    def test_sorts_input_port_names(self, mock_get_input_port_names):
        port_names = ["zeta", "gamma", "beta"]
        mock_get_input_port_names.return_value = port_names

        assert midiutils.list_input_port_names() == sorted(port_names)

    def test_sorts_output_port_names(self, mock_get_output_port_names):
        port_names = ["zeta", "gamma", "beta"]
        mock_get_output_port_names.return_value = port_names

        assert midiutils.list_output_port_names() == sorted(port_names)
