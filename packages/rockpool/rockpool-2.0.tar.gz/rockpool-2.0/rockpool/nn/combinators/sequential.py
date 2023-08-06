from rockpool.nn.modules.module import Module, ModuleBase
from rockpool.parameters import Parameter

from copy import copy

from typing import Tuple, Any

import numpy as onp

from abc import ABC

__all__ = ["Sequential"]


class SequentialMixin(ABC):
    """
    Base class for `Sequential` modules
    """

    def __init__(
        self, *args, **kwargs,
    ):
        # - Check that `shape` wasn't provided as a keyword argument
        if "shape" in kwargs:
            raise ValueError(
                "You may not provide a `shape` argument when building a Sequential module."
            )

        if "spiking_input" in kwargs:
            raise ValueError(
                "You may not provide a `spiking_input` argument when building a Sequential module."
            )

        if "spiking_output" in kwargs:
            raise ValueError(
                "You may not provide a `spiking_output` argument when building a Sequential module."
            )

        # - Collect the submodules
        submods = []
        submod_names = []
        other_args = []
        mod_index = 0
        for item in args:
            if isinstance(item, ModuleBase):
                # - Collect the module and define a name
                submods.append(item)
                submod_names.append(f"{mod_index}_{item.class_name}")
                mod_index += 1

            else:
                other_args.append(item)

        # - Work out shape of each submodule
        shape_in = [mod.size_in for mod in submods]
        shape_out = [mod.size_out for mod in submods]

        # - Check that shapes are compatible
        for mod_index in range(len(submods) - 1):
            if shape_out[mod_index] != shape_in[mod_index + 1]:
                raise ValueError(
                    f"The output of submodule {mod_index} "
                    + "({type(submods[mod_index]).__name__}) "
                    + "does not match the input shape of submodule "
                    + "{mod_index+1} ({type(submods[mod_index+1]).__name__})"
                )

        # - Call superclass __init__
        super().__init__(
            shape=(shape_in[0], shape_out[-1]),
            spiking_input=submods[0].spiking_input,
            spiking_output=submods[-1].spiking_output,
            *other_args,
            **kwargs,
        )

        # - Assign modules as submodules
        for (mod_name, submod) in zip(submod_names, submods):
            setattr(
                self, mod_name, submod,
            )

        # - Record module and weight lists
        self._submodule_names = submod_names

    def evolve(self, input_data, record: bool = False) -> Tuple[Any, Any, Any]:
        # - Initialise state and record dictionaries
        new_state_dict = {}
        record_dict = {}

        x = input_data

        # - Loop through submodules
        for submod_name in self._submodule_names:
            # - Get this submodule and weight
            mod = getattr(self, submod_name)

            # - Push data through submodule
            x, substate, subrec = mod(x, record=record)
            new_state_dict.update({submod_name: substate})
            record_dict.update(
                {submod_name: subrec, f"{submod_name}_output": copy(x),}
            )

        # - Return output, state and record
        return x, new_state_dict, record_dict

    def __getitem__(self, item: int) -> Module:
        """
        Permit indexing into the sequence of modules

        Args:
            item (int): The index of the module to return

        Returns:
            Module: The ``item``th module in the sequence
        """
        return self.modules()[self._submodule_names[item]]


class ModSequential(SequentialMixin, Module):
    pass


try:
    from rockpool.nn.modules.jax.jax_module import JaxModule
    from jax import numpy as jnp
    
    class JaxSequential(SequentialMixin, JaxModule):
        @classmethod
        def tree_unflatten(cls, aux_data, children):
            """Unflatten a tree of modules from Jax to Rockpool"""
            params, sim_params, state, modules = children
            _name, _shape, _submodulenames = aux_data
            modules = tuple(modules.values())
            obj = cls(*modules)
            obj._name = _name
    
            # - Restore configuration
            obj = obj.set_attributes(params)
            obj = obj.set_attributes(state)
            obj = obj.set_attributes(sim_params)
    
            return obj
except:
    class JaxSequential():
        def __init__(self):
            raise ImportError("'Jax' and 'Jaxlib' backend not found. Modules relying on Jax will not be available.")

def Sequential(*args, **kwargs) -> SequentialMixin:
    """
    Build a sequential stack of modules by connecting them end-to-end

    :py:class:`.Sequential` accepts any number of modules. The shapes of the modules must be compatible -- the output size :py:attr:`~.Module.size_out` of each module must match the input size :py:attr:`~.Module.size_in` of the following module.

    Examples:

        Build a :py:class:`.Sequential` stack will be returned a :py:class:`.Module`, containing ``mod0``, ``mod1`` and ``mod2``. When evolving this stack, signals will be passed through ``mod0``, then ``mod1``, then ``mod2``:

        >>> Sequential(mod0, mod1, mod2)

        Index into a :py:class:`.Sequential` stack using Python indexing:

        >>> mod = Sequential(mod0, mod1, mod2)
        >>> mod[0]
        A module with shape (xx, xx)

    Args:
        *mods: Any number of modules to connect. The :py:attr:`~.Module.size_out` attribute of one module must match the :py:attr:`~.Module.size_in` attribute of the following module.

    Returns:
        A :py:class:`.Module` subclass object that encapsulates the provided modules
    """
    # - Check for Jax submodules
    use_jax = False
    for item in args:
        if isinstance(item, JaxModule):
            use_jax = True

    # - Use either the JaxSequential or ModSequential classes
    if use_jax:
        return JaxSequential(*args, **kwargs)
    else:
        return ModSequential(*args, **kwargs)
