from setuptools import setup


setup(
    name='django-keyboard-layout',
    packages=['django_keyboard_layout'],
    version='0.0.3',
    description="Keyboard layout-insensitive search filter",
    long_description=(
        "Keyboard layout-insensitive search filter for Django Rest Framework"
    ),
    author="Denis Krumko",
    author_email="dkrumko@gmail.com",
    url="https://github.com/deniskrumko/django-keyboard-layout",
    license="MIT",
    zip_safe=False,
    platforms=["any"],
    keywords=['django', 'django-rest-framework', 'layout', 'keyboard'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python",
    ],
    requires=['django']
)
