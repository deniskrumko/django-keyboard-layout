from functools import reduce


__all__ = ('DefaultLayout', 'EnglishRussianLayout')


class BaseLayout(object):
    """Base class for keyboard layout."""

    layout = None

    @classmethod
    def create(cls, source_low, source_up, dest_low, dest_up):
        """Method to create `layout_dict`.

        Method creates one dictionary that is used to process each character in
        search term to transform it to different layout.

        """
        source_dict = {}
        source = source_low + source_up

        dest_dict = {}
        dest = dest_low + dest_up

        for index, char in enumerate(source):
            source_dict[char] = dest[index]

        for index, char in enumerate(dest):
            dest_dict[char] = source[index]

        return {
            'source_dict': source_dict,
            'source_set': set(source),
            'dest_dict': dest_dict,
            'dest_set': set(dest),
        }

    @classmethod
    def convert_term(cls, term):
        """Method to convert search term to current layout."""
        if not cls.layout:
            return term

        layout_dict = cls.detect_layout_dict(term)

        return reduce(lambda a, b: a + layout_dict.get(b, b), term, '')

    @classmethod
    def detect_layout_dict(cls, term):
        """Method to detect required layout (source or destination).

        Method searches for larger intersections between set of term chars
        and sets of source and destination layouts. Larger intersection
        defines used layout.

        """
        source_len = len(set(term) & cls.layout['source_set'])
        dest_len = len(set(term) & cls.layout['dest_set'])
        name = 'source_dict' if source_len > dest_len else 'dest_dict'
        return cls.layout[name]


class DefaultLayout(BaseLayout):
    """Default layout that is used to not transform search term."""

    @classmethod
    def convert_term(cls, term):
        """Default layout doesn't convert search terms."""
        return term


class EnglishRussianLayout(BaseLayout):
    """English - Russian keyboard layout."""

    layout = BaseLayout.create(
        "qwertyuiop[]asdfghjkl;'zxcvbnm,./`",
        "QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?~",
        "йцукенгшщзхъфывапролджэячсмитьбю.ё",
        "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё"
    )
