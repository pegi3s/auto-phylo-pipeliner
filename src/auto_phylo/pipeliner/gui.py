from argparse import ArgumentParser, FileType

from auto_phylo.pipeliner import load_commands, check_for_new_versions
from auto_phylo.pipeliner.component.AutoPhyloPipeliner import AutoPhyloPipeliner


def launch():
    parser = ArgumentParser(prog="auto-phylo pipeliner", description="A graphical pipeline designer for auto-phylo")
    parser.add_argument("-c", "--commands", type=FileType("r"), dest="commands_file",
                        help="A custom commands.json file. It will be loaded as a valid auto-phylo version.")
    parser.add_argument("-d", "--disable-update-commands", action="store_true",
                        help="When not disabled, auto-phylo pipeliner will check on-line for the commands available "
                             "in new versions of auto-phylo")

    args = parser.parse_args()

    if not args.disable_update_commands:
        check_for_new_versions()

    if args.commands_file:
        commands = load_commands({"Custom": args.commands_file})
    else:
        commands = load_commands()

    designer = AutoPhyloPipeliner(commands=commands)
    designer.minsize(width=900, height=600)
    designer.mainloop()


if __name__ == "__main__":
    launch()
