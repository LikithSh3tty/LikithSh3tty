<div align="center">

<h3><code>likith@github ~ $ ./contributions.sh</code></h3>

<img src="./contrib-heatmap.svg?v=5" width="860" alt="Contribution heatmap" />

<br><br>

<h3><code>likith@github ~ $ whoami</code></h3>

<table>
  <tr>
    <td valign="top"><img src="./ascii-portrait.svg?v=5" width="370" alt="ASCII portrait" /></td>
    <td valign="top"><img src="./info-card.svg?v=5" width="490" alt="Info card" /></td>
  </tr>
</table>

</div>

### `likith@github ~ $ cat about.md`

I build complete products rather than notebooks. Most of what I ship is some
combination of an agent, a retrieval system, and a web app sitting in front of
both.

The thread running through all of it is systems that know their own limits.
[CloudNest](https://github.com/LikithSh3tty/Cloudnest) refuses to answer below a
calibrated confidence threshold and hands the conversation to a human instead of
guessing. [DriftBell](https://github.com/LikithSh3tty/DriftBell) investigates a
drifting model, proposes a fix, then freezes mid-graph until someone approves it.
[Agenvo](https://github.com/LikithSh3tty/Agenvo) computes every figure in Python
and only lets the language model phrase facts it was handed, so it cannot invent
a number. [Grid0pt](https://github.com/LikithSh3tty/Grid0pt) sweeps every offset
and rotation rather than accepting the first placement that fits.

I care about the unglamorous half: the confidence gate, the fallback path, the
thing that happens when the API key is missing. All four of those run without one.

### `likith@github ~ $ tree stack/`

```
stack/
├── languages/        Python · JavaScript · TypeScript · C
├── frontend/         React · Svelte · Astro · Vite · HTML · CSS · Bootstrap
├── backend/          FastAPI · Node.js · Uvicorn · REST
├── ai/
│   ├── agents/       LangGraph · LangChain · Claude (Haiku + Sonnet)
│   ├── retrieval/    sentence-transformers · ONNX Runtime · RRF fusion
│   ├── ml/           PyTorch · TensorFlow · scikit-learn
│   └── vision/       OpenCV · Shapely
├── data/             PostgreSQL · SQLite · Firebase · Supabase · SQL
├── analysis/         NumPy · Pandas · Matplotlib
└── infra/            Vercel · Docker · n8n · GitHub Actions · Git
```

### `likith@github ~ $ ls -l projects/`

| project | what it is | built with |
| --- | --- | --- |
| [Agenvo](https://github.com/LikithSh3tty/Agenvo) | multi-tenant agency income tracker with a built-in assistant | React, Firebase, LangGraph, FastAPI |
| [CloudNest](https://github.com/LikithSh3tty/Cloudnest) | support agent with semantic retrieval and human escalation | Python, LangGraph, ONNX, Postgres, React |
| [DriftBell](https://github.com/LikithSh3tty/DriftBell) | ML drift watchman that asks before it retrains | LangGraph, n8n, FastAPI, SQLite, Docker |
| [Grid0pt](https://github.com/LikithSh3tty/Grid0pt) | grid packing optimizer for irregular polygons | Python, Shapely, OpenCV, FastAPI, React |

### `likith@github ~ $ cat .profile`

This profile is generated, not hand-written. A
[GitHub Action](.github/workflows/update-profile-art.yml) pulls my contribution
data, renders the heatmap and info card as SVG, and converts a source photo into
the ASCII portrait. The scripts live in [`scripts/`](scripts/) and are covered by
[tests](tests/).

Built with Python, Pillow and hand-rolled SVG. No third-party badge services.
