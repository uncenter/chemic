from commoner import *
from .utils import validate_cas_number, parse_formula

import pandas as pd
import pydash
import importlib.resources


PERIODIC_TABLE = pd.read_csv(
    importlib.resources.open_text("chemic", "periodic_table.csv")
)
FORMULA_TABLE = pd.read_csv(
    importlib.resources.open_text("chemic", "common_formulas.csv")
)
AVOGADRO = 6.02214076e23
L_STP = 22.4


def reconstruct_formula(formula):
    """
    Reconstruct a formula from a dictionary.

    Args:
        formula (dict): The formula to reconstruct.

    Returns:
        str: The reconstructed formula.
    """
    reconstruct_formula = []
    for element in formula:
        if formula[element] == 1:
            reconstruct_formula.append(element)
        else:
            reconstruct_formula.append(f"{element}{formula[element]}")
    return "".join(reconstruct_formula)


def get_molar_mass(molecule):
    """
    Get the molar mass of a molecule.

    Args:
        molecule (Formula, Element): The molecule to get the molar mass of.

    Returns:
        float: The molar mass of the molecule.
    """
    molar_mass = 0
    if isinstance(molecule, Formula):
        for element in molecule.elements:
            molar_mass += (molecule.elements[element]) * Element(element).mass
    elif isinstance(molecule, Element):
        return molecule.mass
    else:
        return None
    return molar_mass


def get_formula_name(formula, verbose=False):
    """
    Get the name of a molecule from its formula.

    Args:
        formula (str): The formula of the molecule.
        verbose (bool, optional): Whether to print the process. Defaults to False.

    Returns:
        str: The name of the molecule.
    """
    if type(formula) != str:
        return None
    if validate_cas_number(formula, False):
        if verbose:
            Shout.info("CAS number detected")
        if formula in FORMULA_TABLE["CAS"].values:
            return FORMULA_TABLE[FORMULA_TABLE["CAS"] == formula]["Names"].values[0]
        else:
            return None
    else:
        if verbose:
            Shout.info("Formula detected")
        if formula in FORMULA_TABLE["Formula"].values:
            return (
                FORMULA_TABLE[FORMULA_TABLE["Formula"] == formula]["Names"]
                .values[0]
                .split("\n")[0]
            )
        else:
            return None


