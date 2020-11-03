from socket import socket

import pytest
from mock import Mock, PropertyMock, patch

from microBrew.brew_repository import BrewInfo, BrewRepository
from microBrew.decision_module import DecisionModule, TargetState
from microBrew.device_manager import DeviceManager
from microBrew.server import Server
from microBrew.temp_logger import TempLogger


@pytest.fixture
def device_manager():
    return Mock(spec=DeviceManager)


@pytest.fixture
def brew_repository():
    return Mock(spec=BrewRepository)


@pytest.fixture
def temp_logger():
    return Mock(spec=TempLogger)


@pytest.fixture
def decision_module():
    return Mock(spec=DecisionModule)


@pytest.fixture
def server_received_message():
    return b"00:00:00:00:00:00\x00 @\x00\x00\xb9A\x00\x80\xa1A\x00\x00\n\n"


@pytest.fixture
def server_sent_message_unassigned_device():
    return b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"


@pytest.fixture
def server_sent_message_heater_on():
    return b"\x00\x00 A\x00\x00\xa0A\x01\x00"


@pytest.fixture
def server_sent_message_cooler_on():
    return b"\x00\x00 A\x00\x00\xa0A\x00\x01"


@pytest.fixture
def mock_client_socket(server_received_message):
    mock_sock = Mock(spec=socket)
    mock_sock.recv.return_value = server_received_message
    return mock_sock


@pytest.fixture
def server(device_manager, brew_repository, temp_logger, decision_module):
    server = Server(device_manager, brew_repository, temp_logger, decision_module)
    return server


@patch("microBrew.server.socket")
def test_server_send_message_to_new_device(
    mock_socket,
    mock_client_socket,
    server,
    device_manager,
    brew_repository,
    server_sent_message_unassigned_device,
):
    mock_socket().accept.return_value = (mock_client_socket, ("ip", "port"))

    device_manager.update_status.return_value = True

    with patch.object(server, "is_running", new_callable=PropertyMock) as run_flag:
        run_flag.side_effect = [True, False]
        server.start()

    mock_client_socket.sendall.assert_called_with(server_sent_message_unassigned_device)


@patch("microBrew.server.socket")
def test_server_send_message_to_unassigned_device(
    mock_socket,
    mock_client_socket,
    server,
    device_manager,
    brew_repository,
    server_sent_message_unassigned_device,
):
    mock_socket().accept.return_value = (mock_client_socket, ("ip", "port"))

    device_manager.update_status.return_value = None
    brew_repository.get_device_active_brew.return_value = None

    with patch.object(server, "is_running") as run_flag:
        run_flag.side_effect = [True, False]
        server.start()

    mock_client_socket.sendall.assert_called_with(server_sent_message_unassigned_device)


@patch("microBrew.server.socket")
def test_server_send_message_heater_on(
    mock_socket,
    mock_client_socket,
    server,
    device_manager,
    brew_repository,
    decision_module,
    server_sent_message_heater_on,
):
    mock_socket().accept.return_value = (mock_client_socket, ("ip", "port"))

    device_manager.update_status.return_value = None
    brew_repository.get_device_active_brew.return_value = BrewInfo(
        None, True, 10, 20, None
    )
    decision_module.get_target_state.return_value = TargetState(
        heater_state=True, cooler_state=False
    )

    with patch.object(server, "is_running") as run_flag:
        run_flag.side_effect = [True, False]
        server.start()

    mock_client_socket.sendall.assert_called_with(server_sent_message_heater_on)


@patch("microBrew.server.socket")
def test_server_send_message_cooler_on(
    mock_socket,
    mock_client_socket,
    server,
    device_manager,
    brew_repository,
    decision_module,
    server_sent_message_cooler_on,
):
    mock_socket().accept.return_value = (mock_client_socket, ("ip", "port"))

    device_manager.update_status.return_value = None
    brew_repository.get_device_active_brew.return_value = BrewInfo(
        None, True, 10, 20, None
    )
    decision_module.get_target_state.return_value = TargetState(
        heater_state=False, cooler_state=True
    )

    with patch.object(server, "is_running") as run_flag:
        run_flag.side_effect = [True, False]
        server.start()

    mock_client_socket.sendall.assert_called_with(server_sent_message_cooler_on)
