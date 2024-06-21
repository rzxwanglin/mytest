class JsonHandle:
    @classmethod
    def helper_list(cls, key, li):
        for values in li:
            if isinstance(values, dict):
                val = cls.helper_dict(key, values)
                if val != None:
                    return val
            elif isinstance(values, list):
                val = cls.helper_list(key, values)
                if val != None:
                    return val

    @classmethod
    def helper_dict(cls, key, dic):
        for keys, values in dic.items():
            if key == keys:
                return values
            elif isinstance(values, dict):
                val = cls.helper_dict(key, values)
                if val != None:
                    return val
            elif isinstance(values, list):
                val = cls.helper_list(key, values)
                if val != None:
                    return val