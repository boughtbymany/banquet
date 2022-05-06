import importlib.util
import os


class BanquetHandler:
    def __init__(self, conf, path=None):
        self.handler = None
        self._base = path
        self.path = os.path.join(os.getcwd(), path)
        self.handler_path = conf.get("x-handler")

        self.load()

    def load(self):
        if self.handler_path is None:
            return

        fp = None
        source_path = os.path.join(self.path, self.handler_path, "index.py")

        if not os.path.exists(source_path):
            raise Exception(f"Handler could not be found: '{source_path}'")

        try:
            spec = importlib.util.spec_from_file_location(
                self.handler_path, source_path
            )
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        except ImportError:
            raise Exception(
                f"Unable to find handler {self.handler_path} in {self._base}"
            )
        finally:
            if fp:
                fp.close()

        self.handler = mod.handler

    def call(self, event, context):
        return self.handler(event, context)