class Element:
    """
    A class to represent an element.

    Args:
        attribute (str, int): The attribute to use to initialize the element.

    Attributes:
        data (dict): The data of the element.
        symbol (str): The symbol of the element.
        name (str): The name of the element.
        number (int): The atomic number of the element.
        mass (float): The atomic mass of the element.
        count (int): The number of atoms of the element in a molecule.

    Methods:
        display: Display the element in a "periodic table"-like format.
        details: Display the details of the element.

    Examples:
        >>> element = Element("H")
        >>> element.display()
        ┌────────────────────┐
        │1.008              1│
        │                    │
        │         H          │
        │                    │
        │      Hydrogen      │
        └────────────────────┘
        >>> print(Element("H").details())
        Atomic Number: 1
        Element: Hydrogen
        Symbol: H
        Atomic Mass: 1.008
        Number Of Neutrons: 0
        Number Of Protons: 1
        Number Of Electrons: 1
        ...
    """

    def __init__(self, attribute):
        if type(attribute) == str:
            if attribute.isdigit():
                attribute = int(attribute)
            else:
                attribute = attribute.capitalize()
        attr_types = ["Symbol", "Element", "AtomicNumber", "AtomicMass"]
        for attr_type in attr_types:
            if attribute in PERIODIC_TABLE[attr_type].values:
                self.data = PERIODIC_TABLE[
                    PERIODIC_TABLE[attr_type] == attribute
                ].to_dict("records")[0]
                self.symbol = self.data["Symbol"]
                self.name = self.data["Element"]
                self.number = self.data["AtomicNumber"]
                self.mass = self.data["AtomicMass"]
                self.count = 1
                break
        else:
            return None

    def display(self):
        """
        Display the element in a "periodic table"-like format.
        """
        # References:
        # https://docs.python.org/3/library/string.html#format-specification-mini-language
        # https://kuvapcsitrd01.kutztown.edu/~schwesin/fall20/csc223/lectures/Python_String_Formatting.html
        # https://en.wikipedia.org/wiki/Box-drawing_character
        width = 20
        if len(self.name) > 10:
            width = round(len(self.name) * 1.8)
            if width % 2 != 0:
                width -= 1
        sections = {
            "blank": f"│{width * ' '}│",
            "top": f"┌{width * '─'}┐",
            "bottom": f"└{width * '─'}┘",
            "sep": f"├{width * '─'}┤",
        }
        Chalk.set("bold")
        print(sections["top"])
        print(f"│{str(self.mass).ljust(width//2)}{str(self.number).rjust(width//2)}│")
        print(sections["blank"])
        print(f"│{str(self.symbol).center(width)}│")
        print(sections["blank"])
        print(f"│{str(self.name).center(width)}│")
        print(sections["bottom"])
        Chalk.reset()
        return

    def details(self):
        """
        Display the details of the element.
        """
        for key in self.data:
            print(f"{pydash.separator_case(key, ' ').title()}: {self.data[key]}")
        return

    def __str__(self):
        return f"{self.symbol}"

    def __repr__(self):
        return f"Element({self.symbol}, {self.name}, {self.number}, {self.mass})"

    def __eq__(self, other):
        if isinstance(other, Element):
            return self.symbol == other.symbol
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if isinstance(other, Element):
            return Formula({self: 1, other: 1})
        return NotImplemented

    def __sub__(self, other):
        return ValueError("Cannot subtract elements")

    def __mul__(self, other):
        if isinstance(other, int):
            return Formula({self: other})
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return ValueError("Cannot divide elements")

    def __rtruediv__(self, other):
        return ValueError("Cannot divide elements")

    def __floordiv__(self, other):
        return ValueError("Cannot divide elements")

    def __rfloordiv__(self, other):
        return ValueError("Cannot divide elements")

    def __mod__(self, other):
        return ValueError("Cannot mod elements")

    def __rmod__(self, other):
        return ValueError("Cannot mod elements")

    def __pow__(self, other):
        return ValueError("Cannot raise elements to a power")

    def __rpow__(self, other):
        return ValueError("Cannot raise elements to a power")

    def __lt__(self, other):
        if isinstance(other, Element):
            return self.number < other.number
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Element):
            return self.number <= other.number
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Element):
            return self.number > other.number
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Element):
            return self.number >= other.number
        return NotImplemented

    def __hash__(self):
        return hash(self.symbol)

    def __len__(self):
        return None

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        return iter(self.data)


class Formula:
    """
    A class to represent a chemical formula.

    Args:
        elements (str, dict, Element): The elements in the formula.

    Attributes:
        elements (dict): The elements in the formula.
        mass (float): The molar mass of the formula.
        name (str): The name of the formula.
        count (int): The number of elements in the formula.

    Methods:
        display: Display the formula in a "periodic table"-like format.
        details: Display the details of the formula.
        __str__: Return the formula as a string.

    Examples:
        >>> print(Formula("H2O").mass)
        18.015
        >>> print(Formula("H2O").name)
        Water
    """

    def __init__(self, elements):
        if isinstance(elements, str):
            if elements.isdigit():
                raise ValueError("Invalid formula")
            elements = parse_formula(elements.strip())
        elif isinstance(elements, Element):
            elements = {elements: 1}
        else:
            if not isinstance(elements, dict):
                return ValueError("Invalid formula")
        self.elements = {
            Element(element).symbol: elements[element] for element in elements
        }
        self.mass = get_molar_mass(self)
        self.name = get_formula_name(reconstruct_formula(self.elements))
        if self.name == None:
            if len(self.elements) == 1:
                element = list(self.elements.keys())[0]
                if element in PERIODIC_TABLE["Symbol"].values:
                    self.name = Element(element).name
            else:
                self.name = "Unknown"
        else:
            self.name = str(self.name).title()
        self.count = 0
        for element in self.elements:
            self.count += self.elements[element]

    def __str__(self):
        return reconstruct_formula(self.elements)

    def __repr__(self):
        return f"Formula({self.elements})"

    def __eq__(self, other):
        if isinstance(other, Formula):
            return self.elements == other.elements
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if isinstance(other, Formula):
            return Formula({**self.elements, **other.elements})
        elif isinstance(other, Element):
            for element in self.elements:
                if element == other:
                    return Formula(
                        {**self.elements, **{element: self.elements[element] + 1}}
                    )
            return Formula({**self.elements, **{other: 1}})
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Formula):
            return Formula(
                {
                    **self.elements,
                    **{
                        element: -1 * other.elements[element]
                        for element in other.elements
                    },
                }
            )
        elif isinstance(other, Element):
            for element in self.elements:
                if element == other:
                    return Formula(
                        {**self.elements, **{element: self.elements[element] - 1}}
                    )
            return ValueError("Cannot subtract element not in formula")
        return NotImplemented

    def __lt__(self, other):
        return self.mass < other.mass

    def __le__(self, other):
        return self.mass <= other.mass

    def __gt__(self, other):
        return self.mass > other.mass

    def __ge__(self, other):
        return self.mass >= other.mass

    def __hash__(self):
        return hash(self.elements)

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, key):
        return self.elements[key]

    def __iter__(self):
        return iter(self.elements)

    def __contains__(self, item):
        return item in self.elements


