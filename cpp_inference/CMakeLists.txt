 
cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
project(ur5_inference)

find_package(Torch REQUIRED)

add_executable(inference_example inference_example.cpp)
target_link_libraries(inference_example ${TORCH_LIBRARIES})
set_property(TARGET inference_example PROPERTY CXX_STANDARD 14)