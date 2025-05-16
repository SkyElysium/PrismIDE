class Binding:
    def __init__(self, master):
        self.master = master

        self.event = {'<Control-z>': '<<Undo>>',
                      '<Control-Shift-z>': '<<Redo>>',
                      '<Control-c>': '<<Copy>>',
                      '<Control-x>': '<<Cut>>',
                      '<Control-v>': '<<Paste>>'
                      }

        self.binding = {'<Control-z>': self.master.undo,
                        '<Control-Shift-z>': self.master.redo,
                        '<Control-c>': self.master.copy,
                        '<Control-x>': self.master.cut,
                        '<Control-v>': self.master.paste,
                        '<Control-a>': self.master.select_all
                        }

        self.run()

    def run(self):
        # delete event
        for key, event_name in self.event.items():
            self.master.event_delete(event_name, key)
            self.master.event_delete(event_name, key.title())

        # binding
        for key, func in self.binding.items():
            self.master.bind(key, func)
            self.master.bind(key.title(), func)