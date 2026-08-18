 #include <torch/script.h> // LibTorch 核心头文件
#include <iostream>
#include <memory>

int main(int argc, const char* argv[]) {
    // 1. 检查 CUDA 是否可用
    torch::Device device(torch::kCPU);
    if (torch::cuda::is_available()) {
        std::cout << "CUDA 可用！使用 GPU 推理。" << std::endl;
        device = torch::kCUDA;
    }

    // 2. 加载模型（注意：模型文件在上级目录）
    std::string model_path = "../ur5_policy_traced.pt";
    torch::jit::script::Module module;
    try {
        module = torch::jit::load(model_path);
        module.to(device);
        module.eval();
        std::cout << "✅ 模型加载成功！" << std::endl;
    } catch (const c10::Error& e) {
        std::cerr << "❌ 加载模型失败: " << e.what() << std::endl;
        return -1;
    }

    // 3. 模拟观测输入（假设观测维度为 24）
    int obs_dim = 24;
    std::vector<torch::jit::IValue> inputs;
    torch::Tensor obs = torch::randn({1, obs_dim});
    inputs.push_back(obs.to(device));

    // 4. 执行推理
    torch::Tensor action = module.forward(inputs).toTensor();
    std::cout << "🎯 推理成功！动作输出: " << action << std::endl;

    return 0;
}