# 2024数学建模国赛A题-基于数值模拟的“板凳龙”运动机理模型研究

## 项目概述

本项目基于数值模拟技术，研究了传统民间表演艺术“板凳龙”的运动机理，并建立了相应的数学模型进行仿真分析。通过对“板凳龙”在行进过程中的运动状态进行精确模拟，我们旨在揭示其运动特性及规律，为相关表演和训练提供科学依据。

## 目录结构

- **problem1/**: 问题一的模型建立与求解代码
   - **savefig**: 问题一保存的图像结果
   - **problem1.py**: 问题一代码
- **problem2/**: 问题二的模型建立与求解代码
   - **savefig**: 问题二保存的图像结果
   - **problem2.py**: 问题二代码
- **problem3/**: 问题三的模型建立与求解代码
   - **savefig**: 问题三保存的图像结果
   - **problem3.py**: 问题三代码
- **problem4/**: 问题四的模型建立与求解代码
   - **savefig**: 问题四保存的图像结果
   - **problem4_1.py**: 问题四代码-路径参数求解
   - **problem4_2.py**: 问题四代码-路径表达式
   - **problem4_3.py**: 问题四代码-求解位置和速度
- **problem5/**: 问题五的模型建立与求解代码
   - **savefig**: 问题五保存的图像结果
   - **problem5.py**: 问题五代码
- **result/**: 输出数据文件
   - **result1.xlsx**: 问题一的结果数据文件
   - **result2.xlsx**: 问题二的结果数据文件
   - **result4.xlsx**: 问题四的结果数据文件
- **ProblemA.pdf**: A题题目
- **README.md**: 项目介绍
- **main.py**: 项目运行入口
- **requirements.txt**: 依赖库
- **thesis.pdf**: 论文

## 使用方法

### 环境要求

- conda
- numpy
- scipy
- matplotlib
- pandas
- shapely
- tqdm

建议使用虚拟环境（如conda或venv）来安装依赖，以避免版本冲突。

### 安装依赖

在项目根目录下，运行以下命令安装所需Python包：

```bash
pip install -r requirements.txt
```

### 运行代码

每个问的代码中都定义了一个该问题的求解器。具体使用参考`main.py`。直接运行`main.py`可以直接得到五个问的结果。

```bash
python main.py
```

### 查看结果

运行后会在`result`文件夹和各个问题的`savefig`文件夹中自动生成结果。`savefig`文件夹下有论文中出现的pdf图像。`result`文件夹下会生成各个问题需要的Excel表格文件，可用Excel打开。

## 注意事项

- 某些问题可能涉及复杂的数学模型和计算，运行时间可能较长。
- 模型的参数需要根据实际情况进行调整，以获得更准确的仿真结果。
- 代码中包含了一些假设和简化，可能会影响仿真结果的精确性。

## 贡献与反馈

欢迎对本项目提出任何改进建议或报告发现的问题。您可以通过GitHub的Issue功能提交反馈，或者直接联系项目维护者。

## 联系方式

- GitHub仓库地址：[项目链接](https://github.com/BrassWrench/CUMCM2024-A-202408007227)
- 维护者：
   - [任上旭(哈尔滨工业大学)](https://github.com/BrassWrench)
   - [刘金浩(哈尔滨工业大学)](https://github.com/FarzoneILIN)
   - [秦翊佳(哈尔滨工业大学)](https://github.com/corinamedici)

感谢查看本项目！希望它能够对您的数学建模比赛有所帮助。
