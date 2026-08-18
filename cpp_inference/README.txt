### C++ 推理示例（LibTorch）

该示例展示了如何使用 C++ (LibTorch) 加载训练好的 TorchScript 模型。

**编译与运行（需安装 LibTorch）**：
```bash
mkdir build && cd build
cmake .. -DCMAKE_PREFIX_PATH=`python3 -c 'import torch;print(torch.utils.cmake_prefix_path)'`
make
./inference_example