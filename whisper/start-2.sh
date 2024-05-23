#!/bin/bash

set -ex

function ctrl_c() {
    echo "exit..."
    exit 0
}
# trap ctrl-c and call ctrl_c()
trap ctrl_c INT

# without MPI
source $(python -c "import oneccl_bindings_for_pytorch as torch_ccl;print(torch_ccl.cwd)")/env/vars.sh

# with MPI
# source $(python -c "import oneccl_bindings_for_pytorch as torch_ccl;print(torch_ccl.cwd)")/env/setvars.sh

uvicorn openaiapi-2:app --host 0.0.0.0 --port 5000
