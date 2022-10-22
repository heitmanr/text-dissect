import regex

# tail-trigger
# ...line1
# ...line2
# ...line3 > Trigger (store)
#
# !tail = head-trigger
# ...line1 > Trigger (ignore 1st trigger)
# ...line2
# ...line3
# ...line4 > Trigger (store lines1..3)
# ...line5
# ...line6
# EOF => store line 4..6    - done when "get()" is called to retrieve captured sections
    
    
class InfoSection():
    
    def __init__(self, re_trigger, re_ignore="", tail=False):
        self.sections = []
        self.re_trigger = re_trigger
        self.re_ignore = re_ignore
        self.mode_tail = tail    #todo: "head"-matching algorithm
        self.stack = []
       
    #
    # ignore empty sections
    #
    def __store_stack(self):
 
        if len(self.stack)>0:
            self.sections.append(self.stack)
            self.stack = []
    #
    # process line - parse it
    # - ignore
    # - trigger => process section
    #
    def add_line(self, l):
        if regex.search(self.re_ignore, l):
            return
          
        rs_trigger = regex.search(self.re_trigger, l)
        if rs_trigger:
            #print("TRIGGER=>",l)
            #
            # tail-trigger? => add trigger-line as last-line to infos
            if self.mode_tail:
                self.stack.append(l)
            #
            self.__store_stack()
            #
            # head-trigger? => add trigger-line as first-line to infos
            if not self.mode_tail:
                self.stack.append(l)
        else:
            self.stack.append(l)
            
    def add_txt_file(self, filename, encoding="utf-8"):

        with open(filename, encoding=encoding) as file:
            for l in file:
                self.add_line(l.rstrip('\n'))
            
        
    # tail-trigger? don't store last section since there was no trigger event
    # head-trigger? store section captured so far
    #
    def close(self):
        if not self.mode_tail:
            self.__store_stack()
        
    #
    # todo: implicit expectation, that "get" is called when all lines are processed, so "close" might be useful
    #
    def get(self):
        self.close()
        return(self.sections)
        

def get_info_section_from_txt_file(filename, trigger, re_ignore, tail, encoding="utf-8"):

    info = InfoSection(trigger, re_ignore, tail=tail)
    #
    info.add_txt_file(filename, encoding=encoding)
            
    return info.get()
