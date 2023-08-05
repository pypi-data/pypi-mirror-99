import logging
from datetime import date

import pint
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
from geocurrency.converters.models import BaseConverter, ConverterResult, \
    ConverterResultDetail, ConverterResultError, ConverterLoadError, \
    CalculationResultError, CalculationResultDetail, CalculationResult
from sympy import sympify, SympifyError

from . import UNIT_EXTENDED_DEFINITION, DIMENSIONS, UNIT_SYSTEM_BASE_AND_DERIVED_UNITS, \
    ADDITIONAL_BASE_UNITS, PREFIX_SYMBOL
from .exceptions import *
from .settings import ADDITIONAL_UNITS, PREFIXED_UNITS_DISPLAY


class Quantity:
    """
    Quantity class
    """
    system = None
    unit = None
    value = 0
    date_obj = None

    def __init__(self, system: str, unit: str, value: float, date_obj: date = None):
        self.system = system
        self.unit = unit
        self.value = value
        self.date_obj = date_obj

    def __repr__(self):
        return f'{self.value} {self.unit} ({self.system})'


class Unit:
    pass


class UnitSystem:
    """
    Pint UnitRegistry wrapper
    """
    ureg = None
    system_name = None
    system = None

    def __init__(self, system_name: str = 'SI', fmt_locale: str = 'en', user: User = None,
                 key: str = None):
        found = False
        for available_system in UnitSystem.available_systems():
            if system_name.lower() == available_system.lower():
                system_name = available_system
                found = True
        if not found:
            raise UnitSystemNotFound("Invalid unit system")
        self.system_name = system_name
        try:
            additional_units_settings = settings.GEOCURRENCY_ADDITIONAL_UNITS
        except AttributeError:
            additional_units_settings = ADDITIONAL_UNITS
        try:
            self.ureg = pint.UnitRegistry(system=system_name, fmt_locale=fmt_locale)
            self.system = getattr(self.ureg.sys, system_name)
            self._load_additional_units(units=ADDITIONAL_BASE_UNITS)
            self._load_additional_units(units=additional_units_settings)
            if user:
                self._load_custom_units(user=user, key=key)
            self._rebuild_cache()
        except (FileNotFoundError, AttributeError):
            raise UnitSystemNotFound("Invalid unit system")

    def _rebuild_cache(self):
        """
        Rebuild registry cache
        It should be in the define method of the registry
        """
        self.ureg._build_cache()

    def _load_additional_units(self, units: dict) -> bool:
        """
        Load additional base units in registry
        """
        if not self.system_name in units:
            logging.warning(f"error loading additional units for {self.system_name}")
            return False
        for key, items in units[self.system_name].items():
            self.ureg.define(f"{key} = {items['relation']} = {items['symbol']}")
        return True

    def _load_custom_units(self, user: User, key: str = None) -> bool:
        """
        Load custom units in registry
        """
        if user and user.is_authenticated:
            if user.is_superuser:
                qs = CustomUnit.objects.all()
            else:
                qs = CustomUnit.objects.filter(user=user)
        if key:
            qs = qs.filter(key=key)
        for cu in qs:
            props = [cu.code, cu.relation]
            if cu.symbol:
                props.append(cu.symbol)
            if cu.alias:
                props.append(cu.alias)
            definition = " = ".join(props)
            self.ureg.define(definition)
        return True

    def _test_additional_units(self, units: dict) -> bool:
        """
        Load and check dimensionality of ADDITIONAL_BASE_UNITS values
        """
        if self.system_name not in units:
            return False
        for key in units[self.system_name].keys():
            try:
                test = self.unit(key).dimensionality and True
            except pint.errors.UndefinedUnitError:
                return False
        return True

    def add_definition(self, code, relation, symbol, alias):
        """
        Add a new unit definition to a UnitSystem, and rebuild cache
        """
        self.ureg.define(f"{code} = {relation} = {symbol} = {alias}")
        self._rebuild_cache()

    @classmethod
    def available_systems(cls) -> [str]:
        """
        List of available Unit Systems
        :return: Array of string
        """
        ureg = pint.UnitRegistry(system='SI')
        return dir(ureg.sys)

    @classmethod
    def is_valid(cls, system: str) -> bool:
        us = cls()
        return system in us.available_systems()

    def current_system(self) -> pint.UnitRegistry:
        """
        Return current pint.UnitRegistry
        """
        return self.ureg

    def unit(self, unit_name):
        return Unit(unit_system=self, code=unit_name)

    def available_unit_names(self) -> [str]:
        """
        List of available units for a given Unit system
        :return: Array of names of Unit systems
        """
        try:
            prefixed_units_display = settings.GEOCURRENCY_PREFIXED_UNITS_DISPLAY
        except AttributeError:
            prefixed_units_display = PREFIXED_UNITS_DISPLAY
        prefixed_units = []
        for key, prefixes in prefixed_units_display.items():
            for prefix in prefixes:
                prefixed_units.append(prefix + key)
        return sorted(prefixed_units + dir(getattr(self.ureg.sys, self.system_name)))

    def unit_dimensionality(self, unit: str) -> str:
        """
        User friendly representation of the dimension
        :param unit: name of the unit to display
        :return: Human readable dimension
        """
        return Unit.dimensionality_string(unit_system=self.system, unit_str=unit)

    def available_dimensions(self, ordering: str = 'name') -> {}:
        if ordering not in ['name', 'code', 'dimension']:
            ordering = 'name'
        return sorted([Dimension(unit_system=self, code=dim) for dim in DIMENSIONS.keys()],
                      key=lambda x: getattr(x, ordering, ''))

    @property
    def _ureg_dimensions(self):
        """
        return dimensions with units
        """
        dimensions = []
        for dim in self.ureg._dimensions:
            try:
                if not self.ureg.get_compatible_units(dim):
                    continue
                dimensions.append(dim)
            except KeyError:
                continue
        return dimensions

    def _get_dimension_dimensionality(self, dimension: str) -> {}:
        """
        Return the dimensionality of a dimension based on the first compatible unit
        """
        for dim in self.ureg.get_compatible_units(dimension):
            return self.ureg.get_base_units(dim)[1]

    def _generate_dimension_delta_dictionnary(self) -> {}:
        """
        Generate the dict to put in DIMENSIONS
        """
        output = {}
        for dim in self._ureg_dimensions:
            if not dim in DIMENSIONS:
                output[dim] = {
                    'name': f'_({dim})',
                    'dimension': str(self._get_dimension_dimensionality(dim)),
                    'symbol': ''
                }
        return output

    def units_per_dimension(self, dimensions: [str]) -> {}:
        output = {}
        registry_dimensions = dimensions or DIMENSIONS.keys()
        for dim in registry_dimensions:
            dimension = Dimension(unit_system=self, code=dim)
            try:
                if units := self.ureg.get_compatible_units(dim):
                    output[dim] = units
            except KeyError:
                continue
        return output

    def units_per_dimensionality(self) -> {}:
        """
        List of units per dimension
        :return: dict of dimensions, with lists of unit strings
        """
        units_array = self.available_unit_names()
        output = {}
        for unit_str in units_array:
            dimension = Unit.dimensionality_string(self, unit_str)
            try:
                output[dimension].append(unit_str)
            except KeyError:
                output[dimension] = [unit_str]
        return output

    @property
    def dimensionalities(self) -> [str]:
        """
        List of dimensions available in the Unit system
        :return: list of dimensions for Unit system
        """
        return set([Unit.dimensionality_string(self, unit_str) for unit_str in dir(self.system)])


