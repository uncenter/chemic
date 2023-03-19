import data from './data.json' assert { type: 'json' };

const AVOGADRO = 6.02214076e23;

let periodicElements = { names: [], symbols: [] };
for (let i = 0; i < data.length; i++) {
    periodicElements.names.push(data[i].Element);
    periodicElements.symbols.push(data[i].Symbol);
}

function getMolarMass(moleculeObj) {
    let molarMass = 0;
    for (let element in moleculeObj.elements) {
        element = String(element);
        molarMass += new Molecule(element).mass * moleculeObj.elements[element];
    }
    return molarMass;
}

function getCount(moleculeObj) {
    let atoms = 0;
    for (let element in moleculeObj.elements) {
        atoms += moleculeObj.elements[element];
    }
    return atoms;
}

export function parseFormula(string) {
    function splitChemicalFormula(formula) {
        let substrings = [];
        let currentSubstring = "";
        for (let char of formula) {
            if (char == "(") {
                substrings.push([currentSubstring, 1]);
                currentSubstring = "";
            } else if (char == ")") {
                let multiplier = parseInt(formula[formula.indexOf(char) + 1]);
                if (!multiplier) {
                    multiplier = 1;
                }
                substrings.push([currentSubstring, multiplier]);
                currentSubstring = "";
            } else {
                currentSubstring += char;
            }
        }
        if (currentSubstring !== "" && isNaN(currentSubstring)) {
            substrings.push([currentSubstring, 1]);
        }
        return substrings;
    }
    function parseString(string) {
        let elements = {};
        let skip = false;
        for (let char of string) {
            if (char.match(/[A-Z]/)) {
                skip = false;
                if (string.indexOf(char) !== string.length - 1) {
                    if (string[string.indexOf(char) + 1].match(/[a-z]/)) {
                        char += string[string.indexOf(char) + 1];
                    }
                }
                if (!periodicElements.symbols.includes(char)) {
                    throw new Error("Invalid formula");
                }
                if (elements[char]) {
                    elements[char] += 1;
                } else {
                    elements[char] = 1;
                }
            }
            if (char.match(/[0-9]/) && !skip) {
                if ((string[string.indexOf(char)] + 1).match(/[0-9]/)) {
                    char += string[string.indexOf(char) + 1];
                    skip = true;
                }
                const lastElement = Object.keys(elements)[Object.keys(elements).length - 1];
                elements[lastElement] *= parseInt(char);
            }
        }
        return elements;
    }
    string = string.trim();
    if (string.match(/[^A-Za-z0-9\(\)]/)) {
        throw new Error("Invalid formula");
    }
    let substrings = splitChemicalFormula(string);
    let elements = {};
    for (let substring of substrings) {
        let parsedString = parseString(substring[0]);
        for (let element in parsedString) {
            if (elements[element]) {
                elements[element] += parsedString[element] * substring[1];
            } else {
                elements[element] = parsedString[element] * substring[1];
            }
        }
    }
    return elements;
}

function populateAttributes(attribute) {
    let matches = [];
    for (let i = 0; i < data.length; i++) {
        if (Object.values(data[i]).includes(attribute)) {
            matches.push(data[i]);
        }
    }
    return matches;
}
/**
 * @class Molecule
 * @param {string} attribute - The name, symbol, or atomic number of the element
 * @param {object} attribute - An object containing the elements and their counts
 * @param {string} attribute - A string containing the chemical formula
 * @property {string} name - The name of the element (e.g. Hydrogen)
 * @property {string} symbol - The symbol of the element
 * @property {number} number - The atomic number of the element
 * @property {number} mass - The atomic mass of the element
 * @property {number} count - The number of atoms in the molecule
 * @property {object} elements - An object containing the elements and their counts
 * @method toAtoms - Returns the number of atoms in a sample of the molecule
 * @method toParticles - Returns the number of particles in a sample of the molecule
 * @method toMoles - Returns the number of moles in a sample of the molecule
 * 
 * @example
 * const water = new Molecule("H2O");
 * const water = new Molecule({H: 2, O: 1});
 */
export class Molecule {
    constructor(attribute) {
        if (typeof attribute === "string" && attribute.length <= 2 && attribute.length > 0) {
            if (populateAttributes(attribute).length === 1) {
                const attributes = populateAttributes(attribute)[0];
                this.name = attributes.Element;
                this.symbol = attributes.Symbol;
                this.number = attributes.AtomicNumber;
                this.mass = parseFloat(attributes.AtomicMass);
                this.count = 1;
                this.elements = parseFormula(this.symbol);
                this.data = attributes;
            }
        } else if (typeof(attribute) === "object") {
            this.elements = attribute;
            this.name = "";
            this.symbol = "";
            this.number = null;
            this.mass = getMolarMass(this);
            this.count = getCount(this);
            this.data = null;
        } else {
            try {
                this.elements = parseFormula(attribute);
                this.name = "";
                this.symbol = "";
                this.number = null;
                this.mass = getMolarMass(this);
                this.count = getCount(this);
                this.data = null;
            } catch {
                throw new Error("Invalid formula");
            }
        }
    }

    toAtoms(sampleMass=1) {
        return (sampleMass / this.mass) * AVOGADRO * this.count;
    }

    toParticles(sampleMass=1) {
        return (sampleMass / this.mass) * AVOGADRO;
    }

    toMoles(sampleMass) {
        return sampleMass / this.mass
    }



    toFormula() {
        let formula = "";
        for (let element in this.elements) {
            formula += element;
            if (this.elements[element] > 1) {
                formula += this.elements[element];
            }
        }
        return formula;
    }
}