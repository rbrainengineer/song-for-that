class approx_key_dict(dict):

    def __setitem__(self, key, value):
        super(approx_key_dict, self).__setitem__(float(key), value)

    def __getitem__(self, key):
        if key in self:
            min_set = super(approx_key_dict, self).__getitem__(float(key))
            return min_set
        else:
            key = float(key)
            min_dst = None
            min_set = []
            for k, v in self.items():
                dst = abs(k - key)
                if dst < min_dst or min_dst is None:
                    min_dst = dst
                    #print k, str(v)
                    min_set = v
                elif dst == min_dst:
                    min_set = min_set.extend(v)
            return min_set