class Dimension:
    """
    Dimenion of a Unit
    """
    unit_system = None
    code = None
    name = None
    dimension = None

    def __init__(self, unit_system: UnitSystem, code: str):
        try:
            dimension = DIMENSIONS[code]
            self.unit_system = unit_system
            self.code = code
            self.name = dimension['name']
            self.dimension = dimension['dimension']
        except (ValueError, KeyError) as e:
            logging.warning(str(e))
            self.code = None
        if not self.code:
            raise DimensionNotFound

    def __repr__(self):
        return self.code

    def units(self, user=None, key=None) -> [Unit]:
        """
        List of units for this dimension
        :param user: optional user for custom units
        :param key: optional key for custom units
        """
        if self.code == '[compounded]':
            return self._compounded_units
        if self.code == '[custom]':
            return self._custom_units(user=user, key=key)
        unit_list = []
        try:
            prefixed_units_display = settings.GEOCURRENCY_PREFIXED_UNITS_DISPLAY
        except AttributeError:
            prefixed_units_display = PREFIXED_UNITS_DISPLAY
        try:
            unit_list.append(
                self.unit_system.unit(
                    UNIT_SYSTEM_BASE_AND_DERIVED_UNITS[self.unit_system.system_name][self.code]
                )
            )
        except (KeyError, UnitNotFound):
            logging.warning("unable to find base unit for unit system and dimension")
        unit_list.extend(
            [
                Unit(unit_system=self.unit_system, pint_unit=unit)
                for unit in self.unit_system.ureg.get_compatible_units(self.code)
            ])
        unit_names = [str(u) for u in unit_list]
        for unit, prefixes in prefixed_units_display.items():
            if unit in unit_names:
                for prefix in prefixes:
                    unit_list.append(self.unit_system.unit(unit_name=prefix + unit))
        return set(sorted(unit_list, key=lambda x: x.name))

    @property
    def _compounded_units(self):
        """
        List units that do not belong to a dimension
        """
        available_units = self.unit_system.available_unit_names()
        dimensioned_units = []
        for dimension_code in [d for d in DIMENSIONS.keys() if
                               d != '[compounded]' and d != '[custom]']:
            dimension = Dimension(unit_system=self.unit_system, code=dimension_code)
            dimensioned_units.extend([u.code for u in dimension.units()])
        return [self.unit_system.unit(au) for au in set(available_units) - set(dimensioned_units)]

    def _custom_units(self, user: User, key: str = None) -> [Unit]:
        """
        Return list of custom units
        :param user: User owning the units
        :param key: optional unit key
        """
        if user and user.is_authenticated:
            if user.is_superuser:
                custom_units = CustomUnit.objects.all()
            else:
                custom_units = CustomUnit.objects.filter(user=user)
            if key:
                custom_units = custom_units.filter(key=key)
            return [self.unit_system.unit(cu.code) for cu in custom_units]
        else:
            return []

    @property
    def base_unit(self):
        """
        Base unit for this dimension in this Unit System
        """
        try:
            return UNIT_SYSTEM_BASE_AND_DERIVED_UNITS[self.unit_system.system_name][self.code]
        except KeyError:
            logging.warning(
                f'dimension {self.dimension} is not part of unit system {self.unit_system.system_name}')
            return None