def iselement(value):
    """
    Check if a value is an element.

    Args:
        value (any): The value to check.

    Returns:
        bool: True if the value is an element, False otherwise.
    """
    try:
        Element(value)
        return True
    except:
        return False


def isformula(value):
    """
    Check if a value is a formula.

    Args:
        value (any): The value to check.

    Returns:
        bool: True if the value is a formula, False otherwise.
    """
    try:
        Formula(value)
        return True
    except:
        return False


def mass_to_moles(molecule, mass):
    """
    Convert mass to moles.

    Args:
        molecule (Element, Formula, str): The molecule.
        mass (float): The mass.

    Returns:
        float: The moles.
    """
    if isinstance(molecule, Element) or isinstance(molecule, Formula):
        return mass / molecule.mass
    elif isinstance(molecule, str):
        return mass / Formula(molecule).mass
    return None


def moles_to_mass(molecule, moles):
    """
    Convert moles to mass.

    Args:
        molecule (Element, Formula, str): The molecule.
        moles (float): The moles.

    Returns:
        float: The mass.
    """
    if isinstance(molecule, Element) or isinstance(molecule, Formula):
        return moles * molecule.mass
    elif isinstance(molecule, str):
        return moles * Formula(molecule).mass
    return None


def mass_to_atoms(molecule, mass):
    """
    Convert mass to atoms.

    Args:
        molecule (Element, Formula, str): The molecule.
        mass (float): The mass.

    Returns:
        float: The atoms.
    """
    if isinstance(molecule, Element) or isinstance(molecule, Formula):
        return mass / molecule.mass * AVOGADRO * molecule.count
    elif isinstance(molecule, str):
        return mass / Formula(molecule).mass * AVOGADRO * Formula(molecule).count
    return None


def atoms_to_mass(molecule, atoms):
    """
    Convert atoms to mass.

    Args:
        molecule (Element, Formula, str): The molecule.
        atoms (float): The atoms.

    Returns:
        float: The mass.
    """
    if isinstance(molecule, Element) or isinstance(molecule, Formula):
        return atoms / AVOGADRO * molecule.mass
    elif isinstance(molecule, str):
        return atoms / AVOGADRO * Formula(molecule).mass
    return None


def mass_to_particles(molecule, mass):
    """
    Convert mass to particles.

    Args:
        molecule (Element, Formula, str): The molecule.
        mass (float): The mass.

    Returns:
        float: The particles.
    """
    if isinstance(molecule, Element) or isinstance(molecule, Formula):
        return mass / molecule.mass * AVOGADRO
    elif isinstance(molecule, str):
        return mass / Formula(molecule).mass * AVOGADRO
    return None


