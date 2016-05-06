from . import random_chooser
from . import random_forest_regressor

LIST_OF_CHOOSERS = {
    'random': random_chooser.next,
    'random_forest_regressor': random_forest_regressor.next
}

DEFAULT_CHOOSER = 'random_forest_regressor'