class Unit:
    """
    Pint Unit wrapper
    """
    unit_system = None
    code = None
    unit = None

    def __init__(self, unit_system: UnitSystem, code: str = '', pint_unit: pint.Unit = None):
        """
        :param unit_system: UnitSystem instance
        :param code: code of the pint.Unit
        """
        self.unit_system = unit_system
        if pint_unit and isinstance(pint_unit, pint.Unit):
            self.code = str(pint_unit)
            self.unit = pint_unit
        elif code:
            self.code = code
            try:
                self.unit = getattr(unit_system.system, code)
            except pint.errors.UndefinedUnitError:
                raise UnitNotFound("invalid unit for system")
        else:
            raise UnitNotFound("invalid unit for system")

    def __repr__(self):
        return self.code

    @classmethod
    def is_valid(cls, name: str) -> bool:
        try:
            us_si = UnitSystem(system_name='SI')
        except UnitSystemNotFound:
            return False
        try:
            return us_si.unit(unit_name=name) and True
        except pint.errors.UndefinedUnitError:
            return False

    @property
    def name(self) -> str:
        return self.unit_name(self.code)

    @property
    def symbol(self) -> str:
        """
        Return symbol for Unit
        """
        return self.unit_symbol(self.code)

    @property
    def dimensions(self) -> [Dimension]:
        """
        Return Dimensions of Unit
        """
        dimensions = [Dimension(unit_system=self.unit_system, code=code) for code in
                      DIMENSIONS.keys()
                      if DIMENSIONS[code]['dimension'] == str(self.dimensionality)]
        return dimensions or '[compounded]'

    def base_unit(unit_str: str) -> (str, str):
        """
        Get base unit in case the unit is a prefixed unit
        :param unit_str: name of unit to check
        :return: base unit name, prefix
        """
        prefix = ''
        base_str = unit_str
        try:
            prefixed_units_display = settings.GEOCURRENCY_PREFIXED_UNITS_DISPLAY
        except AttributeError:
            prefixed_units_display = PREFIXED_UNITS_DISPLAY
        for base, prefixes in prefixed_units_display.items():
            for _prefix in prefixes:
                if unit_str == _prefix + base:
                    prefix = _prefix
                    base_str = base
        return base_str, prefix

    @staticmethod
    def unit_name(unit_str: str) -> str:
        """
        Get translated name from unit string
        :param unit_str: Name of unit
        """
        base_str, prefix = Unit.base_unit(unit_str=unit_str)
        try:
            ext_unit = UNIT_EXTENDED_DEFINITION.get(base_str)
            return prefix + str(ext_unit['name'])
        except (KeyError, TypeError) as e:
            logging.error(f'No UNIT_EXTENDED_DEFINITION for unit {base_str}')
            return unit_str

    @staticmethod
    def unit_symbol(unit_str: str) -> str:
        """
        Static function to get symbol from unit string
        :param unit_str: Name of unit
        """
        base_str, prefix = Unit.base_unit(unit_str=unit_str)
        try:
            prefix_symbol = PREFIX_SYMBOL[prefix]
            ext_unit = UNIT_EXTENDED_DEFINITION.get(base_str)
            return prefix_symbol + ext_unit['symbol']
        except (KeyError, TypeError) as e:
            logging.error(f'No UNIT_EXTENDED_DEFINITION for unit {base_str}')
            return ''

    @staticmethod
    def dimensionality_string(unit_system: UnitSystem, unit_str: str) -> str:
        """
        Converts pint dimensionality string to human readable string
        :param unit_system: UnitSystem
        :param unit_str: Unit name
        :return: str
        """
        ds = str(getattr(unit_system.ureg, unit_str).dimensionality).replace('[', '').replace(']',
                                                                                              '')
        ds = ds.replace(' ** ', '^')
        ds = ds.split()
        return ' '.join([_(d) for d in ds])

    @property
    def dimensionality(self):
        try:
            return self.unit_system.ureg.get_base_units(self.code)[1]
        except KeyError:
            return ''

    @staticmethod
    def translated_name(unit_system: UnitSystem, unit_str: str) -> str:
        try:
            return '{}'.format(unit_system.ureg[unit_str])
        except KeyError:
            return unit_str

    @property
    def readable_dimension(self):
        """
        Wrapper around Unit.dimensionality_string
        """
        return Unit.dimensionality_string(unit_system=self.unit_system, unit_str=self.code)


