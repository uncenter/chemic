from commoner import *
from main import *
from utils import *

import string

from nicegui import ui

ui.colors(primary="#299fbb")
from typing import Dict

def is_float(string):
    if string.replace(".", "").isnumeric():
        return True
    else:
        return False


def switch(menu, menu_item, text, func, **kwargs):
    menu.close()
    menu_item.set_text(text)
    func(**kwargs)


def quick_search():
    def result(molecule):
        bottom_content.clear()
        if (
            molecule not in string.whitespace
            and molecule != ""
            and molecule is not None
        ):
            molecule = Formula(molecule)
            with bottom_content:
                result_box = ui.card().classes("w-1/2")
                with result_box:
                    if molecule.name != "Unknown":
                        ui.label(f"{molecule.name}")
                    ui.label(f"{molecule.mass} g/mol")

    top_content.clear()
    with top_content:
        input_box = ui.card().classes("w-1/2")
    with input_box:
        molecule_input = ui.input(
            label="Molecule",
            placeholder="Ex. Fe or H2O",
            validation={"Invalid molecule": lambda x: isformula(x)},
        )
        with ui.row():
            ui.button("Submit", on_click=lambda: result(molecule_input.value))
            ui.button(
                "Clear",
                on_click=lambda: (molecule_input.set_value(""), bottom_content.clear()),
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
            result_box = ui.card().classes("w-1/2")
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
        input_box = ui.card().classes("w-1/2")
    with input_box:
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
            validation={"Not an element": lambda x: iselement(x)},
        )
        input_c = ui.select(label="Operation", options=operations, value=1)
        with ui.row():
            ui.button(
                "Submit",
                on_click=lambda: result(input_a.value, input_b.value, input_c.value),
            )
            ui.button("Clear", on_click=lambda: clear_all())

def percent_composition():
    bottom_content.clear()
    top_content.clear()

    def clear_all():
        input_a.set_value("")
        bottom_content.clear()

    def result(value):
        bottom_content.clear()
        with bottom_content:
            result_box = ui.card().classes("w-1/2")
        with result_box:
            ui.label(f"Total mass: {Formula(value).mass} g/mol")
            composition = get_percent_composition(Formula(value), False)
            for element in composition.items():
                ui.label(f"{element[0]}: {round(element[1], 2)}% ({round(element[1], 6)}%, {Element(element[0]).mass} g/mol)")


    top_content.clear()
    with top_content:
        input_box = ui.card().classes("w-1/2")
    with input_box:
        input_a = ui.input(
            label="Molecule",
            placeholder="Ex. H2O",
            validation={"Not a molecule": lambda x: isformula(x)},
        )
        with ui.row():
            ui.button(
                "Submit",
                on_click=lambda: result(input_a.value),
            )
            ui.button("Clear", on_click=lambda: clear_all())


def periodic_table():
    def details(data):
        bottom_content.clear()
        if (
            molecule not in string.whitespace
            and molecule != ""
            and molecule is not None
        ):
            molecule = Formula(molecule)
            with bottom_content:
                result_box = ui.card().classes("w-1/2")
                with result_box:
                    if molecule.name != "Unknown":
                        ui.label(f"{molecule.name}")
                    ui.label(f"{molecule.mass} g/mol")

    top_content.clear()
    bottom_content.clear()
    with top_content:
        input_box = ui.card().classes("w-full")
    with input_box:
        data = pd.read_csv("ptable.csv")
        columnDefs = [{'headerName': col, 'field': col} for col in data.columns[:7]]
        rowData = data.to_dict('records')
        grid = ui.aggrid({
            'columnDefs': columnDefs,
            'rowData': rowData,
            'rowSelection': 'single',
        })
        ui.button('View details', on_click=details)

tab_icons = ["home", "info"]


def switch_tab(msg: Dict) -> None:
    name = msg["args"]
    tabs.props(f"model-value={name}")
    panels.props(f"model-value={name}")


with ui.header().classes(replace="row items-center") as header:
    ui.label("Chemic").classes("text-2xl font-bold ml-4 mr-2")
    with ui.element("q-tabs").on("update:model-value", switch_tab) as tabs:
        for icon in tab_icons:
            ui.element("q-tab").props(f"name={icon} icon={icon}")

with ui.element("q-tab-panels").props("model-value=A animated").classes(
    "w-full"
) as panels:
    with ui.element("q-tab-panel").props(f"name=home").classes("w-full"):
        with ui.row():
            with ui.menu() as menu:
                ui.menu_item(
                    "Quick search",
                    on_click=lambda: switch(
                        menu, menu_toggle, "Quick search", quick_search
                    ),
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
                ui.menu_item(
                    "Percent composition",
                    lambda: switch(
                        menu, menu_toggle, "Percent composition", percent_composition
                    ),
                )
            menu_toggle = ui.button("Select", on_click=menu.open).classes("mb-2")
        top_content = ui.row().classes("mt-2")
        bottom_content = ui.row().classes("mt-2")
ui.run()
