"""Spec 003 Phase 4: source-preserving offline diagram specimen contract."""
from __future__ import annotations
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from render_design_system_sample import generate, extract_inventory, validate_fixture
from resolve_repo_style import resolve_repo_style
from verify_design_system import TokenError

class Tags(HTMLParser):
    def __init__(self):
        super().__init__(); self.nodes=[];self.edges=[];self.text=[];self.tags=[];self.attrs=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);self.tags.append(tag);self.attrs.append((tag,a))
        if 'data-node-id' in a:self.nodes.append((a['data-node-id'],a.get('data-kind'),a.get('data-status')))
        if 'data-edge-id' in a:self.edges.append((a['data-edge-id'],a.get('data-source'),a.get('data-target'),a.get('d')))
    def handle_data(self,data):self.text.append(data)

class Diagrams(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture=json.loads((ROOT/'tests/fixtures/design-system/semantic-sample.json').read_text(encoding='utf-8'))
    def test_source_inventory_and_no_invented_relations(self):
        sample=self.fixture
        validate_fixture(sample)
        self.assertEqual(len(sample['nodes']),5)
        self.assertEqual(len(sample['edges']),2)
        self.assertEqual(next(n for n in sample['nodes'] if n['kind']=='gate-result')['value'],'warn')
        self.assertEqual(next(n for n in sample['nodes'] if n['kind']=='decision')['value'],'REPEAT')
        self.assertNotIn(('gate-result','decision-selected'),[(e['source'],e['target']) for e in sample['edges']])
        for theme in ('light','dark'):
            with self.subTest(theme=theme):
                txt=generate(root=ROOT,theme=theme)
                doc=Tags();doc.feed(txt)
                self.assertEqual({n[0] for n in doc.nodes},{n['id'] for n in sample['nodes']})
                self.assertEqual([(e[0],e[1],e[2]) for e in doc.edges],[(e['id'],e['source'],e['target']) for e in sample['edges']])
                self.assertTrue(all(' H ' in e[3] and ' V ' in e[3] for e in doc.edges))
                full=' '.join(doc.text)
                for n in sample['nodes']:
                    self.assertIn(n['label'],full)
                    self.assertIn(n['visual_state']['label'],full)
                    self.assertIn(n['visible_type'],full)
                for e in sample['edges']:
                    self.assertIn(e['label'],full)
                self.assertIn('planned truth',full)
                self.assertNotIn('<script',txt.lower())
                self.assertIn('prefers-reduced-motion',txt)
                self.assertNotIn('http://',txt.replace('http://www.w3.org/2000/svg',''))
                self.assertNotIn('https://',txt)
    def test_accessibility_title_desc_nav_and_focus(self):
        txt=generate(root=ROOT)
        parsed=Tags();parsed.feed(txt)
        self.assertIn(('svg',{'class':'ppmax-design-system','viewbox':'0 0 1140 680','role':'img','aria-labelledby':'ppmax-specimen-title ppmax-specimen-desc','xmlns':'http://www.w3.org/2000/svg'}),parsed.attrs)
        ids={a['id'] for _,a in parsed.attrs if 'id' in a}
        self.assertIn('ppmax-specimen-title',ids)
        self.assertIn('ppmax-specimen-desc',ids)
        self.assertIn('tabindex="0"',txt)
        self.assertIn(':focus-visible',txt)
        self.assertIn('aria-describedby="diagram-hint"',txt)
        self.assertIn('../../../docs/diagrams/index.html',txt)
        self.assertIn('../../../specs/003-product-pro-max-design-system/diagrams.html',txt)
    def test_invalid_semantic_input_fails_closed(self):
        for mutation in ('inferred-edge','unknown-node','bad-state','duplicate-id'):
            data=copy.deepcopy(self.fixture)
            if mutation=='inferred-edge':data['edges'].append(dict(id='invented',source='gate-result',target='decision-selected',label='implied'))
            if mutation=='unknown-node':data['edges'][0]['target']='not-present'
            if mutation=='bad-state':data['nodes'][0]['visual_state']['role']='pass'
            if mutation=='duplicate-id':data['nodes'][1]['id']=data['nodes'][0]['id']
            with self.subTest(mutation=mutation), self.assertRaises(TokenError):
                generate(root=ROOT,sample=data)
    def test_theme_and_density_do_not_modify_source(self):
        original=extract_inventory(self.fixture)
        for t in ('light','dark'):
            for d in ('compact','default','spacious'):
                self.assertIn(f'data-theme="{t}"',generate(ROOT,theme=t,density=d))
                self.assertEqual(extract_inventory(self.fixture),original)
    def test_committed_html_snapshots_are_exact_and_readonly(self):
        for theme in ('light','dark'):
            f=ROOT/f'tests/fixtures/design-system/specimen-{theme}.html'
            original=f.read_bytes()
            proc=subprocess.run([sys.executable,str(ROOT/'scripts/render_design_system_sample.py'),'--theme',theme,'--output',str(f),'--check'],capture_output=True,text=True)
            self.assertEqual(proc.returncode,0,proc.stderr)
            self.assertEqual(f.read_bytes(),original)
            with tempfile.TemporaryDirectory() as tmp:
                bad=Path(tmp)/'out.html';bad.write_text('tampered',encoding='utf-8')
                proc=subprocess.run([sys.executable,str(ROOT/'scripts/render_design_system_sample.py'),'--theme',theme,'--output',str(bad),'--check'],capture_output=True,text=True)
                self.assertNotEqual(proc.returncode,0)
                self.assertEqual(bad.read_text(encoding='utf-8'),'tampered')
    def test_home_profiles_do_not_override_tokens(self):
        import os
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            fake=Path(tmp)/'.diagram-design/profiles';fake.mkdir(parents=True)
            (fake/'unrelated.md').write_text('paper:#ffffff\naccent:#ff00ff',encoding='utf-8')
            with patch.dict(os.environ,{'HOME':tmp,'USERPROFILE':tmp}):
                self.assertIn('--ppmax-accent-brand: #A3FF47',generate(root=ROOT,theme='light'))
            self.assertEqual((fake/'unrelated.md').read_text(encoding='utf-8'),'paper:#ffffff\naccent:#ff00ff')

    def test_repo_specific_adapter_overrides_foreign_home(self):
        import os
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            home=Path(tmp)
            profile=home/'.diagram-design/profiles/fake.md'
            profile.parent.mkdir(parents=True)
            profile.write_text('accent: #FF00FF',encoding='utf-8')
            with patch.dict(os.environ,{'HOME':tmp,'USERPROFILE':tmp}):
                result=resolve_repo_style(ROOT,theme='light')
            self.assertEqual(result['roles']['accent'],'#A3FF47')
            self.assertEqual(result['roles']['paper'],'#F7F9F4')
            self.assertEqual(profile.read_text(encoding='utf-8'),'accent: #FF00FF')
            with self.assertRaisesRegex(TokenError,'repository-local tokens required'):
                resolve_repo_style(home,theme='light')

if __name__=='__main__':unittest.main()
