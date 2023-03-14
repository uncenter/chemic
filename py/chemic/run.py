from commoner import *
from .main import *
from .utils import *

import string

from typing import Dict
from nicegui import ui


def gui():
    """
    Start the GUI.
    """
    GITHUB_BUTTON = """<a href="https://github.com/uncenter/chemic" target"_blank" type="button" class="text-white bg-[#24292F] font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center mr-2 mb-2 mt-3 mb-5">
    <svg class="w-4 h-4 mr-2 -ml-1" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24.774" width="24" height="24.774"><path fill="currentColor" d="M8.027 19.229c0 .097-.111.174-.252.174-.16.015-.271-.063-.271-.174 0-.097.111-.174.252-.174.145-.015.271.063.271.174zm-1.505-.218c-.034.097.063.208.208.237.126.048.271 0 .3-.097s-.063-.208-.208-.252c-.126-.034-.266.015-.3.111zm2.139-.082c-.14.034-.237.126-.223.237.015.097.14.16.285.126.14-.034.237-.126.223-.223-.015-.092-.145-.155-.285-.14zM11.845.387C5.134.387 0 5.482 0 12.194c0 5.366 3.377 9.958 8.202 11.574.619.111.837-.271.837-.585 0-.3-.015-1.955-.015-2.971 0 0-3.387.726-4.098-1.442 0 0-.552-1.408-1.345-1.771 0 0-1.108-.76.077-.745 0 0 1.205.097 1.868 1.248 1.06 1.868 2.835 1.331 3.527 1.011.111-.774.426-1.311.774-1.631-2.705-.3-5.434-.692-5.434-5.347 0-1.331.368-1.998 1.142-2.85-.126-.315-.537-1.611.126-3.285C6.672 5.085 9 6.706 9 6.706c.968-.271 2.008-.411 3.039-.411s2.071.14 3.039.411c0 0 2.327-1.626 3.339-1.306.663 1.679.252 2.971.126 3.285.774.856 1.248 1.524 1.248 2.85 0 4.669-2.85 5.042-5.555 5.347.445.382.823 1.108.823 2.245 0 1.631-.015 3.648-.015 4.045 0 .315.223.697.837.585C20.719 22.152 24 17.56 24 12.194 24 5.482 18.556.387 11.845.387zM4.703 17.076c-.063.048-.048.16.034.252.077.077.189.111.252.048.063-.048.048-.16-.034-.252-.077-.077-.189-.111-.252-.048zm-.523-.392c-.034.063.015.14.111.189.077.048.174.034.208-.034.034-.063-.015-.14-.111-.189-.097-.029-.174-.015-.208.034zm1.568 1.723c-.077.063-.048.208.063.3.111.111.252.126.315.048.063-.063.034-.208-.063-.3-.106-.111-.252-.126-.315-.048zm-.552-.711c-.077.048-.077.174 0 .285.077.111.208.16.271.111.077-.063.077-.189 0-.3-.068-.111-.194-.16-.271-.097z"/></svg>
    Github
    </a>"""
    WIDTH = "w-full"

    ui.colors(primary="#299fbb")

    def search():
        def result(molecule):
            bottom_content.clear()
            if (
                molecule not in string.whitespace
                and molecule != ""
                and molecule is not None
            ):
                molecule = Formula(molecule)
                with bottom_content:
                    result_box = ui.card().classes(WIDTH)
                    with result_box:
                        if molecule.name != "Unknown":
                            ui.label("Name").classes("font-bold mt-2")
                            ui.label(f"{molecule.name}")
                            ui.separator()
                        ui.label("Molecular formula").classes("font-bold mt-2")
                        ui.label(f"{molecule.mass} g/mol")
                        if len(molecule.elements) > 1:
                            ui.separator()
                            ui.label("Percent composition").classes("font-bold mt-2")
                            composition = get_percent_composition(molecule, False)
                            for element in composition.items():
                                ui.label(
                                    f"{element[0]}: {round(element[1], 2)}% ({round(element[1], 6)}%, {Element(element[0]).mass} g/mol)"
                                )
                        else:
                            molecule = Element(list(molecule.elements.keys())[0])
                            if molecule.data["Metal"] == "yes":
                                ui.separator()
                                ui.label("Type: Metal").classes("font-bold mt-2")
                            elif molecule.data["Metalloid"] == "yes":
                                ui.separator()
                                ui.label("Type: Metalloid").classes("font-bold mt-2")
                            elif molecule.data["Nonmetal"] == "yes":
                                ui.separator()
                                ui.label("Type: Nonmetal").classes("font-bold mt-2")

        top_content.clear()
        with top_content:
            input_box = ui.card().classes(WIDTH)
        with input_box:
            with ui.card().style("border: 1px solid var(--q-info);"):
                ui.icon("info", color="blue")
                ui.label(
                    "Enter a formula or element and press submit to search for it. This will display the name, molar mass, percent composition, and type of the molecule."
                )

            def submit(value):
                if value is not None:
                    result(value)

            molecule_input = ui.input(
                label="Molecule",
                placeholder="Ex. Fe or H2O",
                validation={"Invalid molecule": lambda x: isformula(x)},
            )
            with ui.row():
                ui.button("Submit", on_click=lambda: submit(molecule_input.value))
                ui.button(
                    "Clear",
                    on_click=lambda: (
                        molecule_input.set_value(""),
                        bottom_content.clear(),
                    ),
                )

    def conversions():
        bottom_content.clear()
        top_content.clear()

        def clear_all():
            input_a.set_value("")
            input_b.set_value("")
            bottom_content.clear()

        def result(value1, value2, operation):
            bottom_content.clear()
            with bottom_content:
                result_box = ui.card().classes(WIDTH)
            if operation == 1:
                with result_box:
                    ui.label(
                        f"{value1} g {value2} = {round(mass_to_moles(Formula(value2), value1), 2)} mol {value2}"
                    )
            elif operation == 2:
                with result_box:
                    ui.label(
                        f"{value1} g {value2} = {round(mass_to_atoms(Formula(value2), value1), 2)} atoms {value2}"
                    )
            elif operation == 3:
                with result_box:
                    ui.label(
                        f"{value1} g {value2} = {round(mass_to_particles(Formula(value2), value1), 2)} particles {value2}"
                    )
            elif operation == 4:
                with result_box:
                    ui.label(
                        f"{value1} mol {value2} = {round(moles_to_mass(Formula(value2), value1), 2)} g {value2}"
                    )
            elif operation == 5:
                with result_box:
                    ui.label(
                        f"{value1} mol {value2} = {round(moles_to_atoms(Formula(value2), value1), 2)} atoms {value2}"
                    )
            elif operation == 6:
                with result_box:
                    ui.label(
                        f"{value1} atoms {value2} = {round(atoms_to_mass(Formula(value2), value1), 2)} g {value2}"
                    )
            elif operation == 7:
                with result_box:
                    ui.label(
                        f"{value1} atoms {value2} = {round(atoms_to_moles(Formula(value2), value1), 2)} mol {value2}"
                    )
            elif operation == 8:
                with result_box:
                    ui.label(
                        f"{value1} particles {value2} = {round(particles_to_mass(Formula(value2), value1), 2)} g {value2}"
                    )

        top_content.clear()
        with top_content:
            input_box = ui.card().classes(WIDTH)
        with input_box:
            with ui.card().style("border: 1px solid var(--q-negative);"):
                ui.icon("warning", color="red")
                ui.label(
                    "This feature is still in development and may not work properly. Confirm calculations are within expected range."
                )

            def submit(value, value2, value3):
                if all([value, value2, value3]):
                    result(value, value2, value3)

            operations = {
                1: "Mass to moles",
                2: "Mass to atoms",
                3: "Mass to particles",
                4: "Moles to mass",
                5: "Moles to atoms",
                6: "Atoms to mass",
                7: "Atoms to moles",
                8: "Particles to mass",
            }

            input_a = ui.number(
                label="Number",
                placeholder="Ex. 10",
            )
            input_b = ui.input(
                label="Element",
                placeholder="Ex. H",
                validation={"Not an element": lambda x: isformula(x)},
            )
            input_c = ui.select(label="Operation", options=operations, value=1)
            with ui.row():
                ui.button(
                    "Submit",
                    on_click=lambda: submit(
                        input_a.value, input_b.value, input_c.value
                    ),
                )
                ui.button("Clear", on_click=lambda: clear_all())

    def periodic_table():
        def result(data):
            bottom_content.clear()
            if (
                molecule not in string.whitespace
                and molecule != ""
                and molecule is not None
            ):
                molecule = Formula(molecule)
                with bottom_content:
                    result_box = ui.card().classes(WIDTH)
                    with result_box:
                        if molecule.name != "Unknown":
                            ui.label(f"{molecule.name}")
                        ui.label(f"{molecule.mass} g/mol")

        bottom_content.clear()
        top_content.clear()
        with top_content:
            input_box = ui.card().classes("w-full")
        with input_box:

            def submit(value):
                if value is not None:
                    result(value)

            data = PERIODIC_TABLE
            columnDefs = [{"headerName": col, "field": col} for col in data.columns[:7]]
            rowData = data.to_dict("records")
            grid = ui.aggrid(
                {
                    "columnDefs": columnDefs,
                    "rowData": rowData,
                    "rowSelection": "single",
                }
            )

    def switch(menu, menu_item, text, func, **kwargs):
        menu.close()
        menu_item.set_text(text)
        func(**kwargs)

    with ui.header().classes(replace="row justify-between h-16"):
        ui.label("Chemic").classes("text-2xl font-bold ml-4 mr-2 my-4")
        ui.html(GITHUB_BUTTON)

    with ui.element("div").classes("w-full"):
        with ui.row():
            with ui.menu() as menu:
                ui.menu_item(
                    "Search",
                    on_click=lambda: switch(menu, menu_toggle, "Search", search),
                )
                ui.menu_item(
                    "Periodic table",
                    on_click=lambda: switch(
                        menu, menu_toggle, "Periodic table", periodic_table
                    ),
                )
                ui.separator()
                ui.menu_item(
                    "Conversions",
                    lambda: switch(menu, menu_toggle, "Conversions", conversions),
                )
            menu_toggle = ui.button("Select", on_click=menu.open).classes("mb-2")
        top_content = ui.row().classes("mt-2")
        bottom_content = ui.row().classes("mt-2")

    ui.run(
        title="Chemic",
        favicon="https://a.mtstatic.com/@public/production/site_4334/1478193457-favicon.ico",
        reload=False,
    )


