#!/bin/bash

REQ_FILES=(
  "/app/config/requirements/base"
  "/app/config/requirements/dev"
)

for f in "${REQ_FILES[@]}"; do
  pip-compile --generate-hashes --resolver=backtracking -o ${f}.txt ${f}.in || exit 1;
done
