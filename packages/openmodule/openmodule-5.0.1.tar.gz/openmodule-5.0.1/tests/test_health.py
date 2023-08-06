from unittest import TestCase

from openmodule.core import OpenModuleCore
from openmodule.health import health_ok, health_error
from openmodule_test.health import HealthTestMixin


class HealthTestCase(HealthTestMixin, TestCase):
    topics = ["healthz"]

    def setUp(self):
        super().setUp()
        self.core = OpenModuleCore(self.zmq_context(), self.zmq_config())
        self.core.start()
        self.wait_for_health()

    def tearDown(self):
        super().tearDown()
        self.core.join()

    def test_health_ok(self):
        self.core.health.health_handler = lambda: health_ok({"some": "meta"})
        health = self.get_health()
        self.assertHealthOk(health)

    def test_health_error(self):
        self.core.health.health_handler = lambda: health_error("some error message")
        health = self.get_health()
        self.assertHealthError(health)

    def test_health_handler_error(self):
        self.core.health.health_handler = lambda: 1 / 0
        health = self.get_health()
        self.assertHealthError(health)
        self.assertIn("health routine", str(health))

    def test_health_handler_invalid_return_type(self):
        self.core.health.health_handler = lambda: None
        health = self.get_health()
        self.assertHealthError(health)
        self.assertIn("health routine", str(health))
