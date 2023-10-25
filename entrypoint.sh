#!/bin/bash

uvicorn app.main:api --host 0.0.0.0 --reload --log-level=trace