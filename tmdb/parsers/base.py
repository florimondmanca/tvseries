"""Definition of base parser classes.

Parsers allow to ingest objects returned by the TMDB API.
"""

from typing import Type, Generic, TypeVar

T = TypeVar('T')


class Parser(Generic[T]):
    """Abstract parser base class.

    Parsers transform TMDB's API representation of an object to our
    internal representation of that object (defined by the object_class).
    """

    object_class: Type[T]

    def get_kwargs(self, data: dict) -> dict:
        """Return the keyword arguments used to build the object.

        Must be implemented by subclasses.

        :param data: dict
            Dictionary containing raw API data about the object.
        :return kwargs: dict
            A dictionary containing arguments that will be used to build
            the object.
        """
        raise NotImplementedError

    def parse(self, data: dict) -> T:
        """Build and return a new object from the raw TMDB API data dict.

        :param data: dict
            Dictionary containing raw API data about the object.
        :return obj: T
        """
        kwargs = self.get_kwargs(data)
        return self.object_class(**kwargs)


class ParserGroup(Generic[T]):
    """Utility for grouping parsers of a same object class."""

    list_parser_class: Type[Parser[T]]
    detail_parser_class: Type[Parser[T]]

    def for_list(self, data) -> T:
        return self.list_parser_class().parse(data)

    def for_detail(self, data) -> T:
        return self.detail_parser_class().parse(data)
