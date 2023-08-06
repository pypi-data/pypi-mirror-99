import os.path
import socket
import unittest
from shutil import rmtree

from grpcalchemy.utils import (
    socket_bind_test,
    select_address_family,
    get_sockaddr,
    generate_proto_file,
)
from tests.test_grpcalchemy import TestGrpcalchemy


class UtilsTestCase(TestGrpcalchemy):
    def test_socket_bind_test_INET(self):
        host = "0.0.0.0"
        address_family = select_address_family(host)
        with socket.socket(address_family, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            port = s.getsockname()[1]
            with self.subTest(f"host: {host}"):
                with socket.socket(address_family, socket.SOCK_STREAM) as s:
                    with self.assertRaises(OSError):
                        socket_bind_test(host, port)

    def test_socket_bind_test_INET6(self):
        host = "::"
        address_family = select_address_family(host)
        with socket.socket(address_family, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            port = s.getsockname()[1]
            with self.assertRaises(OSError):
                socket_bind_test(host, port)

    def test_socket_bind_test_UNIX(self):
        host = "unix://test"
        address_family = select_address_family(host)
        with socket.socket(address_family, socket.SOCK_STREAM) as s:
            s.bind("test")
            port = s.getsockname()[1]
            server_address = get_sockaddr(host, port, address_family)
            with self.assertRaises(OSError):
                socket_bind_test(host, port)
            if os.path.exists(server_address):
                os.remove(server_address)

    def test_generate_proto_file(self):
        from grpcalchemy.orm import Message

        class TestNestedPackage(Message):
            test: str

        dir_name = "protos/v1"
        if os.path.exists(dir_name):
            rmtree("protos")
        generate_proto_file(template_path=dir_name)
        self.assertTrue(os.path.exists(dir_name))
        self.assertTrue(os.path.exists(os.path.join(dir_name, "__init__.py")))
        self.assertTrue(os.path.exists(os.path.join(dir_name, "README.md")))
        rmtree("protos")


if __name__ == "__main__":
    unittest.main()
