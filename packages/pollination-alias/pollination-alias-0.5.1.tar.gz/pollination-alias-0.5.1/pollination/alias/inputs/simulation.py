from pollination_dsl.alias import InputAlias
from queenbee.io.common import IOAliasHandler


"""Alias for inputs that expect a simulation parameter .json file as the recipe input."""
energy_simulation_parameter_input = [
    InputAlias.any(
        name='sim_par',
        description='A SimulationParameter object that describes all of the setting for '
        'the energy simulation. If None, some default simulation parameters will '
        'automatically be used. This can also be the path to a SimulationParameter '
        'JSON file.',
        optional=True,
        platform=['grasshopper'],
        handler=[
            IOAliasHandler(
                language='python',
                module='pollination_handlers.inputs.simulation',
                function='energy_sim_par_to_json'
            )
        ]
    )
]
