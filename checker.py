def check(haiku, tokens):
    for s in tokens:
        if s not in haiku:
            return False
    return True

