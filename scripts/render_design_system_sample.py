#!/usr/bin/env python3
"""Render only the committed Spec 003 test fixture; not a general diagram engine."""
from __future__ import annotations
import argparse
import html
import json
from pathlib import Path
from export_design_tokens import render as render_css
from verify_design_system import ROOT, TokenError, load_tokens, resolve, resolve_visual_state

FIXTURE = Path('tests/fixtures/design-system/semantic-sample.json')
# Editorial layout for this exact test sample. It is not a second ontology.
RECTS = {
    'evidence-input': (60, 96, 300, 164),
    'gate-result': (438, 96, 310, 164),
    'decision-selected': (438, 400, 310, 164),
    'next-step': (808, 400, 278, 164),
    'evidence-gap': (60, 400, 300, 164),
}
SEMANTIC_KINDS = {'evidence', 'gate-result', 'decision', 'activity'}

def extract_inventory(sample: dict) -> dict:
    return {
        'nodes': [(n['id'], n['kind'], n['visible_type'], n['label'], n.get('value'), n['visual_state']['role'], n['visual_state']['label']) for n in sample['nodes']],
        'edges': [(e['id'], e['source'], e['target'], e['label']) for e in sample['edges']],
        'provenance': sample['provenance'],
    }

def validate_fixture(sample: dict) -> None:
    if sample['provenance']['scope'] != 'feature' or sample['provenance']['truth'] != 'planned':
        raise TokenError('only planned test fixture supported')
    names = [n['id'] for n in sample['nodes']]
    if len(names) != len(set(names)) or set(names) != set(RECTS):
        raise TokenError('missing, duplicate or invented node')
    edgeids=set()
    for n in sample['nodes']:
        if n['kind'] not in SEMANTIC_KINDS: raise TokenError('unsupported source node kind')
        if not all(isinstance(n[k],str) and n[k].strip() for k in ('id','visible_type','label')): raise TokenError('missing source node label')
        state=n['visual_state']
        if state['role'] not in {'success','warning','danger','neutral'} or not isinstance(state['label'],str) or not state['label'].strip(): raise TokenError('invalid source visual state')
    for edge in sample['edges']:
        if edge['id'] in edgeids or edge['source'] not in names or edge['target'] not in names: raise TokenError('unknown or duplicated source edge')
        if not isinstance(edge['label'],str) or not edge['label'].strip(): raise TokenError('missing source edge label')
        edgeids.add(edge['id'])
    if any(e['source']=='gate-result' and e['target']=='decision-selected' for e in sample['edges']): raise TokenError('no inferred Gate-to-Decision edge')


def orthogonal_points(source: tuple, target: tuple) -> str:
    x,y,w,h=source; tx,ty,tw,th=target
    if x+w < tx:
        sx,sy=x+w,y+h/2; ex,ey=tx,ty+th/2
        mid=(sx+ex)/2
        return f'M {sx:g} {sy:g} H {mid:g} V {ey:g} H {ex:g}'
    raise TokenError('sample only supports explicitly defined left-to-right edges')