class UnitConverter(BaseConverter):
    """
    Conversion between units
    """
    base_system = None
    base_unit = None
    user = None
    key = None

    def __init__(self, base_system: str, base_unit: str, user: User = None, key: key = None,
                 id: str = None):
        try:
            super().__init__(id=id)
            self.base_system = base_system
            self.base_unit = base_unit
            self.user = user
            self.key = key
            self.system = UnitSystem(system_name=base_system, user=user, key=key)
            self.unit = Unit(unit_system=self.system, code=base_unit)
            self.compatible_units = [str(u) for u in self.unit.unit.compatible_units()]
        except (UnitSystemNotFound, UnitNotFound):
            raise UnitConverterInitError

    def add_data(self, data: []) -> []:
        """
        Check data and add it to the dataset
        Return list of errors
        """
        errors = super().add_data(data)
        return errors

    def check_data(self, data):
        """
        Validates that the data contains
        system = str
        unit = str
        value = float
        date_obj ('YYYY-MM-DD')
        """
        from .serializers import QuantitySerializer
        errors = []
        for line in data:
            serializer = QuantitySerializer(data=line)
            if serializer.is_valid():
                self.data.append(serializer.create(serializer.validated_data))
            else:
                errors.append(serializer.errors)
        return errors

    @classmethod
    def load(cls, id: str, user: User = None, key: str = None) -> BaseConverter:
        try:
            uc = super().load(id)
            uc.system = UnitSystem(system_name=uc.base_system, user=user, key=key)
            uc.unit = Unit(unit_system=uc.system, code=uc.base_unit)
            return uc
        except (UnitSystemNotFound, UnitNotFound, KeyError) as e:
            raise ConverterLoadError

    def save(self):
        system = self.system
        unit = self.unit
        self.system = None
        self.unit = None
        super().save()
        self.system = system
        self.unit = unit

    def convert(self) -> ConverterResult:
        """
        Converts data to base unit in base system
        """

        result = ConverterResult(id=self.id, target=self.base_unit)
        Q_ = self.system.ureg.Quantity
        for quantity in self.data:
            if quantity.unit not in self.compatible_units:
                error = ConverterResultError(
                    unit=quantity.unit,
                    original_value=quantity.value,
                    date=quantity.date_obj,
                    error=_('Incompatible units')
                )
                result.errors.append(error)
                continue
            try:
                pint_quantity = Q_(quantity.value, quantity.unit)
                out = pint_quantity.to(self.base_unit)
                result.increment_sum(out.magnitude)
                detail = ConverterResultDetail(
                    unit=quantity.unit,
                    original_value=quantity.value,
                    date=quantity.date_obj,
                    conversion_rate=0,
                    converted_value=out.magnitude
                )
                result.detail.append(detail)
            except pint.UndefinedUnitError:
                error = ConverterResultError(
                    unit=quantity.unit,
                    original_value=quantity.value,
                    date=quantity.date_obj,
                    error=_('Undefined unit in the registry')
                )
                result.errors.append(error)
        self.end_batch(result.end_batch())
        return result


