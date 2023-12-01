import unicodedata

class Util:
    @staticmethod
    def remove_accents(text: str) -> str:
        return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")