def generate(root: Path = ROOT, theme: str='light', density: str='default', sample: dict|None=None) -> str:
    data=load_tokens(root)
    selected,palette,_=resolve(data, 'diagram', theme, density)
    if sample is None:
        sample=json.loads((root/FIXTURE).read_text(encoding='utf-8'))
    validate_fixture(sample)
    css=render_css(data,surface='diagram',theme=selected,density=density)
    h=html.escape
    paths=[]
    for e in sample['edges']:
        p=orthogonal_points(RECTS[e['source']],RECTS[e['target']])
        # Long connector labels sit in the canvas gutter ABOVE nodes. Text must
        # not be painted beneath a later node or truncated by its fill.
        sx,sy,sw,_=RECTS[e['source']]
        tx,ty,_,_=RECTS[e['target']]
        lx=(sx+sw+tx)/2
        paths.append(f'<path class="ppmax-edge" data-edge-id="{h(e["id"])}" data-source="{h(e["source"])}" data-target="{h(e["target"])}" d="{p}" marker-end="url(#ppmax-arrow)"/>')
        paths.append(f'<text class="edge-label" x="{lx:g}" y="{ty-18:g}" text-anchor="middle">{h(e["label"])}</text>')
    nodes=[]
    for n in sample['nodes']:
        x,y,w,height=RECTS[n['id']]
        role=n['visual_state']['role']; label=n['visual_state']['label']
        color=resolve_visual_state(data,selected,role,label)
        kind=n['kind']
        accent_role={'evidence':'evidence-emphasis','gate-result':'gate-result-emphasis','decision':'decision-emphasis','activity':'edge-emphasis'}[kind]
        # status shape uses explicit semantic kind. Color and type label redundant.
        symbol={'success':'✓','warning':'!','danger':'×','neutral':'•'}[role]
        nodes.append(f'<g class="semantic-node" data-node-id="{h(n["id"])}" data-kind="{h(kind)}" data-status="{h(role)}">'
                     f'<rect class="node-box" x="{x}" y="{y}" width="{w}" height="{height}" rx="12"/>'
                     f'<rect x="{x}" y="{y}" width="5" height="{height}" rx="2" fill="var(--ppmax-{accent_role})"/>'
                     f'<text class="kind-label" x="{x+20}" y="{y+32}">{h(n["visible_type"])}</text>'
                     f'<text class="node-title" x="{x+20}" y="{y+70}">{h(n["label"])}</text>'
                     + (f'<text class="node-value" x="{x+20}" y="{y+99}">{h(n["value"])}</text>' if n.get('value') else '')
                     + f'<text class="status-label" x="{x+20}" y="{y+136}" fill="{color}">{h(symbol)}  {h(label)}</text></g>')
    provenance=sample['provenance']; content='\n'.join([*paths,*nodes]);
    return f'''<!doctype html>
<html lang="vi" data-theme="{h(selected)}" data-density="{h(density)}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Spec 003 · Signal Protocol specimen · {h(selected)}</title>
<style>
{css}
*{{box-sizing:border-box}}html{{color-scheme:{selected};font-family:var(--ppmax-font-ui)}}body{{background:var(--ppmax-surface);color:var(--ppmax-text-primary);margin:0;padding:clamp(14px,4vw,36px)}}
main{{max-width:1216px;margin:auto}}nav{{display:flex;gap:18px;flex-wrap:wrap;margin-bottom:24px}}a{{color:var(--ppmax-link)}}a:focus-visible,.diagram-region:focus-visible{{outline:3px solid var(--ppmax-focus-ring);outline-offset:4px}}h1{{font-size:clamp(22px,3vw,32px)}}p,footer{{color:var(--ppmax-text-secondary);line-height:1.5}}.diagram-region{{overflow-x:auto;border:2px solid var(--ppmax-border-strong);border-radius:var(--ppmax-radius-large);background:var(--ppmax-surface-elevated);scrollbar-width:auto}}svg{{display:block;width:100%;min-width:840px;height:auto}}.node-box{{fill:var(--ppmax-node-fill);stroke:var(--ppmax-node-outline);stroke-width:2}}.ppmax-edge{{fill:none;stroke:var(--ppmax-edge);stroke-width:2.5}}.kind-label{{font-size:16px;font-weight:650;fill:var(--ppmax-text-primary)}}.node-title{{font-size:18px;fill:var(--ppmax-text-primary)}}.node-value{{font-size:16px;font-weight:bold;fill:var(--ppmax-text-primary)}}.status-label{{font-size:15px;font-weight:650}}.edge-label{{font-size:14px;fill:var(--ppmax-text-secondary);paint-order:stroke;stroke:var(--ppmax-surface-elevated);stroke-width:8px;stroke-linejoin:round}}@media(max-width:700px){{nav{{gap:14px}}svg{{min-width:1120px}}}}@media(prefers-reduced-motion:reduce){{*,*::before,*::after{{animation:none!important;transition:none!important;scroll-behavior:auto!important}}}}@media print{{.diagram-region{{overflow:visible}}}}
</style></head>
<body><main><nav aria-label="Điều hướng"><a href="../../../docs/diagrams/index.html">Diagram Atlas</a><a href="../../../specs/003-product-pro-max-design-system/diagrams.html">Feature Ledger</a></nav>
<h1>Signal Protocol · specimen ({h(selected)})</h1><p>Test fixture · <strong>planned truth</strong> · Source: <code>{h(provenance['path'])}</code>. Sample illustration; Gate result is independent of Decision.</p>
<p id="diagram-hint">Có thể dùng Tab để chọn vùng sơ đồ, sau đó dùng phím mũi tên để cuộn ngang trên màn hình hẹp.</p>
<div class="diagram-region" tabindex="0" role="region" aria-label="Sơ đồ thử nghiệm về bằng chứng, Gate result và Decision" aria-describedby="diagram-hint">
<svg class="ppmax-design-system" viewBox="0 0 1140 680" role="img" aria-labelledby="ppmax-specimen-title ppmax-specimen-desc" xmlns="http://www.w3.org/2000/svg"><title id="ppmax-specimen-title">Bằng chứng, Gate result và Decision</title><desc id="ppmax-specimen-desc">Sơ đồ planned test fixture; kết quả Gate warn không tự quyết định REPEAT. Hai cạnh nguồn được giữ nguyên hướng.</desc><defs><marker id="ppmax-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="var(--ppmax-edge)"/></marker></defs>
{content}
</svg></div><footer><p>Visual preview only · Token revision: {h(data['revision'])} · Source: {h(provenance['path'])} · No inferred semantics.</p></footer></main></body></html>
'''


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=ROOT)
    p.add_argument('--theme',choices=['light','dark'],default='light')
    p.add_argument('--density',choices=['compact','default','spacious'],default='default')
    p.add_argument('--output',type=Path)
    p.add_argument('--check',action='store_true')
    args=p.parse_args()
    try:
        page=generate(root=args.root,theme=args.theme,density=args.density)
        if args.output:
            if args.check:
                if not args.output.exists() or args.output.read_text(encoding='utf-8')!=page:
                    raise TokenError('sample output drift or missing; --check is read only')
                print('PASS: specimen exact, no-write check')
            else:
                args.output.parent.mkdir(parents=True,exist_ok=True)
                args.output.write_text(page,encoding='utf-8')
                print(f'EXPORTED: {args.output}')
        elif args.check:
            print('PASS: generated valid specimen without writing')
        else:
            print(page,end='')
    except (TokenError,AssertionError,ValueError,KeyError,OSError) as exc:
        p.exit(1,f'FAIL: {exc}\n')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