class UnitConversionPayload:
    """
    Unit conversion payload
    """
    data = None
    base_system = ''
    base_unit = ''
    key = ''
    batch_id = ''
    eob = False

    def __init__(self, base_system: UnitSystem, base_unit: Unit, data=None, key: str = None,
                 batch_id: str = None, eob: bool = False):
        self.data = data
        self.base_system = base_system
        self.base_unit = base_unit
        self.key = key
        self.batch_id = batch_id
        self.eob = eob


class CustomUnit(models.Model):
    """
    Additional unit for a user
    """
    AVAILABLE_SYSTEMS = (
        ('Planck', 'Planck'),
        ('SI', 'SI'),
        ('US', 'US'),
        ('atomic', 'atomic'),
        ('cgs', 'CGS'),
        ('imperial', 'imperial'),
        ('mks', 'mks'),
    )
    user = models.ForeignKey(User, related_name='units', on_delete=models.PROTECT)
    key = models.CharField(max_length=255, default=None, db_index=True, null=True, blank=True)
    unit_system = models.CharField(max_length=20, choices=AVAILABLE_SYSTEMS)
    code = models.SlugField()
    name = models.CharField("Human readable name", max_length=255)
    relation = models.CharField("Relation to an existing unit", max_length=255)
    symbol = models.CharField("Symbol", max_length=20, blank=True, null=True)
    alias = models.CharField("Alias", max_length=20, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'key', 'code')

    def save(self, *args, **kwargs):
        """
        Save custom unit to database
        """
        us = UnitSystem(system_name=self.unit_system)
        if self.code in us.available_unit_names():
            raise UnitDuplicateError
        us.add_definition(code=self.code, relation=self.relation, symbol=self.symbol,
                          alias=self.alias)
        try:
            us.unit(self.code).unit.dimensionality
        except pint.errors.UndefinedUnitError:
            raise UnitDimensionError
        return super(CustomUnit, self).save(*args, **kwargs)


class Operand:
    """
    Operand in a formula
    """
    name = None
    value = None
    unit = None

    def __init__(self, name=None, value=None, unit=None):
        self.name = name
        self.value = value
        self.unit = unit

    def validate(self):
        if not self.name or self.value is None or self.unit is None:
            return False
        return True


class ComputationError(Exception):
    pass


