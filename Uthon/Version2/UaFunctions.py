from TranslateUaToPy import PyWordToUa


def ua_dir(obj_) -> list:
    """Returns dir() but in ukrainian format"""
    return [PyWordToUa(attribute) for attribute in dir(obj_)]


if __name__ == "__main__":
    print(ua_dir(5))
