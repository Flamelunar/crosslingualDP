对应大论文第三个论文-AAAI 2025

# 论文训练步骤文档

## 环境准备

### 1. 激活Conda环境

```
conda activate llama_factory
```

## 训练执行

### 2. 运行训练脚本

```
./exe --is_dictionary_exist 1 --random_seed 1540422239 --is_train 1 --is_test 0 > log.train 2>&1
```

### 3. 后台运行方式(先进入当前目录)

```
nohup ./run.sh &
```
这是第一篇论文的

# 论文训练步骤文档

## 环境准备

### 1. 激活Conda环境

```
conda activate llama_factory
```

## 训练执行

### 2. 运行训练脚本

```
./exe --is_dictionary_exist 1 --random_seed 1540422239 --is_train 1 --is_test 0 > log.train 2>&1
```

### 3. 后台运行方式(先进入当前目录)

```
nohup ./run.sh &
```

### 4. 查看训练日志

```
tail -f log.train
```

---

## 参数说明

| 参数 | 值 | 说明 |
| ------ |------ |------ |
| `--is_dictionary_exist` | 1 | 字典是否存在标志 |
| `--random_seed` | 1540422239 | 随机种子设置 |
| `--is_train` | 1 | 是否进行训练 |
| `--is_test` | 0 | 是否进行测试 |

## 日志管理

- **日志文件**: `log.train`
- **输出重定向**: `> log.train 2>&1`
- **实时监控**: `tail -f log.train`

---

**文档生成时间**: 2024年


### 4. 查看训练日志

```
tail -f log.train
```

---

## 参数说明

| 参数 | 值 | 说明 |
| ------ |------ |------ |
| `--is_dictionary_exist` | 1 | 字典是否存在标志 |
| `--random_seed` | 1540422239 | 随机种子设置 |
| `--is_train` | 1 | 是否进行训练 |
| `--is_test` | 0 | 是否进行测试 |

## 日志管理

- **日志文件**: `log.train`
- **输出重定向**: `> log.train 2>&1`
- **实时监控**: `tail -f log.train`

---

**文档生成时间**: 2024年

