"""
Contains the module base classes for Rockpool
"""
# - Rockpool imports
from rockpool.parameters import ParameterBase

# - Other imports
from abc import ABC, abstractmethod
from warnings import warn
from collections import ChainMap
from typing import Tuple, Any, Iterable, Dict, Optional, List, Union
import numpy as np


class ModuleBase(ABC):
    """
    Base class for all `Module` subclasses in Rockpool
    """

    def __init__(
        self,
        shape: Optional[Tuple] = None,
        spiking_input: bool = False,
        spiking_output: bool = False,
        *args,
        **kwargs,
    ):
        """
        Initialise this module

        Args:
            shape (Optional[Tuple]): The shape of the defined module
            spiking_input (bool): Whether this module receives spiking input. Default: False
            spiking_output (bool): Whether this module produces spiking output. Default: False
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
        """
        # - Initialise co-classes etc.
        super().__init__(*args, **kwargs)

        # - Initialise Module attributes
        self._submodulenames: List[str] = []
        """Registry of sub-module names"""

        self._name: Optional[str] = None
        """Name of this module, if assigned"""

        self._spiking_input: bool = spiking_input
        """Whether this module receives spiking input"""

        self._spiking_output: bool = spiking_output
        """Whether this module produces spiking output"""

        # - Be generous if a scalar was provided instead of a tuple
        if isinstance(shape, Iterable):
            self._shape = tuple(shape)
            """The shape of this module"""
        else:
            self._shape = (shape,)
            """The shape of this module"""

    def __repr__(self, indent: str = "") -> str:
        """
        Produce a string representation of this module

        Args:
            indent (str): The indent to prepend to each line of output

        Returns:
            str: A string representation of this module
        """
        # - String representation
        repr = f"{indent}{self.full_name} with shape {self._shape}"

        # - Add submodules
        if self.modules():
            repr += " {"
            for mod in self.modules().values():
                repr += "\n" + mod.__repr__(indent=indent + "    ")

            repr += f"\n{indent}" + "}"

        return repr

    def _get_attribute_registry(self) -> Tuple[Dict, Dict]:
        """
        Return or initialise the attribute registry for this module

        Returns:
            (tuple): registered_attributes, registered_modules
        """
        if not hasattr(self, "_ModuleBase__registered_attributes") or not hasattr(
            self, "_ModuleBase__modules"
        ):
            super().__setattr__("_ModuleBase__registered_attributes", {})
            super().__setattr__("_ModuleBase__modules", {})

        # - Get the attribute and modules dictionaries in a safe way
        __registered_attributes = self.__dict__.get(
            "_ModuleBase__registered_attributes"
        )
        __modules = self.__dict__.get("_ModuleBase__modules")

        return __registered_attributes, __modules

    def __setattr__(self, name: str, val: Any):
        """
        Set an attribute for this module

        Args:
            name (str): The name of the attribute to set
            val (Any): The value to assign to the attribute
        """
        # - Get attribute registry
        __registered_attributes, __modules = self._get_attribute_registry()

        # - Check if this is a new rockpool Parameter
        if isinstance(val, ParameterBase):
            if hasattr(self, name):
                raise ValueError(
                    f'Cannot assign a new Parameter or State to an existing attribute "{name}".'
                )

            # - Register the attribute
            self._register_attribute(name, val)
            val = val.data

        # - Are we assigning a sub-module?
        if isinstance(val, ModuleBase):
            self._register_module(name, val)

        # - Check if this is an already registered attribute
        if name in __registered_attributes:
            # - Check that shapes are identical
            if hasattr(self, name):
                (_, _, _, _, shape) = __registered_attributes[name]
                if np.shape(val) != shape and val is not None:
                    raise ValueError(
                        f"The new value assigned to {name} must be of shape {shape}."
                    )

            # - Assign the value to the __registered_attributes dictionary
            __registered_attributes[name][0] = val

        # - Assign attribute to self
        super().__setattr__(name, val)

    def __delattr__(self, name: str):
        """
        Delete an attribute from this module, and remove from the attribute registry if present

        Args:
            name (str): The name of the attribute to delete
        """
        # - Get attribute registry
        __registered_attributes, __modules = self._get_attribute_registry()

        # - Remove attribute from registered attributes
        if name in __registered_attributes:
            del __registered_attributes[name]

        # - Remove name from modules
        if name in __modules:
            del __modules[name]
            self._submodulenames.remove(name)

        # - Remove attribute
        super().__delattr__(name)

    def _register_attribute(self, name: str, val: ParameterBase):
        """
        Record an attribute in the attribute registry

        Args:
            name (str): The name of the attribute to register
            val (ParameterBase): The `ParameterBase` subclass object to register. e.g. `Parameter`, `SimulationParameter` or `State`.
        """
        # - Get attribute registry
        __registered_attributes, __modules = self._get_attribute_registry()

        # - Record attribute in attribute registry
        __registered_attributes[name]: dict = [
            val.data,
            type(val).__name__,
            val.family,
            val.init_func,
            val.shape,
        ]
        """The attribute registry for this module"""

    def _register_module(self, name: str, mod: "ModuleBase"):
        """
        Register a sub-module in the module registry

        Args:
            name (str): The name of the module to register
            mod (ModuleBase): The `ModuleBase` object to register
        """
        # - Get attribute registry
        __registered_attributes, __modules = self._get_attribute_registry()

        if not isinstance(mod, ModuleBase):
            raise ValueError(
                f"You may only assign a `Module` subclass as a sub-module."
            )

        # - Assign module name to module
        mod._name = name

        # - Assign to appropriate attribute dictionary
        __modules[name] = [mod, type(mod).__name__]
        self._submodulenames.append(name)

    def set_attributes(self, new_attributes: dict) -> "ModuleBase":
        """
        Set the attributes and sub-module attributes from a dictionary

        This method can be used with the dictionary returned from module evolution to set the new state of the module. It can also be used to set multiple parameters of a module and submodules.

        Examples:
            Use the functional API to evolve, obtain new states, and set those states:

            >>> _, new_state, _ = mod(input)
            >>> mod = mod.set_attributes(new_state)

            Obtain a parameter dictionary, modify it, then set the parameters back:

            >>> params = mod.parameters()
            >>> params['w_input'] *= 0.
            >>> mod.set_attributes(params)

        Args:
            new_attributes (dict): A nested dictionary containing parameters of this module and sub-modules.
        """
        # - Get attribute registry
        __registered_attributes, __modules = self._get_attribute_registry()

        # - Set self attributes
        for (k, v) in __registered_attributes.items():
            if k in new_attributes:
                self.__setattr__(k, new_attributes[k])

        # - Set submodule attributes
        for (k, m) in __modules.items():
            if k in new_attributes:
                m[0].set_attributes(new_attributes[k])

        # - Return the module, for compatibility with the functional interface
        return self

    def _get_attribute_family(
        self, type_name: str, family: Union[str, Tuple, List] = None
    ) -> dict:
        """
        Search for attributes of this module and submodules that match a given family

        This method can be used to conveniently get all weights for a network; or all time constants; or any other family of parameters. Parameter families are defined simply by a string: ``"weights"`` for weights; ``"taus"`` for time constants, etc. These strings are arbitrary, but if you follow the conventions then future developers will thank you (that includes you in six month's time).

        Args:
            type_name (str): The class of parameters to search for. Must be one of ``["Parameter", "SimulationParameter", "State"]`` or another future subclass of :py:class:`.ParameterBase`
            family (Union[str, Tuple[str]]): A string or list or tuple of strings, that define one or more attribute families to search for

        Returns:
            dict: A nested dictionary of attributes that match the provided `type_name` and `family`
        """
        # - Get attribute registry
        __registered_attributes, __modules = self._get_attribute_registry()

        # - Filter own attribute dictionary by type key
        matching_attributes = {
            k: v for (k, v) in __registered_attributes.items() if v[1] == type_name
        }

        # - Filter by family
        if family is not None:
            if not isinstance(family, (tuple, list)):
                family = (family,)

            list_attributes = [
                {k: v for (k, v) in matching_attributes.items() if v[2] is f}
                for f in family
            ]
            matching_attributes = dict(ChainMap(*list_attributes))

        # - Just take values using getattr
        matching_attributes = {k: getattr(self, k) for k in matching_attributes.keys()}

        # - Append sub-module attributes as nested dictionaries
        submodule_attributes = {}
        for (k, m) in __modules.items():
            mod_attributes = m[0]._get_attribute_family(type_name, family)

            if (family and mod_attributes) or (not family):
                submodule_attributes[k] = mod_attributes

        # - Push submodule attributes into dictionary
        if family and submodule_attributes or not family:
            matching_attributes.update(submodule_attributes)

        # - Return nested attributes
        return matching_attributes

    def attributes_named(self, name: Union[Tuple[str], List[str], str]) -> dict:
        """
        Search for attributes of this or submodules by time

        Args:
            name (Union[str, Tuple[str]): The name of the attribute to search for

        Returns:
            dict: A nested dictionary of attributes that match `name`
        """
        # - Get attribute registry
        __registered_attributes, __modules = self._get_attribute_registry()

        # - Check if we were given a tuple or not
        if not isinstance(name, (tuple, list)):
            name = (name,)

        # - Filter own attribute dictionary by name keys
        list_attributes = [
            {k: v for (k, v) in __registered_attributes.items() if k == n} for n in name
        ]
        matching_attributes = dict(ChainMap(*list_attributes))

        # - Just take values
        matching_attributes = {k: v[0] for (k, v) in matching_attributes.items()}

        # - Append sub-module attributes as nested dictionaries
        submodule_attributes = {}
        for (k, m) in __modules.items():
            mod_attributes = m[0].attributes_named(name)

            if mod_attributes:
                submodule_attributes[k] = mod_attributes

        # - Push submodule attributes into dictionary
        if submodule_attributes:
            matching_attributes.update(submodule_attributes)

        # - Return nested attributes
        return matching_attributes

    def parameters(self, family: Union[str, Tuple, List] = None) -> Dict:
        """
        Return a nested dictionary of module and submodule Parameters

        Use this method to inspect the Parameters from this and all submodules. The optional argument `family` allows you to search for Parameters in a particular family — for example ``"weights"`` for all weights of this module and nested submodules.

        Although the `family` argument is an arbitrary string, reasonable choises are ``"weights"``, ``"taus"`` for time constants, ``"biases"`` for biases...

        Examples:
            Obtain a dictionary of all Parameters for this module (including submodules):

            >>> mod.parameters()
            dict{ ... }

            Obtain a dictionary of Parameters from a particular family:

            >>> mod.parameters("weights")
            dict{ ... }

        Args:
            family (str): The family of Parameters to search for. Default: ``None``; return all parameters.

        Returns:
            dict: A nested dictionary of Parameters of this module and all submodules
        """
        return self._get_attribute_family("Parameter", family)

    def simulation_parameters(self, family: Union[str, Tuple, List] = None) -> Dict:
        """
        Return a nested dictionary of module and submodule SimulationParameters

        Use this method to inspect the SimulationParameters from this and all submodules. The optional argument `family` allows you to search for SimulationParameters in a particular family.

        Examples:
            Obtain a dictionary of all SimulationParameters for this module (including submodules):

            >>> mod.simulation_parameters()
            dict{ ... }

        Args:
            family (str): The family of SimulationParameters to search for. Default: ``None``; return all SimulationParameter attributes.

        Returns:
            dict: A nested dictionary of SimulationParameters of this module and all submodules

        """
        return self._get_attribute_family("SimulationParameter", family)

    def state(self, family: Union[str, Tuple, List] = None) -> Dict:
        """
        Return a nested dictionary of module and submodule States

        Use this method to inspect the States from this and all submodules. The optional argument `family` allows you to search for States in a particular family.

        Examples:
            Obtain a dictionary of all States for this module (including submodules):

            >>> mod.state()
            dict{ ... }

        Args:
            family (str): The family of States to search for. Default: ``None``; return all State attributes.

        Returns:
            dict: A nested dictionary of States of this module and all submodules
        """
        return self._get_attribute_family("State", family)

    def modules(self) -> Dict:
        """
        Return a dictionary of all sub-modules of this module

        Returns:
            dict: A dictionary containing all sub-modules. Each item will be named with the sub-module name.
        """
        # - Get attribute registry
        __registered_attributes, __modules = self._get_attribute_registry()

        return {k: m[0] for (k, m) in __modules.items()}

    def _reset_attribute(self, name: str) -> "ModuleBase":
        """
        Reset an attribute to its initialisation value

        Args:
            name (str): The name of the attribute to reset

        Returns:
            self (`Module`): For compatibility with the functional API
        """
        # - Get attribute registry
        __registered_attributes, __modules = self._get_attribute_registry()

        # - Check that the attribute is registered
        if name not in __registered_attributes:
            raise KeyError(f"{name} is not a registered attribute.")

        # - Get the initialisation function from the registry
        (_, _, family, init_func, shape) = __registered_attributes[name]

        # - Use the registered initialisation function, if present
        if init_func is not None:
            setattr(self, name, init_func(shape))

        return self

    def _has_registered_attribute(self, name: str) -> bool:
        """
        Check if the module has a registered attribute

        Args:
            name (str): The name of the attribute to check

        Returns:
            bool: ``True`` if the attribute `name` is in the attribute registry, ``False`` otherwise.
        """
        __registered_attributes, _ = self._get_attribute_registry()
        return name in __registered_attributes

    def reset_state(self) -> "ModuleBase":
        """
        Reset the state of this module

        Returns:
            Module: The updated module is returned for compatibility with the functional API

        """
        # - Get attribute registry
        __registered_attributes, __modules = self._get_attribute_registry()

        # - Get a list of states
        states = self.state()

        # - Set self attributes
        for (k, v) in __registered_attributes.items():
            if k in states:
                self._reset_attribute(k)

        # - Reset submodule states
        for (k, m) in __modules.items():
            m[0] = m[0].reset_state()

        return self

    def reset_parameters(self):
        """
        Reset all parameters in this module

        Returns:
            Module: The updated module is returned for compatibility with the funcitonal API
        """
        # - Get attribute registry
        __registered_attributes, __modules = self._get_attribute_registry()

        # - Get a list of parameters
        parameters = self.parameters()

        # - Set self attributes
        for (k, v) in __registered_attributes.items():
            if k in parameters:
                self._reset_attribute(k)

        # - Reset submodule states
        for (k, m) in __modules.items():
            m[0] = m[0].reset_parameters()

        return self

    @property
    def class_name(self) -> str:
        """ str: Class name of ``self``
        """
        # - Determine class name by removing "<class '" and "'>" and the package information
        return type(self).__name__

    @property
    def name(self) -> str:
        """ str: The name of this module, or an empty string if ``None``
        """
        return f"'{self._name}'" if hasattr(self, "_name") and self._name else ""

    @property
    def full_name(self) -> str:
        """ str: The full name of this module (class plus module name)
        """
        return f"{self.class_name} {self.name}"

    @property
    def spiking_input(self) -> bool:
        """ bool: If ``True``, this module receives spiking input. If ``False``, this module expects continuous input. """
        return self._spiking_input

    @property
    def spiking_output(self):
        """ bool: If ``True``, this module sends spiking output. If ``False``, this module sends continuous output. """
        return self._spiking_output

    @property
    def shape(self) -> tuple:
        """ tuple: The shape of this module """
        return self._shape

    @property
    def size(self) -> int:
        """ int: (DEPRECATED) The output size of this module """
        warn(
            "The `size` property is deprecated. Please use `size_out` instead.",
            DeprecationWarning,
        )
        return self._shape[-1]

    @property
    def size_out(self) -> int:
        """ int: The output size of this module """
        return self._shape[-1]

    @property
    def size_in(self) -> int:
        """ int: The input size of this module """
        return self._shape[0]

    @abstractmethod
    def evolve(self, input_data, record: bool = False) -> Tuple[Any, Any, Any]:
        """
        Evolve the state of this module over input data

        NOTE: THIS MODULE CLASS DOES NOT PROVIDE DOCUMENTATION FOR ITS EVOLVE METHOD. PLEASE UPDATE THE DOCUMENTATION FOR THIS MODULE.

        Args:
            input_data: The input data with shape ``(T, size_in)`` to evolve with
            record (bool): If ``True``, the module should record internal state during evolution and return the record. If ``False``, no recording is required. Default: ``False``.

        Returns:
            tuple: (output, new_state, record)
                output (np.ndarray): The output response of this module with shape ``(T, size_out)``
                new_state (dict): A dictionary containing the updated state of this and all submodules after evolution
                record (dict): A dictionary containing recorded state of this and all submodules, if requested using the `record` argument
        """
        return None, None, None

    def __call__(self, input_data, *args, **kwargs):
        """
        Evolve the state of this module over input data

        Args:
            input_data: The input data with shape ``(T, size_in)`` to evolve this module with
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:

        """
        # - Catch the case where we have been called with the raw output of a previous call
        if isinstance(input_data, tuple) and len(input_data) == 3:
            input_data, new_state, recorded_state = input_data
            outputs, this_new_state, this_recorded_state = self.evolve(
                input_data, *args, **kwargs
            )
            new_state.update({self.name: this_new_state})
            recorded_state.update({self.name: this_recorded_state})
        else:
            outputs, new_state, recorded_state = self.evolve(
                input_data, *args, **kwargs
            )

        return outputs, new_state, recorded_state


