from .config import COMMANDS


def validateCmd(input: list[str]) -> tuple[str | None, str | None, bool]:
    # Initialize command and arg
    cmd = ""
    arg = None

    # Validate input
    if len(input) < 1 or len(input) > 2:
        print("Invalid input\n")
        return None, None, False

    # Assign the command
    cmd = input[0]

    # If argument is provided, assign it to a variable
    if len(input) > 1:
        arg = input[1]

    # Validate cmd
    if cmd not in COMMANDS:
        print("Invalid command")
        print("Valid commands:")
        print("\tls")
        print("\tget <file name>")
        print("\tput <file name>")
        print("\tquit\n")
        return None, None, False

    # Validate argument
    if cmd == "get" or cmd == "cmd":
        if len(input) != 2:
            print("Invalid command")
            print("Valid commands:")
            print("\tls")
            print("\tget <file name>")
            print("\tput <file name>")
            print("\tquit\n")
            return None, None, False

    return cmd, arg, True
