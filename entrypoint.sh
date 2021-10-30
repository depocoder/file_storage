#!/bin/bash

echo "Starting server"
uvicorn server:app --reload