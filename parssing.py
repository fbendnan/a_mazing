from typing import Dict

def mandatory_exist(configuration: Dict):
    mandatory = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
    for m in mandatory:
        if m not in configuration:
            return False
    return True


def parsser(config_file: str) -> Dict:
    configuration: Dict= {}
    try:
        with open(config_file, 'r') as configuratin_file:
            for line in configuratin_file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    raise ValueError(
                        "Invalid line format,"
                        " the line should containe key=value"
                    )
                line_s = line.split('=')
                to_check = line_s[0].strip().upper()
                if to_check == 'WIDTH' or to_check == 'HEIGHT' \
                   or to_check == 'SEED':
                    if to_check in configuration:
                        raise ValueError(
                            "you shouldn't duplicate a parametter"
                            )
                    else:
                        value = line_s[1].strip('\n')
                        configuration[to_check] = int(value)
                elif to_check == 'ENTRY' or to_check == 'EXIT':
                    if to_check in configuration:
                        raise ValueError(
                            "you shouldn't duplicate a parametter"
                            )
                    coord = line_s[1].split(',')
                    if len(coord) == 2:
                        configuration[to_check] = (
                            int(coord[0]), int(coord[1])
                            )
                    else:
                        raise ValueError(
                            "in Entry and Exit you must enter 2 values"
                            )
                elif to_check == 'PERFECT':
                    if to_check in configuration:
                        raise ValueError(
                            "you shouldn't duplicate a parametter"
                            )
                    if line_s[1].strip().upper() == 'TRUE':
                        configuration[to_check] = True
                    elif line_s[1].strip().upper() == 'FALSE':
                        configuration[to_check] = False
                elif to_check == 'OUTPUT_FILE' or to_check == 'ALGO':
                    if to_check in configuration:
                        raise ValueError(
                            "you shouldn't duplicate a parametter"
                            )
                    configuration[to_check] = str(line_s[1].strip('\n'))
                else:
                    raise ValueError(
                        "you enter a parameter does't needed...!"
                        )
            if len(configuration) < 6 \
                    or mandatory_exist(configuration) is False:
                raise ValueError(
                    "you should enter all the mandatory data needed: "
                    "'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', "
                    "'OUTPUT_FILE', 'PERFECT'"
                    )

            entry = configuration['ENTRY']
            exit = configuration['EXIT']
            width = configuration['WIDTH']
            height = configuration['HEIGHT']
            if not (entry[1] >= 0 and entry[1] < width):
                raise ValueError("The entry and Exit are invalid "
                                 "for this maze")
            elif not (exit[1] >= 0 and exit[1] < width):
                raise ValueError("The entry and Exit are invalid "
                                 "for this maze")
            elif not (entry[0] >= 0 and entry[0] < height):
                raise ValueError("The entry and Exit are invalid "
                                 "for this maze")
            elif not (exit[0] >= 0 and exit[0] < height):
                raise ValueError("The entry and Exit are invalid "
                                 "for this maze")
            # proba1: bool = (entry[0] < width and entry[1] == 0) \
            #     and (exit[0] < width and exit[1] == height - 1)
            # proba2: bool = (entry[0] < width and entry[1] == height - 1) \
            #     and (exit[0] < width and exit[1] == 0)
            # proba3: bool = (entry[0] == 0 and entry[1] < height) \
            #     and (exit[0] == width - 1 and exit[1] < height)
            # proba4: bool = (entry[0] == width - 1 and entry[1] < height) \
            #     and (exit[0] == 0 and exit[1] < height)
            
            # if proba1 is False and proba2 is False and proba3 is False \
            #    and proba4 is False:
                
        return configuration
    except Exception as e:
        print(f"Error: {e}")
