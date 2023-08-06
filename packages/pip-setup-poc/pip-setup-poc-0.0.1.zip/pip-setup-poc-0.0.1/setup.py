__import__('os').chdir(__import__('tempfile').gettempdir())
with open('pip-setup-poc.executed_at=%d' % (int(__import__('time').time()),), 'w'): pass