class Expression:
    """
    Expression with operands
    """
    expression = None
    operands = None

    def __init__(self, expression: str, operands: [Operand]):
        self.expression = expression
        self.operands = operands

    def validate(self, unit_system: UnitSystem) -> (bool, str):
        Q_ = unit_system.ureg.Quantity
        if not self.expression:
            return False, "missing expression"
        try:
            sympify(self.expression.format(**{v.name: v.value for v in self.operands}))
        except SympifyError as e:
            return False, "Improper expression"
        for var in self.operands:
            if not var.validate():
                return False, "invalid operand"
        kwargs = {v.name: f"{v.value} {v.unit}" for v in self.operands}
        try:
            Q_(self.expression.format(**kwargs))
        except KeyError:
            return False, "Missing operand"
        except pint.errors.DimensionalityError:
            return False, "Incoherent dimensions"
        return True, ''

    def calculate(self, unit_system: UnitSystem) -> pint.Quantity:
        Q_ = unit_system.ureg.Quantity
        kwargs = {v.name: f"{v.value} {v.unit}" for v in self.operands}
        if self.validate(unit_system=unit_system):
            return Q_(self.expression.format(**kwargs))
        return None

    def evaluate(self, unit_system) -> pint.Quantity:
        Q_ = unit_system.ureg.Quantity
        is_valid, error = self.validate()
        if is_valid:
            kwargs = {v.name: f"{v.value} {v.unit}" for v in self.operands}
            return Q_(self.expression.format(kwargs))
        else:
            raise ComputationError("Invalid formula")


class CalculationPayload:
    """
    Calculation payload: caculate expressions
    """
    data = None
    unit_system = ''
    user = ''
    key = ''
    batch_id = ''
    eob = False

    def __init__(self, unit_system: UnitSystem, key: str = None, data: [] = None,
                 batch_id: str = None, eob: bool = False):
        self.data = data
        self.unit_system = unit_system
        self.key = key
        self.batch_id = batch_id
        self.eob = eob


class ExpressionCalculator(BaseConverter):
    """
    Conversion between units
    """
    unit_system = None

    def __init__(self, unit_system: str, user: User = None, key: str = '', id: str = None):
        """
        Initiate ExpressionCalculator
        :param unit_system: unit system name
        :param user: User
        :param key: key of user
        :param id: ID of the batch
        """
        try:
            super().__init__(id=id)
            self.unit_system = unit_system
            self.user = user
            self.key = key
            self.system = UnitSystem(system_name=unit_system, user=self.user, key=self.key)
        except (UnitSystemNotFound) as e:
            raise ExpressionCalculatorInitError from e

    def add_data(self, data: []) -> []:
        """
        Check data and add it to the dataset
        Return list of errors
        """
        errors = super().add_data(data)
        return errors

    def check_data(self, data):
        """
        Validates that the data contains
        - system (str)
        - unit (str)
        - value (float)
        - date (YYYY-MM-DD)
        """
        from .serializers import ExpressionSerializer
        errors = []
        for line in data:
            serializer = ExpressionSerializer(data=line)
            if serializer.is_valid(unit_system=self.system):
                self.data.append(serializer.create(serializer.validated_data))
            else:
                errors.append(serializer.errors)
        return errors

    @classmethod
    def load(cls, id: str, user: User = None, key: str = None) -> BaseConverter:
        """
        Load converter from batch
        :param id: ID of the batch
        """
        try:
            uc = super().load(id)
            uc.system = UnitSystem(system_name=uc.unit_system, user=user, key=key)
            return uc
        except (UnitSystemNotFound, KeyError) as e:
            raise ConverterLoadError

    def save(self):
        """
        Save converter to caching system
        """
        system = self.system
        self.system = None
        super(ExpressionCalculator, self).save()
        self.system = system

    def convert(self) -> CalculationResult:
        """
        Converts data to base unit in base system
        """

        result = CalculationResult(id=self.id)
        Q_ = self.system.ureg.Quantity
        for expression in self.data:
            valid, exp_error = expression.validate(unit_system=self.system)
            if not valid:
                error = CalculationResultError(
                    expression=amount.unit,
                    original_value=amount.value,
                    date=amount.date_obj,
                    error=exp_error
                )
                result.errors.append(error)
                continue
            out = expression.calculate(unit_system=self.system)
            detail = CalculationResultDetail(
                expression=expression.expression,
                operands=expression.operands,
                magnitude=out.magnitude,
                units=out.units
            )
            result.detail.append(detail)
        self.end_batch(result.end_batch())
        return result
