GDAX Prometheus Exporter
===

Exposes GDAX data on the exposition api

# Setup

```bash
pip install -r requirements.tx
```

# Run it

```bash
python gdax_exporter.py
```

# View it

Navigate to http://localhost:8000

# Run it with docker

```bash
docker run -p 8000:8000 parabuzzle/gdax_prometheus_exporter:latest
```