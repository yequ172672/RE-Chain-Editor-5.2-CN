"""Export UI regression: execute real invoke without loading Blender."""
import ast
from pathlib import Path
from types import SimpleNamespace as NS
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ExportOptionsTests(unittest.TestCase):
    def test_owots_option_and_automatic_filename(self):
        tree = ast.parse((ROOT / '__init__.py').read_text(encoding='utf-8-sig'))
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'ExportREChain2')
        field = next(n for n in cls.body if isinstance(n, ast.AnnAssign) and n.target.id == 'filename_ext')
        items = ast.literal_eval(next(k.value for k in field.annotation.keywords if k.arg == 'items'))
        self.assertTrue(any(x[0] == '.17' and 'Onimusha' in x[1] for x in items))
        invoke = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == 'invoke')
        ns = {}
        for n in tree.body:
            if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ('supportedChainVersions','supportedChain2Versions') for t in n.targets):
                exec(compile(ast.Module(body=[n], type_ignores=[]), '<versions>', 'exec'), ns)
        for version, expected in [(17,17),(15,15),(12,14),(13,14)]:
            collection = NS(name='body.chain2', get=lambda key, default: default)
            scene = type('Scene', (dict,), {})({'REChainLastImportedChain2Version': version})
            scene.re_chain_toolpanel = NS(chainCollection=collection)
            context = NS(scene=scene, window_manager=NS(fileselect_add=lambda op: None))
            ns['bpy'] = NS(data=NS(collections={}), context=context)
            exec(compile(ast.Module(body=[invoke], type_ignores=[]), '<invoke>', 'exec'), ns)
            op = NS(targetCollection='', filename_ext='.14', filepath='')
            ns['invoke'](op, context, None)
            self.assertEqual(op.filename_ext, '.' + str(expected))
            self.assertEqual(op.filepath, 'body.chain2.' + str(expected))

if __name__ == '__main__': unittest.main()
