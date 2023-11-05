class Utils:
    def treat_phone(phone_str: str) -> str:
        new_phone = ""
        for i in phone_str:
            if "0" <= i <= "9":
                new_phone += i
        return new_phone