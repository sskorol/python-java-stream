from functools import cmp_to_key

from .iterators import IteratorUtils
from .optional import Optional


class Stream():

    """
    A sequence of elements supporting sequential operations.

    The following example illustrates an aggregate operation using
    Stream:

        result = Stream(elements)
                        .filter(lambda w: w.getColor() == RED)
                        .map(lambda w: w.getWeight())
                        .sum()

    A stream pipeline, like the "widgets" example above, can be viewed as a query on the stream source.

    A stream should be operated on (invoking an intermediate or terminal stream operation) only once. This rules out, for example, "forked" streams, where the same source feeds two or more pipelines, or multiple traversals of the same stream. A stream implementation may raise Exception if it detects that the stream is being reused.
    """

    """
    Static Methods
    """

    @staticmethod
    def empty():
        '''
        Returns an empty sequential Stream.

        :return: an empty sequential stream
        '''
        return Stream([])

    @staticmethod
    def of(elem):
        '''
        Returns a sequential Stream containing a single element.

        :param T elem: the single element
        :return: a singleton sequential stream
        '''
        return Stream([elem])

    @staticmethod
    def of(*elements):
        '''
        Returns a sequential ordered stream whose elements are the specified values.

        :param *T elements: the elements of the new stream
        :return: the new stream
        '''
        return Stream(list(elements))

    @staticmethod
    def ofNullable(elem):
        '''
        Returns a sequential Stream containing a single element, if non-null, otherwise returns an empty Stream.

        :param T elem: the single element
        :return: a stream with a single element if the specified element is non-null, otherwise an empty stream
        '''
        return Stream.of(elem) if elem is not None else Stream.empty()

    @staticmethod
    def iterate(seed, operator):
        '''
        Returns an infinite sequential ordered Stream produced by iterative application of a function f to an initial element seed, producing a Stream consisting of seed, f(seed), f(f(seed)), etc.

        :param T seed: the initial element
        :param UnaryOperator operator: a function to be applied to the previous element to produce a new element
        :return: a new sequential Stream
        '''
        return Stream(IteratorUtils.iterate(seed, operator))

    @staticmethod
    def generate(supplier):
        '''
        Returns an infinite sequential unordered stream where each element is generated by the provided Supplier. This is suitable for generating constant streams, streams of random elements, etc.

        :param Supplier supplier: the Supplier of generated elements
        :return: a new infinite sequential unordered Stream
        '''
        return Stream(IteratorUtils.generate(supplier))

    @staticmethod
    def concat(*streams):
        '''
        Creates a lazily concatenated stream whose elements are all the elements of the first stream followed by all the elements of the second stream and so on.

        :param *Stream streams: the streams to concat
        :return: the concatenation of the input streams
        '''
        return Stream(IteratorUtils.concat(*streams))

    """
    Normal Methods
    """

    def __init__(self, iterable):
        self.__iterable = iterable

    def filter(self, predicate):
        '''
        Returns a stream consisting of the elements of this stream, additionally performing the provided action on each element as elements are consumed from the resulting stream.

        :param function predicate: predicate to apply to each element to determine if it should be included
        :return: the new stream
        '''
        return Stream(IteratorUtils.filter(self.__iterable, predicate))

    def map(self, mapper):
        '''
        Returns a stream consisting of the results of applying the given function to the elements of this stream.

        :param function mapper: function to apply to each element
        :return: the new stream
        '''
        return Stream(IteratorUtils.map(self.__iterable, mapper))

    def flatMap(self, flatMapper):
        '''
        Returns a stream consisting of the results of replacing each element of this stream with the contents of a mapped stream produced by applying the provided mapping function to each element. Each mapped stream is closed after its contents have been placed into this stream. (If a mapped stream is null an empty stream is used, instead.)

        :param function flatMapper: function to apply to each element which produces a stream of new values
        :return: the new stream
        '''
        return Stream(IteratorUtils.flatMap(self.__iterable, flatMapper))

    def distinct(self):
        '''
        Returns a stream consisting of the distinct elements of this stream.

        :return: the new stream
        '''
        return Stream(IteratorUtils.distinct(self.__iterable))

    def limit(self, count):
        '''
        Returns a stream consisting of the elements of this stream, truncated to be no longer than maxSize in length.

        :param int count:  the number of elements the stream should be limited to
        :return: the new stream
        '''
        return Stream(IteratorUtils.limit(self.__iterable, count))

    def skip(self, count):
        '''
        Returns a stream consisting of the remaining elements of this stream after discarding the first n elements of the stream. If this stream contains fewer than n elements then an empty stream will be returned.

        :param int count:  the number of leading elements to skip
        :return: the new stream
        '''
        return Stream(IteratorUtils.skip(self.__iterable, count))

    def takeWhile(self, predicate):
        '''
        Returns a stream consisting of the longest prefix of elements taken from this stream that match the given predicate.

        :param Predicate predicate:  predicate to apply to elements to determine the longest prefix of elements.
        :return: the new stream
        '''
        return Stream(IteratorUtils.takeWhile(self.__iterable, predicate))

    def dropWhile(self, predicate):
        '''
        Returns a stream consisting of the remaining elements of this stream after dropping the longest prefix of elements that match the given predicate.

        :param Predicate predicate:  predicate to apply to elements to determine the longest prefix of elements.
        :return: the new stream
        '''
        return Stream(IteratorUtils.dropWhile(self.__iterable, predicate))

    """
    From here this method mustn't be called on infinite stream
    """

    def sorted(self, comparator=None):
        '''
        Returns a stream consisting of the elements of this stream, sorted according to the provided Comparator.

        :param Comparator comparator: Comparator to be used to compare stream elements - if null default comparator is used
        :return: the new stream
        '''
        return Stream(sorted(
            self.__iterable, key=cmp_to_key(comparator))) if comparator is not None else Stream(sorted(
                self.__iterable))

    def peek(self, consumer):
        '''
        Returns a stream consisting of the elements of this stream, additionally performing the provided action on each element as elements are consumed from the resulting stream.

        :param Consumer consumer: action to perform on the elements as they are consumed from the stream
        :return: the new stream
        '''
        return Stream(IteratorUtils.peek(self.__iterable, consumer))

    def forEach(self, function):
        '''
        Performs an action for each element of this stream.

        :param Function function: action to perform on the elements
        :return: None
        '''
        for elem in self.__iterable:
            function(elem)

    def anyMatch(self, predicate):
        '''
        Returns whether any elements of this stream match the provided predicate.

        :param Predicate predicate: predicate to apply to elements of this stream
        :return: True if any elements of the stream match the provided predicate, otherwise False
        '''
        return any([predicate(elem) for elem in self.__iterable])

    def allMatch(self, predicate):
        '''
        Returns whether all elements of this stream match the provided predicate.

        :param Predicate predicate: predicate to apply to elements of this stream
        :return: True if either all elements of the stream match the provided predicate or the stream is empty, otherwise False
        '''
        return all([predicate(elem) for elem in self.__iterable])

    def noneMatch(self, predicate):
        '''
        Returns whether no elements of this stream match the provided predicate.

        :param Predicate predicate: predicate to apply to elements of this stream
        :return: True if either no elements of the stream match the provided predicate or the stream is empty, otherwise False
        '''
        return len(self.__iterable) == 0 or not self.anyMatch(predicate)

    def findFirst(self):
        '''
        Returns an Optional describing the first element of this stream, or an empty Optional if the stream is empty. If the stream has no encounter order, then any element may be returned.

        :return: an Optional describing the first element of this stream, or an empty Optional if the stream is empty
        '''
        for elem in self.__iterable:
            return Optional.of(elem)
        return Optional.ofNullable(None)

    def findAny(self):
        '''
        Returns an Optional describing some element of the stream, or an empty Optional if the stream is empty.

        :return: an Optional describing some element of this stream, or an empty Optional if the stream is empty
        '''
        return self.findFirst()

    def reduce(self, accumulator, identity=None):
        '''
        Performs a reduction on the elements of this stream, using the provided identity value and an associative accumulation function, and returns the reduced value.

        :param T identity: the identity value for the accumulating function - if not specified it will be the first element of the stream
        :param Accumulator accumulator: function for combining two values
        :return: the result of reduction
        '''
        result = identity
        for elem in self.__iterable:
            if(result is None):
                result = elem
            else:
                result = accumulator(result, elem)
        return Optional.ofNullable(result)

    def min(self, comparator=None):
        '''
        Returns the minimum element of this stream according to the provided Comparator. This is a special case of a reduction.

        :param Comparator comparator: Comparator to compare elements of this stream - if null default comparator is used
        :return: an Optional describing the minimum element of this stream, or an empty Optional if the stream is empty
        '''
        return Optional.ofNullable(min(self.__iterable, key=cmp_to_key(comparator))) if comparator is not None else Optional.ofNullable(min(self.__iterable))

    def max(self, comparator=None):
        '''
        Returns the maximum element of this stream according to the provided Comparator. This is a special case of a reduction.

        :param Comparator comparator: Comparator to compare elements of this stream - if null default comparator is used
        :return: an Optional describing the maximum element of this stream, or an empty Optional if the stream is empty
        '''
        return Optional.ofNullable(max(self.__iterable, key=cmp_to_key(comparator))) if comparator is not None else Optional.ofNullable(max(self.__iterable))

    def sum(self):
        '''
        Returns the sum of all elements of this stream. This is a special case of a reduction.

        :return: an Optional describing the sum of all the elements of this stream, or an empty Optional if the stream is empty
        '''
        return self.reduce(lambda x, y: x + y)

    def count(self):
        '''
        Returns the count of elements in this stream. This is a special case of a reduction.

        :return: the count of elements in this stream
        '''
        count = 0
        for elem in self.__iterable:
            count += 1

        return count

    def toList(self):
        '''
        Returns a list with the elements in this stream.

        :return: the list of elements in this stream
        '''
        return list(self.__iterable)

    def toSet(self):
        '''
        Returns a set with the elements in this stream.

        :return: the set of elements in this stream
        '''
        return set(self.__iterable)

    def __iter__(self):
        '''
        Returns an iterator over the elements in this stream.

        :return: the iterator over the elements in this stream
        '''
        return iter(self.__iterable)

    def __eq__(self, value):
        '''
        Check if this stream is equal to the specified stream

        :return: True if the streams match, False otherwise
        '''
        return self.__iterable == value.__iterable
