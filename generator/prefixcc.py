import requests


class PrefixCCMap:
    """ Map from namespace to URI from Prefix.cc """
    def __init__(self):
        resp = requests.get("https://prefix.cc/context")
        if resp.ok:
            map = resp.json()['@context']
            for k, v in map.items():
                setattr(self, k, v)
        print(f"{len(map.keys())} prefixes loaded from prefix.cc")

    def __contains__(self, item):
        return hasattr(self, item.lower())

    def __getitem__(self, item):
        return getattr(self, item.lower())


# x = PrefixCCMap()
# for e in generate:
#     pfx = e.pfx.lower()
#     if pfx not in x:
#         print(f"Can't find {e.pfx}")
#     elif e.uri and e.uri != x[pfx]:
#         print(f"URI Mismatch: prefix.cc={x[pfx]}, table={e.uri}")