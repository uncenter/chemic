from commoner import *
from main import *
from utils import *

def quick_search():
    Console.clear()
    string = input("Enter an element/formula: ")
    if iselement(string):
        molecule = Element(string)
        molecule.display()
    elif isformula(string):
        molecule = Formula(string)
    else:
        Shout.error("Invalid input")
        quick_search()
    if input("View more details? (y/N) ").lower() == "y":
        molecule.details()
        if input("View another element? (Y/n) ").lower() in ["y", ""]:
            quick_search()
    else:
        if input("View another element? (Y/n) ").lower() in ["y", ""]:
            quick_search()
        else:
            menu()


def view_details():
    Console.clear()
    string = input("Enter an element/formula: ")
    if iselement(string):
        molecule = Element(string)
        molecule.details()
    elif isformula(string):
        molecule = Formula(string)
        molecule.details()
    else:
        Shout.error("Invalid input")
        view_details()
    if input("View another element? (Y/n) ").lower() in ["y", ""]:
        view_details()
    else:
        menu()

def conversions():
    Console.clear()
    choice = create_menu("Mass to moles", "Moles to mass", "Atoms to moles", "Moles to atoms", "Particles to mass", "Mass to particles", "Back")
    if choice == "1":
        mass = float(input("Enter the mass: "))
        element = input("Enter the element: ")
        print(f"{mass} g {element} = {round(mass_to_moles(Element(element), mass))} mol {element}")
    elif choice == "2":
        moles = float(input("Enter the moles: "))
        element = input("Enter the element: ")
        print(f"{moles} mol {element} = {moles_to_mass(Element(element), moles)} g {element}")
    elif choice == "3":
        atoms = float(input("Enter the atoms: "))
        element = input("Enter the element: ")
        print(f"{atoms} {element} = {atoms_to_moles(Element(element), atoms)} mol {element}")
    elif choice == "4":
        moles = float(input("Enter the moles: "))
        element = input("Enter the element: ")
        print(f"{moles} mol {element} = {moles_to_atoms(Element(element), moles)} {element}")
    elif choice == "5":
        particles = float(input("Enter the particles: "))
        element = input("Enter the element: ")
        print(f"{particles} {element} = {particles_to_mass(Element(element), particles)} g {element}")
    elif choice == "6":
        mass = float(input("Enter the mass: "))
        element = input("Enter the element: ")
        print(f"{mass} g {element} = {mass_to_particles(Element(element), mass)} {element}")
    elif choice == "7":
        menu()
    else:
        Shout.error("Invalid choice")
        conversions()

def percent_composition():
    Console.clear()
    formula = input("Enter the formula: ")
    if isformula(formula):
        molecule = Formula(formula)
        get_percent_composition(molecule)
    else:
        Shout.error("Invalid formula")
        percent_composition()


def empirical_molecular():
    Console.clear()
    choice = create_menu("Calculate empirical formula", "Calculate molecular formula", "Back")
    if choice == "1":
        num_elements = int(input("Enter the number of elements: "))
        for i in range(num_elements):
            element = input(f"Enter the element {i+1}: ")
            mass = float(input(f"Enter the mass of {element}: "))
            if iselement(element):
                molecule = Element(element)
                print(f"Empirical formula: {get_empirical_formula(molecule, mass)}")
            else:
                Shout.error("Invalid element")
                empirical_molecular()
    elif choice == "2":
        formula = input("Enter the empirical formula: ")
        mass = float(input("Enter the mass: "))
        if isformula(formula):
            print(f"Molecular formula: {get_molecular_formula(formula, mass)}")
        else:
            Shout.error("Invalid formula")
            empirical_molecular()
    elif choice == "3":
        menu()
    else:
        Shout.error("Invalid choice")
        empirical_molecular()

def menu():
    choice = create_menu("Quick search", "View details", "Conversions and calculations", "Percent composition", "Empirical formula and molecular formula", "Exit")
    if choice == "1":
        quick_search()
    elif choice == "2":
        view_details()
    elif choice == "3":
        conversions()
    elif choice == "4":
        percent_composition()
    elif choice == "5":
        empirical_molecular()
    elif choice == "6":
        exit()
    else:
        Shout.error("Invalid choice")
        menu()

if __name__ == "__main__":
    Shout.welcome("cHelper", "uncenter", version="0.1.0", pause=True)
    menu()