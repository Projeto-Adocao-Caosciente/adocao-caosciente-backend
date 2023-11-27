from enum import Enum

class Mask(Enum):
    """Enum class for mask types."""
    PHONE = "(xx) xxxxx-xxxx"
    CNPJ = "xx.xxx.xxx/xxxx-xx"
    CEP = "xxxxx-xxx"
    CPF = "xxx.xxx.xxx-xx"
    DATE = "dd/mm/yyyy"
    TIME = "hh:mm:ss"
    DATETIME = "dd/mm/yyyy hh:mm:ss"
    