import { Molecule } from "./molecule.js";

const PERCENT_ERROR = 0.03;

function getEmpiricalFormula(percentages) {
    let ratio = {};
    let toMoles = {};
    let sum = Object.values(percentages).reduce((a, b) => a + b, 0);
    if (sum === 1 || sum === 100) {
        if (sum === 1) {
            percentages = Object.keys(percentages).map((key) => {
                return [key, percentages[key] * 100];
            });
        } else {
            percentages = Object.keys(percentages).map((key) => {
                return [key, percentages[key]];
            });
        }
        percentages.forEach((item) => {
            const ELEMENT = item[0];
            const PERCENTAGE = item[1];
            toMoles[ELEMENT] = PERCENTAGE / new Molecule(String(ELEMENT)).mass;
        });
        let min = Math.min(...Object.values(toMoles));
        for (let element in toMoles) {
            ratio[element] = parseFloat((toMoles[element] / min).toFixed(2));
        }
        // Check if each value of the ratio is within the PERCENT_ERROR
        for (let element in ratio) {
            if (ratio[element] !== 1) {
                if (
                    Math.round(ratio[element]) <=
                        ratio[element] + PERCENT_ERROR * ratio[element] &&
                    Math.round(ratio[element]) >=
                        ratio[element] - PERCENT_ERROR * ratio[element]
                ) {
                    ratio[element] = Math.round(ratio[element]);
                } else {
                    for (let i = 2; i < 50; i++) {
                        if (+(ratio[element] * i).toFixed(2) % 1 === 0) {
                            for (let element in ratio) {
                                ratio[element] = ratio[element] * i;
                            }
                            break;
                        }
                    }
                }
            }
        }
        return ratio;
    }
}

function getMolecularFormula(
    mass,
    empiricalFormula = null,
    percentages = null
) {
    if (empiricalFormula === null) {
        empiricalFormula = getEmpiricalFormula(percentages);
    }
    let molecularFormula = {};
    let molecularMass = new Molecule(empiricalFormula).mass;
    for (let element in empiricalFormula) {
        molecularFormula[element] = Math.round(
            (empiricalFormula[element] * mass) / molecularMass
        );
    }
    return molecularFormula;
}

function getPercentages(mass, formula) {
    for (let element in formula) {
        formula[element] = formula[element] / mass;
    }
    return formula;
}

function getPercentComposition(formula, round = false) {
    if (!(formula instanceof Molecule)) {
        formula = new Molecule(formula);
    }
    let percentComposition = {};
    const molecularMass = formula.mass;
    for (let element in formula.elements) {
        percentComposition[element] =
            ((new Molecule(element).mass * formula.elements[element]) /
                molecularMass) *
            100;
        if (round) {
            if (round === true) {
                round = 2;
            }
            percentComposition[element] = parseFloat(
                percentComposition[element].toFixed(round)
            );
        }
    }
    return percentComposition;
}

export {
    getEmpiricalFormula,
    getMolecularFormula,
    getPercentages,
    getPercentComposition,
};