def particles_to_mass(molecule, particles):
    """
    Convert particles to mass.

    Args:
        molecule (Element, Formula, str): The molecule.
        particles (float): The particles.

    Returns:
        float: The mass.
    """
    if isinstance(molecule, Element) or isinstance(molecule, Formula):
        return particles / AVOGADRO * molecule.mass
    elif isinstance(molecule, str):
        return particles / AVOGADRO * Formula(molecule).mass
    return None


def moles_to_atoms(molecule, moles):
    """
    Convert moles to atoms.

    Args:
        molecule (Element, Formula, str): The molecule.
        moles (float): The moles.

    Returns:
        float: The atoms.
    """
    if isinstance(molecule, Element) or isinstance(molecule, Formula):
        return moles * AVOGADRO * molecule.count
    elif isinstance(molecule, str):
        return moles * AVOGADRO * Formula(molecule).count
    return None


def atoms_to_moles(molecule, atoms):
    """
    Convert atoms to moles.

    Args:
        molecule (Element, Formula, str): The molecule.
        atoms (float): The atoms.

    Returns:
        float: The moles.
    """
    if isinstance(molecule, Element) or isinstance(molecule, Formula):
        return atoms / AVOGADRO / molecule.count
    elif isinstance(molecule, str):
        return atoms / AVOGADRO / Formula(molecule).count
    return None


def get_empirical_formula(percentages):
    """
    Get the empirical formula from percentages of elements.

    Args:
        percentages (dict): The percentages of elements in the formula, summed to 1 or 100 (e.g. {'C': 0.5, 'H': 0.5} or {'C': 50, 'H': 50}).

    Returns:
        Formula: The empirical formula.
    """
    if isinstance(percentages, dict):
        elements = [key for key in percentages]
        if not all([iselement(element) for element in elements]):
            return ValueError("Invalid percentages (not all elements)")
        if sum(percentages.values()) == 1 or sum(percentages.values()) == 100:
            if sum(percentages.values()) == 100:
                percentages = {key: value / 100 for key, value in percentages.items()}
            empirical_num_atoms = {
                key: value / Element(key).mass for key, value in percentages.items()
            }
            empirical_ratio = {
                key: round(value / min(empirical_num_atoms.values()))
                for key, value in empirical_num_atoms.items()
            }
            for element in empirical_ratio:
                print(f"{element}: {empirical_ratio[element]}")
            return Formula(empirical_ratio)
    else:
        return ValueError("Invalid input (not a dictionary)")


def get_molecular_formula(empirical_formula, mass):
    """
    Get the molecular formula from the empirical formula and the mass.

    Args:
        empirical_formula (Formula, dict): The empirical formula.
        mass (float): The mass.

    Returns:
        Formula: The molecular formula.
    """
    if isinstance(empirical_formula, dict):
        empirical_formula = Formula(empirical_formula)
    if isinstance(empirical_formula, Formula):
        if isinstance(mass, (int, float)):
            molecular_mass = empirical_formula.mass
            molecular_ratio = {
                key: round((value * mass) / molecular_mass)
                for key, value in empirical_formula.elements.items()
            }
            return Formula(molecular_ratio)
    else:
        return ValueError("Invalid input (not a formula)")


def get_percent_composition(formula, round_result=False):
    """
    Get the percent composition of a formula.

    Args:
        formula (Formula): The formula.
        round_result (bool, optional): Whether to round the result. Defaults to False.

    Returns:
        dict: The percent composition of each element in the formula.
    """
    if isinstance(formula, Formula):
        if round_result:
            return {
                key: round((Element(key).mass * value / formula.mass) * 100, 2)
                for key, value in formula.elements.items()
            }
        return {
            key: (Element(key).mass * value / formula.mass) * 100
            for key, value in formula.elements.items()
        }
    else:
        return ValueError("Invalid input (not a formula)")


def get_percent_error(actual, theoretical):
    """
    Get the percent error between two numbers.

    Args:
        actual (int, float): The actual value.
        theoretical (int, float): The theoretical value.

    Returns:
        float: The percent error.
    """
    if isinstance(actual, (int, float)) and isinstance(theoretical, (int, float)):
        return abs(actual - theoretical) / theoretical * 100
    else:
        return ValueError("Invalid input (not a number)")
