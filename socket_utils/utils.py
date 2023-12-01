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
        print("\t'ls' to list file in server")
        print("\t'get <file name>' to download file")
        print("\t'put <file name>' to upload file")
        print("\t'quit' to exit\n")
        return None, None, False

    # Validate argument
    if cmd == "get" or cmd == "cmd":
        if len(input) != 2:
            print("Invalid command")
            print("Valid commands:")
            print("\t'ls' to list file in server")
            print("\t'get <file name>' to download file")
            print("\t'put <file name>' to upload file")
            print("\t'quit' to exit\n")
            return None, None, False

    return cmd, arg, True
