import random


def get_promo_code(num_chars=8) -> str:
    code_chars = '123456789ABCDEFGHIJKLMNPQRSTUVWXYZ'
    code = ''
    for i in range(0, num_chars):
        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start: slice_start + 1]
    return code
