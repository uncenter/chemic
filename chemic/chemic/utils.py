from commoner import reverse, replace_all, Shout, Chalk

def validate_cas_number(cas_num, verbose=True):
    if not isinstance(cas_num, str):
        if verbose:
            Shout.error("CAS number is not a string")
        return False
    if len(replace_all(cas_num, "-", "")) > 10:
        if verbose:
            Shout.error("CAS number is too long")
        return False
    cas_num = {
        "full": cas_num,
        "clean": replace_all(cas_num, "-", ""),
        "parts": cas_num.split("-"),
    }
    if len(cas_num["parts"]) != 3:
        if verbose:
            Shout.error("CAS number is not formatted correctly [x(2-7)-x(2)-x(1)]")
        return False
    check_sum = 0
    check_sum_num = reverse(cas_num["parts"][0] + cas_num["parts"][1])
    for i in range(0, len(check_sum_num)):
        check_sum += int(check_sum_num[i]) * (i + 1)
    check_sum = check_sum % 10
    if check_sum != int(cas_num["parts"][2]):
        if verbose:
            Shout.error(
                f"Check sum does not match check digit [{check_sum} != {cas_num['parts'][2]}]"
            )
        return False
    if verbose:
        Shout.success("CAS number is valid")
    return True


def parse_formula(formula):
    element_dict = {}
    looking_for_num = False
    skip = False
    element = ""
    for i in range(len(formula)):
        if skip:
            skip = False
            continue
        elif formula[i] == "(":
            if looking_for_num:
                element_dict[element] = 1
                looking_for_num = False
            for j in range(i, len(formula)):
                if formula[j] == ")":
                    index = j
                    break
            result = parse_formula(formula[i + 1 : index])
            multiplier = None
            for k in range(index + 1, len(formula)):
                if formula[k].isdigit():
                    multiplier = int(formula[index + 1 : k + 1])
                else:
                    break
            if multiplier == None:
                multiplier = 1
            for sub_element, sub_num_atoms in result.items():
                if sub_element in element_dict:
                    element_dict[sub_element] += sub_num_atoms * (multiplier)
                else:
                    element_dict[sub_element] = sub_num_atoms * (multiplier)
            formula = formula.replace(formula[: index + (1 + len(str(multiplier)))], "")
            sub_element_dict = parse_formula(formula)
            for sub_element, sub_num_atoms in sub_element_dict.items():
                if sub_element in element_dict:
                    element_dict[sub_element] += sub_num_atoms
                else:
                    element_dict[sub_element] = sub_num_atoms
            return element_dict
        if formula[i].isupper():
            if looking_for_num:
                element_dict[element] = 1
                looking_for_num = False
            element = formula[i]
            num_atoms = 1
            looking_for_num = True
        elif formula[i].islower():
            if i == 0 or not formula[i - 1].isupper():
                if formula[i - 1].islower():
                    element_dict[element] = 1
                element = formula[i].upper()
                num_atoms = 1
            else:
                element += formula[i]
            looking_for_num = True
        elif formula[i].isdigit():
            if i < len(formula) - 1 and formula[i + 1].isdigit():
                num_atoms = int(formula[i : i + 2])
                skip = True
            else:
                num_atoms = int(formula[i])
            if element in element_dict:
                element_dict[element] += num_atoms
            else:
                element_dict[element] = num_atoms
            looking_for_num = False
        else:
            return
    if looking_for_num:
        element_dict[element] = num_atoms
    new_dict = {}
    for element, num_atoms in element_dict.items():
        if element != '':
            new_dict[element] = num_atoms
    return new_dict


def create_menu(*args, cursor="> ", prompt="Select an option: "):
    print(prompt)
    for i in range(len(args)):
        print(f"{i + 1}. {args[i]}")
    while True:
        try:
            choice = int(input(Chalk.cyan(cursor)))
            if int(choice) > len(args) or int(choice) < 1:
                raise ValueError
            return str(choice)
        except ValueError:
            print("Invalid choice")