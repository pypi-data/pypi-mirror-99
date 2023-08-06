class Context:
    def __init__(self, manager, pane, parent, **ctx_vars):
        self.manager = manager
        self.pane_getter = pane
        self.parent = parent
        self.ctx_vars = ctx_vars
        self.previous = None

    @property
    def lineage(self):
        return f'{self.parent.lineage}.{self.name}' if self.parent else self.name

    def __call__(self):
        raise NotImplemented

    @property
    def pane(self):
        return self.pane_getter()

    def run(self, cmd, echo=False):
        msg = f' > {cmd}' if echo else None
        self.pane.run(cmd, self.prompt, head=msg)

    def enter(self):
        current = self.manager.current
        print(f' + {self.name}')
        self()
        self.previous = current
        self.manager.current = self

    def exit_cmd(self):
        self.pane.send_keys('C-d')

    def wait_cmd(self, what):
        self.pane.wait(what)

    def exit(self):
        print(f' - {self.name}')
        self.exit_cmd()
        if self.previous:
            self.wait_cmd(self.previous.prompt)
            self.manager.current = self.previous

    def __str__(self):
        return self.lineage


class Manager:
    def __init__(self, pane_getter, ctxs, **kw):
        cdict = {}
        for ctx in ctxs:
            cdict[ctx.name] = ctx(
                self,
                pane_getter,
                cdict.get(ctx.parent),
                **kw
            )
        self.contexts = cdict
        self.current = None

    def enter(self, target):
        last = self.current

        target = self.contexts[target]
        targets = target.lineage.split('.')

        while self.current and self.current.name not in targets:
            self.current.exit()

        for name in targets:
            names = self.current.lineage.split('.') if self.current else []
            if name not in names:
                ctx = self.contexts[name]
                ctx.enter()

        if self.current != last:
            print(f' = {self.current}')

    def exit(self, target=None):
        last = self.current

        if not target:
            target = self.current.previous.name

        while self.current.name!=target:
            self.current.exit()
            if not self.current.parent:
                self.current.exit()
                break

        if self.current != last:
            print(f' = {self.current}')