def cli():
    """
    Start the CLI (deprecated, use `gui()` instead).
    """

    def search():
        Console.clear()
        string = input("Enter an element/formula: ")
        if iselement(string):
            molecule = Element(string)
            molecule.display()
        elif isformula(string):
            molecule = Formula(string)
        else:
            Shout.error("Invalid input")
            search()
        if input("View more details? (y/N) ").lower() == "y":
            molecule.details()
            if input("View another element? (Y/n) ").lower() in ["y", ""]:
                search()
        else:
            if input("View another element? (Y/n) ").lower() in ["y", ""]:
                search()
            else:
                menu()

    def details():
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
            details()
        if input("View another element? (Y/n) ").lower() in ["y", ""]:
            details()
        else:
            menu()

    def conversions():
        Console.clear()
        choice = create_menu(
            "Mass to moles",
            "Moles to mass",
            "Atoms to moles",
            "Moles to atoms",
            "Particles to mass",
            "Mass to particles",
            "Back",
        )
        if choice == "1":
            mass = float(input("Enter the mass: "))
            element = input("Enter the element: ")
            print(
                f"{mass} g {element} = {round(mass_to_moles(Element(element), mass))} mol {element}"
            )
        elif choice == "2":
            moles = float(input("Enter the moles: "))
            element = input("Enter the element: ")
            print(
                f"{moles} mol {element} = {moles_to_mass(Element(element), moles)} g {element}"
            )
        elif choice == "3":
            atoms = float(input("Enter the atoms: "))
            element = input("Enter the element: ")
            print(
                f"{atoms} {element} = {atoms_to_moles(Element(element), atoms)} mol {element}"
            )
        elif choice == "4":
            moles = float(input("Enter the moles: "))
            element = input("Enter the element: ")
            print(
                f"{moles} mol {element} = {moles_to_atoms(Element(element), moles)} {element}"
            )
        elif choice == "5":
            particles = float(input("Enter the particles: "))
            element = input("Enter the element: ")
            print(
                f"{particles} {element} = {particles_to_mass(Element(element), particles)} g {element}"
            )
        elif choice == "6":
            mass = float(input("Enter the mass: "))
            element = input("Enter the element: ")
            print(
                f"{mass} g {element} = {mass_to_particles(Element(element), mass)} {element}"
            )
        elif choice == "7":
            menu()
        else:
            Shout.error("Invalid choice")
            conversions()
        if input("Again? (Y/n) ").lower() in ["y", ""]:
            conversions()
        else:
            menu()

    def percent_composition():
        Console.clear()
        formula = input("Enter the formula: ")
        if isformula(formula):
            molecule = Formula(formula)
            comp = get_percent_composition(molecule, True)
            for element in comp:
                print(f"{element}: {comp[element]}%")
                if input("Again? (Y/n) ").lower() in ["y", ""]:
                    percent_composition()
                else:
                    menu()
        else:
            Shout.error("Invalid formula")
            percent_composition()

    def empirical_molecular():
        Console.clear()
        choice = create_menu(
            "Calculate empirical formula", "Calculate molecular formula", "Back"
        )
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
        if input("Again? (Y/n) ").lower() in ["y", ""]:
            empirical_molecular()

    def menu():
        choice = create_menu(
            "Quick search",
            "View details",
            "Conversions and calculations",
            "Percent composition",
            "Empirical formula and molecular formula",
            "Exit",
        )
        if choice == "1":
            search()
        elif choice == "2":
            details()
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

    Shout.welcome("Chemic", "uncenter", version="0.9", pause=True)
    Shout.warning("This CLI is deprecated, use `gui()` instead.")
    menu()
