from importing_config import import_config

def echo(type, output):
    statuscodes = import_config("config.json")["longterm_settings"]["statuscodes"]

    if type.lower() == "print":
        if output["status"] == statuscodes["Success"]:
            print(output["return"])
        else:
            print(f'{output["status"]}: {output["return"]}')
