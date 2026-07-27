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
