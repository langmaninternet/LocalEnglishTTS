import pkgutil
import sys
print('python:', sys.executable)
for m in pkgutil.iter_modules():
    if m.name.lower() == 'kokoro' or m.name.lower().startswith('kokoro'):
        print('found module:', m.name, m.module_finder)
try:
    import kokoro
    print('kokoro imported', kokoro.__version__)
except Exception as e:
    print('kokoro import failed', repr(e))
