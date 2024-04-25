# Docker build

```
docker build \
    --build-arg https_proxy=$https_proxy \
    --build-arg http_proxy=$http_proxy \
    -f Dockerfile.vllm-xft.base \
    -t registry.cn-shanghai.aliyuncs.com/taosy/vllm-xft-base:0.01 .
```

```
docker build \
    --build-arg https_proxy=$https_proxy \
    --build-arg http_proxy=$http_proxy \
    --build-arg HF_ENDPOINT=$HF_ENDPOINT \
    --build-arg HF_TOKEN=$HF_TOKEN \
    -f Dockerfile.vllm-xft-llama2-7b \
    -t registry.cn-shanghai.aliyuncs.com/taosy/vllm-xft-llama2-7b:0.01 .
```

```
docker build \
    --build-arg https_proxy=$https_proxy \
    --build-arg http_proxy=$http_proxy \
    --build-arg HF_ENDPOINT=$HF_ENDPOINT \
    --build-arg HF_TOKEN=$HF_TOKEN \
    -f Dockerfile.vllm-xft-qwen-7b \
    -t registry.cn-shanghai.aliyuncs.com/taosy/vllm-xft-qwen-7b:0.01 .
```

# Docker run
```
docker run \
    -e https_proxy -e http_proxy \
    -e HF_ENDPOINT -e HF_TOKEN \
    -it \
    registry.cn-shanghai.aliyuncs.com/taosy/vllm-xft-base:0.01 \
    bash
```

```
docker run \
    -e https_proxy -e http_proxy \
    -e port=8000 \
    -p 8000:8000 \
    -d \
    registry.cn-shanghai.aliyuncs.com/taosy/vllm-xft-llama2-7b:0.01 
```

```
docker run \
    -e https_proxy -e http_proxy \
    -e port=8000 \
    -p 8000:8000 \
    -d \
    registry.cn-shanghai.aliyuncs.com/taosy/vllm-xft-qwen-7b:0.01 
```