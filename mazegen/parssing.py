from typing import Dict, Tuple, Any

H_42: int = 5
W_42: int = 7


def parse_config(config_file: str) -> Dict[str, Any]:
    """
    Parse a maze configuration file.

    The configuration file contains key=value pairs describing
    the maze parameters.

    Mandatory parameters:
        WIDTH (int)        : Maze width
        HEIGHT (int)       : Maze height
        ENTRY (x,y)        : Entry coordinates
        EXIT (x,y)         : Exit coordinates
        OUTPUT_FILE (str)  : Output file name (.txt)

    Optional parameters:
        PERFECT (bool)     : Whether the maze is perfect (default: True)
        SEED (int)         : Random seed
        ALGO (str)         : Algorithm to use ('dfs' or 'prim')

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        Dict[str, Any]: Parsed configuration dictionary.

    Raises:
        ValueError: If configuration values are invalid.
    """

    configuration: Dict[str, Any] = {
    }

    mandatory = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE"}
    int_fields = {"WIDTH", "HEIGHT", "SEED"}
    coord_fields = {"ENTRY", "EXIT"}
    str_fields = {"OUTPUT_FILE", "ALGO"}

    with open(config_file, "r") as file:

        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError("Invalid line format. Expected key=value")

            key, value = line.split("=", 1)
            key = key.strip().upper()
            value = value.strip()

            if key in configuration:
                raise ValueError(f"Duplicate parameter: {key}")

            if key in int_fields:
                try:
                    configuration[key] = int(value)
                except ValueError:
                    raise ValueError(f"{key} must be an integer")

            elif key in coord_fields:
                parts = value.split(",")

                if len(parts) != 2:
                    raise ValueError(f"{key} must contain two coordinates (x,y)")

                try:
                    x = int(parts[0].strip())
                    y = int(parts[1].strip())
                except ValueError:
                    raise ValueError(f"{key} coordinates must be integers")

                configuration[key] = (x, y)

            elif key == "PERFECT":
                value_lower = value.lower()

                if value_lower == "true":
                    configuration[key] = True
                elif value_lower == "false":
                    configuration[key] = False
                else:
                    raise ValueError("PERFECT must be TRUE or FALSE")

            elif key in str_fields:
                configuration[key] = value

            else:
                raise ValueError(f"Unknown parameter: {key}")

    for param in mandatory:
        if param not in configuration:
            raise ValueError(f"Missing mandatory parameter: {param}")

    width = configuration["WIDTH"]
    height = configuration["HEIGHT"]
    entry = configuration["ENTRY"]
    exit_ = configuration["EXIT"]

    if height < (H_42 + 2) or width < (W_42 + 2):
        raise ValueError("HEIGHT must be >= 7 and WIDTH must be >= 9")

    if entry == exit_:
        raise ValueError("ENTRY and EXIT must be different")

    if not (0 <= entry[0] < height and 0 <= entry[1] < width):
        raise ValueError("ENTRY must be inside the maze")

    if not (0 <= exit_[0] < height and 0 <= exit_[1] < width):
        raise ValueError("EXIT must be inside the maze")

    output_file = configuration["OUTPUT_FILE"]

    if not isinstance(output_file, str) or not output_file.endswith(".txt"):
        raise ValueError("OUTPUT_FILE must end with '.txt'")
    output_file = configuration["OUTPUT_FILE"]

    if " " in output_file:
        raise ValueError("OUTPUT_FILE must not contain spaces")

    if "ALGO" in configuration:
        algo = configuration["ALGO"].lower()

        if algo not in {"dfs", "prim"}:
            raise ValueError("ALGO must be 'dfs' or 'prim'")

        configuration["ALGO"] = algo

    return configuration