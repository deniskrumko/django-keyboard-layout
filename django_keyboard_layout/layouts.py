from functools import reduce


__all__ = ('DefaultLayout', 'EnglishRussianLayout')


class BaseLayout(object):
    """Base class for keyboard layout."""

    layout_dict = None

    @classmethod
    def create(cls, source_low, source_up, dest_low, dest_up):
        """Method to create `layout_dict`.

        Method creates one dictionary that is used to process each character in
        search term to transform it to different layout.

        """
        result_dict = {}
        source = source_low + source_up
        dest = dest_low + dest_up

        for index, char in enumerate(source):
            result_dict[char] = dest[index]

        for index, char in enumerate(dest):
            result_dict[char] = source[index]

        return result_dict

    @classmethod
    def convert_term(cls, term):
        """Method to convert search term to current layout."""
        if not cls.layout_dict:
            return term

        return reduce(lambda a, b: a + cls.layout_dict.get(b, b), term, '')


class DefaultLayout(BaseLayout):
    """Default layout that is used to not transform search term."""

    @classmethod
    def convert_term(cls, term):
        """Default layout doesn't convert search terms."""
        return term


class EnglishRussianLayout(BaseLayout):
    """English - Russian keyboard layout."""
    english_lowercase = "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
    english_uppercase = "QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?~"
    russian_lowercase = "йцукенгшщзхъфывапролджэячсмитьбю.ё"
    russian_uppercase = "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё"

    layout_dict = BaseLayout.create(
        source_low=english_lowercase,
        source_up=english_uppercase,
        dest_low=russian_lowercase,
        dest_up=russian_uppercase
    )