class Module(ModuleBase, ABC):
    """
    The native Python / numpy ``Module`` base class for Rockpool
    """

    pass
    # def _register_module(self, name: str, mod: ModuleBase):
    #     """
    #     Register a submodule in the module registry
    #
    #     Args:
    #         name (str): The name to assign to the submodule
    #         mod (Module): The submodule to register. Must inherit from ``Module``
    #     """
    #     # - Register the module
    #     super()._register_module(name, mod)
    #
    #     # - Do we even have a `dt` attribute?
    #     if hasattr(self, "dt"):
    #         # - Check that the submodule `dt` is the same as mine
    #         if hasattr(mod, "dt"):
    #             if mod.dt != getattr(self, "dt"):
    #                 raise ValueError(
    #                     f"The submodule {mod.name} must have the same `dt` as the parent module {self.name}"
    #                 )
    #         else:
    #             # - Add `dt` as an attribute to the module (not a registered attribute)
    #             mod.dt = getattr(self, "dt")
    #
    #     else:
    #         # - We should inherit the first `dt` of a submodule
    #         if hasattr(mod, "dt"):
    #             setattr(self, "dt", mod.dt)


class PostInitMetaMixin(type(ModuleBase)):
    """
    A mixin base class that adds a ``__post_init__()`` method to a class. ``__post_init__()`` is called after the ``__init__()`` method, on instantiation of an object.
    """

    def __call__(cls, *args, **kwargs):
        obj = super().__call__(*args, **kwargs)
        if hasattr(cls, "__post_init__"):
            cls.__post_init__(obj)

        return obj
