import re


def remove_csi(text):
    """
    Args:
        text:
    """
    text = str(text)
    return (
        re.sub(
            r"\\x1[bB]\[[\d;]*[a-zA-Z]",
            "",
            text.encode("unicode_escape").decode(),
        )
        .encode()
        .decode("unicode_escape")
    )


def screate(string, size=10, insert="r", filler_symbol=" "):
    """
    Args:
        string:
        size:
        insert:
        filler_symbol:
    """
    string = str(string)
    filler_symbol = str(filler_symbol)
    calcstring = remove_csi(string)

    spaces = str(filler_symbol) * (size - len(calcstring))
    if insert == "r":
        return string + spaces
    if insert == "l":
        return spaces + string


def sslice(text, chunk_size):
    """
    Args:
        text:
        chunk_size:
    """
    text = str(text)
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


def parse_args(readed):
    # [\'][a-zA-ZА-ЯЁа-яё\d\s[\]{}()\\\.\":;,-]*[\']|\b[a-zA-Z\d]+
    # [\"\'][a-zA-ZА-ЯЁа-яё‘\d\s[\]{}()@\\\.:;,-]*[\"\']|[a-zA-ZA-ZА-ЯЁа-яё‘\d\.[\]{}()@\\\.:;,-]+
    # [\"][a-zA-ZА-ЯЁа-яё‘\d\s[\]{}()@\\\.:;,\'-]*[\"]|[a-zA-ZA-ZА-ЯЁа-яё‘\d\.[\]{}()@\\\.:;,\'-]+
    # [\"][a-zA-ZА-ЯЁа-яё‘\d\s[\]{}()@\\\.:;,\'-/]*[\"]|[a-zA-ZA-ZА-ЯЁа-яё‘\d\.[\]{}()@\\\.:;,\'-/]+
    # [\"][a-zA-ZА-ЯЁа-яё‘\d\s[\]{}()@#_=%?\*\\\.:;,\'-/]*[\"]|[a-zA-ZA-ZА-ЯЁа-яё‘\d\.[\]{}()@\\\.:;,\'-/]+
    # [\"][a-zA-ZA-ZА-ЯЁа-яё‘\d.[\]{}()@\\:;,\'\-\/!?#$%^&*_+в„–\d]*[\"]|[a-zA-ZA-ZА-ЯЁа-яё‘\d.[\]{}()@\\:;,\'\-\/!?#$%^&*_+в„–]+
    # [\"][a-zA-ZA-ZА-ЯЁа-яё‘\d.[\]{}()<>@\\:;,\'\-\/!?#$%^&*_+в„–\d]*[\"]|[a-zA-ZA-ZА-ЯЁа-яё‘\d.[\]{}()@\\:;,\'\-\/!?#$%^&*_+в„–<>]+
    # \"[a-zA-ZA-ZА-ЯЁа-яё‘\d.[\]{}()<>@\\:;,\'\-\/!?#$%^&*_+в„–\s]*\"|[a-zA-ZA-ZА-ЯЁа-яё‘\d.[\]{}()@\\:;,\'\-\/!?#$%^&*_+в„–<>]+

    """
    Args:
        readed:
    """

    res = re.findall(
        r"\"[a-zA-ZA-ZА-ЯЁа-яё‘\d.[\]{}()<>@\\:;,\'\-\/!?#$%^&*_+в„–\s]*\"|[a-zA-ZA-ZА-ЯЁа-яё‘\d.[\]{}()@\\:;,\'\-\/!?#$%^&*_+в„–<>]+",
        readed,
        re.MULTILINE,
    )
    res2 = []
    for item in res:
        if item.startswith('"'):
            res2.append(item[1:-1])
        else:
            res2.append(item)
    res = [x for x in res2 if x != ""]

    if len(res) == 0:
        return {"command": "", "param": [], "paramCount": 0, "split": []}
    if len(res) == 1:
        return {"command": res[0], "param": [], "paramCount": 0, "split": [res[0]]}
    else:
        return {
            "command": res[0],
            "param": res[1:],
            "paramCount": len(res[1:]),
            "split": res,
        }
