{{THEMES}}
body{font-family:var(--ppmax-font-ui,system-ui),system-ui,sans-serif;background:var(--ppmax-surface);color:var(--ppmax-text-primary);margin:0;padding:28px}
main{max-width:1100px;margin:auto}
nav{display:flex;flex-wrap:wrap;gap:16px;font-size:14px;margin-bottom:22px}
a{color:var(--ppmax-link)} a:focus-visible{outline:3px solid var(--ppmax-focus-ring);outline-offset:4px;border-radius:3px}
h1{font-size:28px;line-height:1.18}
p,footer{color:var(--ppmax-text-secondary);line-height:1.5}
svg{display:block;width:100%;height:auto;background:var(--ppmax-node-fill);border:1px solid var(--ppmax-border-strong);border-radius:10px;overflow:visible}
svg text{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;fill:var(--ppmax-text-primary)}
svg .node{fill:var(--ppmax-node-fill);stroke:var(--ppmax-node-outline);stroke-width:2}
svg .focus{fill:var(--ppmax-surface-elevated);stroke:var(--ppmax-edge-emphasis);stroke-width:2.5}
svg .edge{stroke:var(--ppmax-edge);stroke-width:2;fill:none;marker-end:url(#arr)}
svg #arr path{fill:var(--ppmax-edge)}
svg .small{font-size:14px;fill:var(--ppmax-label-muted)}
svg .head{font-size:18px;font-weight:650}
svg .label{font-size:15px;font-weight:600}
@media(max-width:600px){body{padding:16px}nav{gap:10px}main{min-width:0}svg{min-width:820px}main{overflow-x:auto;scrollbar-gutter:stable}h1{font-size:23px}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}
