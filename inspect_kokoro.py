import sys
print('python_executable:', sys.executable)
print('python_version:', sys.version)
try:
    import kokoro
    import pkgutil
    print('kokoro_version:', kokoro.__version__)
    print('kokoro_file:', kokoro.__file__)
    print('kokoro_path:', kokoro.__path__)
    print('kokoro_modules:', [m.name for m in pkgutil.iter_modules(kokoro.__path__)])
    print('kokoro_dir_tts:', [x for x in dir(kokoro) if 'tts' in x.lower() or 'voice' in x.lower()])
except Exception as e:
    print('kokoro_import_error:', repr(e))
