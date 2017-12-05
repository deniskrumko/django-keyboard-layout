# django-keyboard-layout

**Keyboard layout-insensitive search filter for Django Rest Framework.**

## Installation

```bash
pip install -e git+https://github.com/deniskrumko/django-keyboard-layout@v0.0.2#egg=django-keyboard-layout
```

## Example

#### Define `filter_backends`, `search_fields` and `search_layouts` in `APIView`

```python
from django_keyboard_layout import filters, layouts

class ExampleListView(APIView):
    queryset = Example.objects.all()
    serializer_class = ExampleSerializer

    filter_backends = (filters.LayoutSearchFilter,)
    search_fields = ('name',)
    search_layouts = (layouts.EnglishRussianLayout,)
```

#### Check that search term is layout-insensitive

```bash
GET localhost:8000/api/example/?search=Example

# is equal to

GET localhost:8000/api/example/?search=Учфьзду
```

```bash
GET localhost:8000/api/example/?search=Пример

# is equal to

GET localhost:8000/api/example/?search=Ghbvth
```

## Available layouts

* English - Russian
