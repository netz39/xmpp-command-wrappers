

class Command(object):
    """Parse and Generate new Commands for the xmpp-communication protocoll"""
    def __init__(self, c=None):
        self.c = c
        self.params = []
        if(c):
            self.parse(c)

    def toString(self):
        """convert command to string"""
#        if self.c:
#            return self.c
        s = "%s" %self.command
        for param in self.params:
            s = s + "\n%s "%len(param['values']) + param['name'] + "\n%s" % "\n".join(param['values'])
        return s

    def parse(self, s):
        """ parse command from string """
        lines = s.split("\n")
        self.command = lines.pop(0)
        while(len(lines) > 0):
            current = lines.pop(0).split(" ")
            num_lines = int(current[0])
            self.params.append({"name" : current[1], "values" : []})
            for i in range(0, num_lines):
                param = lines.pop(0)
                self.params[-1]['values'].append(param)

    def get_prefix(self):
        split = self.command.split(".")
        if(len(split) < 2)
            return None
        return split[0]

if __name__ == '__main__':
    a = Command(c="ic2.read16\n1 device\n0x22\n1 register\n0x95")
    print a.command
    print "====="
    print a.params

    print a.toString()

    hw = Command(c="helloworld\n1 subject\nhallo welt!\n3 body\nHallo Welt,\nich kann auch\nZeilenumbrueche!")
    print hw.command
    print "====="
    print hw.params

    print hw.toString()
