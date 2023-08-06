#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2021.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#

# Before _sequential

from dask import delayed


def create_new_processor(
    processor_input: Processor, keys: t.Sequence, params: t.Mapping
) -> Processor:
    processor_output = deepcopy(processor_input)
    # new_key = deepcopy(keys)

    for key, value in zip(keys, params):
        processor_output.set(key=key, value=value)

    return processor_output


def collect(self, processor, with_dask: bool):

    delayed_processor = delayed(processor)

    lst = []

    all_steps = self.enabled_steps
    keys = (step.key for step in self.enabled_steps)  # tuple
    delayed_keys = delayed(keys)

    if with_dask:
        func = delayed(my_new_func)
    else:
        func = my_new_func

    # _embedded
    for params in itertools.product(*all_steps):
        delayed_params = delayed(params, pure=True)

        new_proc = func(
            processor_input=delayed_processor, keys=delayed_keys, params=delayed_params
        )

        lst.append(new_proc)

    return lst
