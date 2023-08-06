import pathlib
import re

from aiohttp import web

class AiohttpOpenAPI():

    def setup_openapi(self, app, path_prefix='', yaml_path=None):
        self.path_prefix = path_prefix if path_prefix[-1] != '/' else path_prefix[:-1]
        self._YAML_DATA = ''

        self._load_yml(yaml_path)
        self._travers_endpoints(app)

        swagger_ui_path = pathlib.Path(__file__).parent / 'dist'
        app.router.add_static('/dist', swagger_ui_path, show_index=True)

        app.router.add_get('/docs', self.redirect_to_index)
        app.router.add_get('/swagger', self.stream_yaml)


    async def redirect_to_index(self, request):
        path = request.path.replace('docs', 'dist/index.html')
        return web.HTTPFound(path)


    async def stream_yaml(self, request):
        stream = web.StreamResponse()
        await stream.prepare(request)
        await stream.write(self._YAML_DATA.encode())
        await stream.write_eof()
        return stream


    def _travers_endpoints(self, app) -> None:
        d_tree = {}
        for route in app.router.routes():
            method = route.method.lower()
            if method == 'head':
                continue
            endpoint = route.resource.canonical

            if route.handler.__doc__ and '---' in route.handler.__doc__:
                try:
                    docstr = route.handler.__doc__.splitlines()
                except AttributeError:
                    return None
                opanapi_docstr, is_skip_verify = self._extract_openapi_docstr(docstr)
                endpoint_, method_ = self._get_path_method(opanapi_docstr)
                if not is_skip_verify and (method != method_ or endpoint != endpoint_):
                    assert False, f'docstr does not match handler definition ({method} {endpoint} != {method_} {endpoint_})'

                path_wiht_prefix = f'{self.path_prefix}{endpoint_}'
                if d_tree.get(path_wiht_prefix) is None:
                    d_tree[path_wiht_prefix] = {}
                d_tree[path_wiht_prefix][method_] = self._remove_endpoint_and_method(opanapi_docstr)

        # join dict to a single file
        for endpoint in d_tree:
            if len(d_tree[endpoint]) > 0:
                self._YAML_DATA += f'    {endpoint}:'
                for method in d_tree[endpoint]:
                    self._YAML_DATA += f'\n        {method}:'
                    docstr = d_tree[endpoint][method]
                    self._YAML_DATA += docstr


    def _load_yml(self, yaml_path) -> None:
        """
        Load global yaml file if one exist.
        :param yaml_path:
        :return: None
        """
        with open(yaml_path, 'r') as yaml_file:
            data = yaml_file.read()
            self._YAML_DATA += data
        if 'paths' not in self._YAML_DATA:
            self._YAML_DATA += 'paths:\n'


    def _get_path_method(self, docstr: str):
        """
        Check if first two lines of the docstr matches with a handler's endpoint & method.
        :param endpoint:
        :param method:
        :param docstr:
        :return:
        """
        # TODO: do not hard code tab's spaces size
        first_line: str = r'\s{4}(\S*):\s'  # 4 white spaces ENDPOINT: newline
        second_line: str = r'\s{8}(\S*):\s'  # 8 white spaces METHOD: newline
        pattern: str = first_line + second_line
        result = re.findall(pattern, docstr)
        if len(result[0]) != 2 or result[0][1] not in ("post", "get", "delete", "put", "patch", "option"):
            print("GRESKA", len(result), docstr)
        return result[0]


    def _remove_endpoint_and_method(self, docstr: str) -> str:
        second_new_line = self._find_nth(docstr, '\n', 2)
        return docstr[second_new_line:]


    def _extract_openapi_docstr(self, endpoint_doc):
        # Find Swagger start point in doc
        endpoint_swagger_start = 0
        is_skip_verify = False
        for i, doc_line in enumerate(endpoint_doc):
            if '---' in doc_line:
                endpoint_swagger_start = i + 1
                is_skip_verify = "aiohtt-openapi: skip-verify" in doc_line
                break

        out = '\n'.join(endpoint_doc[endpoint_swagger_start:-1])
        out += '\n'
        return out, is_skip_verify


    def _find_nth(self, haystack, needle, n):
        start = haystack.find(needle)
        while start >= 0 and n > 1:
            start = haystack.find(needle, start+len(needle))
            n -= 1
        return start
