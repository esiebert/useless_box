from abc import ABC, abstractmethod


class Processor(ABC):
    @abstractmethod
    def process(body):
        pass

class SumNumbers(Processor):
    def process(self, body):
        return sum([int(val) for val in str(body) if val.isnumeric()])
