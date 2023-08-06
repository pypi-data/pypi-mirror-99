# Uptrace for Python

![build workflow](https://github.com/uptrace/uptrace-python/actions/workflows/build.yml/badge.svg)
[![Documentation](https://img.shields.io/badge/uptrace-documentation-informational)](https://docs.uptrace.dev/python/)

<a href="https://docs.uptrace.dev/python/">
  <img src="https://docs.uptrace.dev/devicons/python-original.svg" height="200px" />
</a>

## Installation

## Introduction

uptrace-python is an OpenTelemery distribution configured to export
[traces](https://docs.uptrace.dev/tracing/#spans) to Uptrace.

## Quickstart

Install uptrace-python:

```bash
pip install uptrace
```

Run the [basic example](example/basic) below using the DSN from the Uptrace project settings page.

```python
#!/usr/bin/env python3

import uptrace
from opentelemetry import trace

# Set dsn or UPTRACE_DSN env var.
uptrace.configure_opentelemetry(
    dsn="", service_name="myservice", service_version="1.0.0"
)
tracer = trace.get_tracer("app_or_package_name", "1.0.0")

with tracer.start_as_current_span("main") as span:
    with tracer.start_as_current_span("child1") as span:
        span.set_attribute("key1", "value1")
        span.record_exception(ValueError("error1"))

    with tracer.start_as_current_span("child2") as span:
        span.set_attribute("key2", "value2")
        span.set_attribute("key3", 123.456)

    print("trace:", uptrace.trace_url(span))

# Send buffered spans.
trace.get_tracer_provider().shutdown()
```

Please see [uptrace-python documentation](https://docs.uptrace.dev/python/) for more details.
