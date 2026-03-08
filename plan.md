# 碎片整理测试计划

## 1. 增加数据量
当前表 `composite_key_table` 只有 50,000 行数据，表大小约 49MB。
为了有效测试 `ALTER TABLE` 的性能和并发读写能力，我们需要增加数据量，使表足够大（例如几百 MB 或更多），这样 `ALTER` 操作才会有明显的执行时间。

**执行步骤：**
- 运行 `python insert_composite_key_table.py`，插入 1,000,000 行数据。

## 2. 生成碎片
数据插入后，表是紧凑的。我们需要通过大量的随机删除和插入操作来制造“空洞”（碎片）。
`data_free` 指标将反映碎片的大小。

**执行步骤：**
- 运行 `python run_fragment_until.py`，该脚本会循环调用 `fragment_test.py`，直到碎片空间（`data_free`）超过 1GB（或达到显著水平）。
- 或者手动运行 `python fragment_test.py` 多次，观察 `data_free` 的变化。

## 3. 准备测试脚本 (`alter_test.py`)
现有的 `alter_test.py` 需要改进以准确模拟并发场景：
- **修改 SQL 语句**：添加 `ENGINE=InnoDB`，强制重建表以释放空间。
  `ALTER TABLE composite_key_table ALGORITHM=INPLACE, LOCK=NONE, ENGINE=InnoDB;`
- **优化并发测试**：主线程应持续运行读写操作直到 `ALTER` 线程结束，而不是固定循环 5 次。
- **增强日志**：记录每次操作的耗时，以便观察是否发生阻塞。

## 4. 执行测试与验证
运行修改后的 `alter_test.py`，并观察：
- `ALTER` 操作期间，读（SELECT）和写（INSERT）操作是否成功且无显著延迟。
- `ALTER` 完成后，`data_free` 是否显著减少（理想情况接近 0 或大幅降低）。
- 确认整个过程没有锁表（LOCK=NONE）。

## 5. 预期结果
- `data_free` 在 `ALTER` 后显著减小。
- 在 `ALTER` 执行期间，应用程序（模拟脚本）可以正常读写数据库。
