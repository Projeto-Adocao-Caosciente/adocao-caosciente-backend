from app.utils.mask import Mask

class Utils:
    def convert_to_digit(value: str) -> str:
        return  "".join(digit for digit in value if digit.isdigit())
    
    def convert_digit_to_mask(value: str, mask: Mask) -> str:
        return mask.format(value)