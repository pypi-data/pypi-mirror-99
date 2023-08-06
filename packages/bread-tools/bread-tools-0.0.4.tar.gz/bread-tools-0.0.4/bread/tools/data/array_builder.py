import random
import numpy as np


class ArrayBuilder(object):
    """
    Array generation tool.
    """

    @staticmethod
    def gen_new_array(from_array):
        """
        Generate a new array when there is a value greater than 1 or less than -1.
        :param from_array: An array containing elements greater than 1 or less than -1.
        :return: Return an array between -1 and 1.
        """
        if isinstance(from_array, list) or isinstance(from_array, np.ndarray):
            total = np.sum(from_array)
            m = 10000
            numbers = np.random.randn(len(from_array))
            max_value = max(np.max(numbers), abs(np.min(numbers)))
            numbers = numbers / (max_value + 0.0001)
            summation = sum(numbers)
            k = m / summation
            new_array = [i * k / (1 / total * m) for i in numbers]
            if abs(np.max(new_array)) >= 1.0 or abs(np.min(new_array)) >= 1.0:
                new_array = ArrayBuilder.gen_new_array([x / -2 for x in new_array])
            return new_array
        else:
            return None

    @staticmethod
    def random_array(size, must_over_zero=False):
        """
        Random an initial array.
        :param size: array size.
        :param must_over_zero: must number over zero.
        :return: Return an array between -1 and 1.
        """
        if isinstance(size, int) and size > 0:
            if must_over_zero:
                return [random.uniform(0.0, 0.999) for _ in range(size)]
            return [random.uniform(-0.999, 0.999) for _ in range(size)]
        return None
