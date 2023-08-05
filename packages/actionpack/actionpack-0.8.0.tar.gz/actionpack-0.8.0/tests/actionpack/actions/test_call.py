import pickle

from actionpack.actions import Call
from actionpack.utils import Closure
from actionpack.utils import pickleable

from oslash import Right
from unittest import TestCase


class CallTest(TestCase):

    @classmethod
    def function(*args, **kwargs):
        return args[1:], kwargs

    def setUp(self):
        self.arg = 'arg'
        self.kwarg = 'kwarg'
        self.closure = Closure(self.function, self.arg, kwarg=self.kwarg)
        self.action = Call(closure=self.closure)

    def test_can_Call(self):
        result = self.action.perform()
        self.assertIsInstance(result, Right)
        self.assertEqual(result.value, ((self.arg,), {self.kwarg: self.kwarg}))

    def test_can_pickle(self):
        pickled = pickleable(self.action)
        unpickled = pickle.loads(pickled)

        self.assertTrue(pickleable(self.action))
        self.assertEqual(unpickled.__dict__, self.action.__dict__)

