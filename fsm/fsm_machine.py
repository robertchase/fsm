from fsm.FSM import STATE, EVENT, FSM
# pylint: skip-file
# flake8: noqa
# action
# context
# default
# enter
# event
# exception
# exit
# handler
# state
def create(**actions):
  S_init=STATE('init')
  S_state=STATE('state',on_enter=actions['state'])
  S_event=STATE('event',on_enter=actions['event'])
  S_context=STATE('context',on_enter=actions['context'])
  S_handler=STATE('handler',on_enter=actions['handler'])
  S_error=STATE('error')
  S_exception=STATE('exception',on_enter=actions['exception'])
  S_default=STATE('default',on_enter=actions['default'])
  S___default__=STATE('__default__')
  S_init.set_events([EVENT('state',[], S_state),])
  S_state.set_events([EVENT('error',[], S_error),EVENT('enter',[actions['enter']]),EVENT('exit',[actions['exit']]),EVENT('event',[], S_event),EVENT('state',[], S_state),EVENT('context',[], S_context),EVENT('handler',[], S_handler),])
  S_event.set_events([EVENT('error',[], S_error),EVENT('action',[actions['action']]),EVENT('event',[], S_event),EVENT('state',[], S_state),EVENT('context',[], S_context),EVENT('handler',[], S_handler),])
  S_context.set_events([EVENT('handler',[], S_handler),])
  S_handler.set_events([EVENT('handler',[], S_handler),])
  S_error.set_events([])
  S_exception.set_events([EVENT('state',[], S_state),EVENT('context',[], S_context),EVENT('handler',[], S_handler),])
  S_default.set_events([EVENT('action',[actions['action']]),EVENT('state',[], S_state),EVENT('context',[], S_context),EVENT('handler',[], S_handler),])
  S___default__.set_events([EVENT('default',[], S_default),EVENT('exception',[], S_exception),])
  return FSM([S_init,S_state,S_event,S_context,S_handler,S_error,S_exception,S_default,S___default__])
