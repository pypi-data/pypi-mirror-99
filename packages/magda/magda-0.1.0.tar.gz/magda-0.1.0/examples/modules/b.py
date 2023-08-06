from time import sleep

from magda.module import Module
from magda.decorators import register, accept, finalize, produce

from examples.modules.common import logger, log
from examples.interfaces.common import Context
from examples.interfaces.fn import LambdaInterface


@accept(LambdaInterface)
@produce(LambdaInterface)
@register('B')
@finalize
class ModuleB(Module.Runtime):
    SLEEP_TIME = 1

    def bootstrap(self):
        ctx: Context = self.context
        log(self, ctx.timer, '--- Created!')

    def teardown(self):
        ctx: Context = self.context
        log(self, ctx.timer, '--- Teardown!')

    @logger
    def run(self, data: Module.ResultSet, *args, **kwargs):
        # Access strings (results) from the previous modules
        src = [text.fn() for text in data.of(LambdaInterface)]

        # Add delay for example purposes
        sleep(self.SLEEP_TIME)

        # Build output string and produce declared interface
        msg = '(' + ' + '.join(src) + (' = ' if len(src) else '') + f'{self.name})'
        return LambdaInterface(lambda: msg)
