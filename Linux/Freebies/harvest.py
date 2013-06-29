import DailyFreebies

if __name__ == '__main__':
    s = DailyFreebies.login()
    #print hide(s), hide(s),hide(s),hide(s)
    for f in DailyFreebies.__dict__.keys():
        if f[:3] == 'get' and f[3] != 'p':
            freebie = getattr(DailyFreebies, f)
            print f, '\t', freebie(s)

