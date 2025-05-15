
def get_queue_name(currency_pair: str) -> str:
    parsing, target = currency_pair.rsplit('-', 1)
    "/".join([parsing, target])
    return "/".join([parsing, target])