# -*- coding: utf-8 -*-

from datetime import date  # noqa analysis:ignore

from numpy import (   # noqa analysis:ignore
    logical_not as not_,
    maximum as max_,
    minimum as min_,
    round as round_,
    select,
    where,
    )

from openfisca_core.holders import (  # noqa analysis:ignore
    set_input_dispatch_by_period,
    set_input_divide_by_period,
    )
from openfisca_core.indexed_enums import Enum  # noqa analysis:ignore
from openfisca_core.populations import (ADD, DIVIDE)  # noqa analysis:ignore
from openfisca_core.simulations import (  # noqa analysis:ignore
    calculate_output_add,
    calculate_output_divide,
    )
from openfisca_core.variables import Variable  # noqa analysis:ignore
from openfisca_core.formula_helpers import apply_thresholds, concat, switch  # noqa analysis:ignore
from openfisca_core.periods import DAY, MONTH, YEAR, ETERNITY, period  # noqa analysis:ignore
from openfisca_core.reforms import Reform  # noqa analysis:ignore
from openfisca_core.parameters import load_parameter_file, ParameterNode, Scale, Bracket, Parameter, ValuesHistory  # noqa analysis:ignore
