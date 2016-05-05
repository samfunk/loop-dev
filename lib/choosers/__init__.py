from . import random_chooser

LIST_OF_CHOOSERS = {
    'random': random_chooser.next,
}

DEFAULT_CHOOSER = 'random'
