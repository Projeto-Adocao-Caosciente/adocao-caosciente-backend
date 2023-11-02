class Utils:
    def treat_phone(phone_str: str) -> str:
        new_phone = ""
        for i in phone_str:
            if i >="0" and i <="9":
                new_phone += i
        return new_phone