def validate_ip(any_that_can_be_ip: any) -> bool:
    if not isinstance(any_that_can_be_ip, str):
        return False
    try:
        parts = any_that_can_be_ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit():
                return False
            number = int(part)
            if number < 0 or number > 255:
                return False
        return True
    except Exception as e:
        print("FAIL validate IP", e)
        return False


def validate_digit(value: any, min_value: int, max_value: int) -> bool:
    if isinstance(value, (int, float)):
        if min_value < value < max_value:
            return True
        else:
            return False
    else:
        return False


