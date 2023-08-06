from typing import Callable, ContextManager, List, Type, Dict, Iterator
from unittest.mock import Mock

from google.protobuf.json_format import MessageToDict
from grpc import insecure_channel
from grpc_health.v1.health_pb2 import HealthCheckRequest
from grpc_health.v1.health_pb2_grpc import HealthStub
from grpc_reflection.v1alpha.reflection_pb2 import ServerReflectionRequest
from grpc_reflection.v1alpha.reflection_pb2_grpc import ServerReflectionStub

from grpcalchemy import Blueprint, Context, Server, grpcmethod
from grpcalchemy.orm import Message
from tests.test_grpcalchemy import TestGrpcalchemy


class ServerTestCase(TestGrpcalchemy):
    def setUp(unittest_self):
        super().setUp()

        server_start = Mock()
        server_stop = Mock()
        app_process_request = Mock()
        app_process_response = Mock()
        blueprint_before_request = Mock()
        blueprint_after_request = Mock()
        enter_context = Mock()

        class User(Message):
            name: str

        class Post(Message):
            content: str

        class TestMessage(Message):
            user: User
            posts: List[Post]
            tag: Dict[str, Post]

        class AppService(Server):
            def before_server_start(self):
                server_start()

            def after_server_stop(self):
                server_stop()

            def process_request(
                self, request: TestMessage, context: Context
            ) -> TestMessage:
                unittest_self.assertIn(
                    request.user.name, {"unary_unary", "unary_stream"}
                )
                app_process_request()
                return request

            def process_response(
                self, response: TestMessage, context: Context
            ) -> TestMessage:
                unittest_self.assertIn(
                    response.user.name, {"unary_unary", "stream_unary"}
                )
                app_process_response()
                return response

            def app_context(
                self,
                current_service: Blueprint,
                current_method: Callable,
                context: Context,
            ) -> ContextManager:
                enter_context()
                return super().app_context(current_service, current_method, context)

            @classmethod
            def get_blueprints(cls) -> List[Type[Blueprint]]:
                return [BlueprintService]

        class BlueprintService(Blueprint):
            @grpcmethod
            def UnaryUnary(self, request: TestMessage, context: Context) -> TestMessage:
                return TestMessage(
                    user={"name": "unary_unary"},
                    posts=[dict(content=request.user.name)],
                    tag={"test": Post(content="")},
                )

            @grpcmethod
            def UnaryStream(
                self, request: TestMessage, context: Context
            ) -> Iterator[TestMessage]:
                yield TestMessage(
                    user={"name": "unary_stream"},
                    posts=[dict(content=request.user.name)],
                    tag={"test": Post(content="")},
                )

            @grpcmethod
            def StreamUnary(
                self, request: Iterator[TestMessage], context: Context
            ) -> TestMessage:
                return TestMessage(
                    user={"name": "stream_unary"},
                    posts=[dict(content=r.user.name) for r in request],
                    tag={"test": Post(content="")},
                )

            @grpcmethod
            def StreamStream(
                self, request: Iterator[TestMessage], context: Context
            ) -> Iterator[TestMessage]:
                yield TestMessage(
                    user={"name": "stream_stream"},
                    posts=[dict(content=r.user.name) for r in request],
                    tag={"test": Post(content="")},
                )

            def before_request(
                self, request: TestMessage, context: Context
            ) -> TestMessage:
                blueprint_before_request()
                unittest_self.assertIn(
                    request.user.name, {"unary_unary", "unary_stream"}
                )
                return request

            def after_request(
                self, response: TestMessage, context: Context
            ) -> TestMessage:
                blueprint_after_request()
                unittest_self.assertIn(
                    response.user.name, {"unary_unary", "stream_unary"}
                )
                return response

        unittest_self.app = AppService.run(config=unittest_self.config, block=False)
        unittest_self.assertEqual(1, server_start.call_count)
        unittest_self.server_stop = server_stop

        unittest_self.app_process_request = app_process_request
        unittest_self.app_process_response = app_process_response
        unittest_self.blueprint_after_request = blueprint_after_request
        unittest_self.blueprint_before_request = blueprint_before_request
        unittest_self.enter_context = enter_context

    def tearDown(self):
        self.app.stop(0)
        self.assertEqual(1, self.server_stop.call_count)

    def test_server(self):
        from protos.blueprintservice_pb2_grpc import BlueprintServiceStub
        from protos.testmessage_pb2 import TestMessage
        from protos.user_pb2 import User

        with insecure_channel("0.0.0.0:50051") as channel:
            response = BlueprintServiceStub(channel).UnaryUnary(
                TestMessage(user=User(name="unary_unary"))
            )
            self.assertEqual("unary_unary", response.user.name)
            self.assertEqual(1, self.app_process_request.call_count)
            self.assertEqual(1, self.app_process_response.call_count)
            self.assertEqual(1, self.blueprint_after_request.call_count)
            self.assertEqual(1, self.blueprint_before_request.call_count)

            for response in BlueprintServiceStub(channel).UnaryStream(
                TestMessage(user=User(name="unary_stream"))
            ):
                pass
            self.assertEqual("unary_stream", response.user.name)
            self.assertEqual(2, self.app_process_request.call_count)
            self.assertEqual(1, self.app_process_response.call_count)
            self.assertEqual(1, self.blueprint_after_request.call_count)
            self.assertEqual(2, self.blueprint_before_request.call_count)

            response = BlueprintServiceStub(channel).StreamUnary(
                iter([TestMessage(user=User(name="stream_unary"))])
            )
            self.assertEqual("stream_unary", response.user.name)
            self.assertEqual(2, self.app_process_request.call_count)
            self.assertEqual(2, self.app_process_response.call_count)
            self.assertEqual(2, self.blueprint_after_request.call_count)
            self.assertEqual(2, self.blueprint_before_request.call_count)

            for response in BlueprintServiceStub(channel).StreamStream(
                iter([TestMessage(user=User(name="stream_stream"))])
            ):
                pass
            self.assertEqual("stream_stream", response.user.name)
            self.assertEqual(2, self.app_process_request.call_count)
            self.assertEqual(2, self.app_process_response.call_count)
            self.assertEqual(2, self.blueprint_after_request.call_count)
            self.assertEqual(2, self.blueprint_before_request.call_count)

            self.assertEqual(1, HealthStub(channel).Check(HealthCheckRequest()).status)
            for response in ServerReflectionStub(channel).ServerReflectionInfo(
                iter([ServerReflectionRequest(list_services="")])
            ):
                self.assertEqual(
                    {
                        "service": [
                            {"name": "AppService"},
                            {"name": "BlueprintService"},
                            {"name": "grpc.health.v1.Health"},
                            {"name": "grpc.reflection.v1alpha.ServerReflection"},
                        ]
                    },
                    MessageToDict(response.list_services_response),
                )

        self.assertEqual(4, self.enter_context.call_count)
