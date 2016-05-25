from . import random_chooser
from . import random_forest_regressor
from . import gp_ei_mcmc_chooser

LIST_OF_CHOOSERS = {
    'random': random_chooser.next,
    'random_forest_regressor': random_forest_regressor.next,
    'gpei': gp_ei_mcmc_chooser.next
}

DEFAULT_CHOOSER = 'gpei'
