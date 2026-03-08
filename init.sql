CREATE TABLE composite_key_table (
    time_col DATETIME NOT NULL,
    number_col INT NOT NULL,
    string_col VARCHAR(50) NOT NULL,
    num_val1 INT,
    num_val2 DECIMAL(10, 2),
    num_val3 BIGINT,
    string_val1 VARCHAR(100),
    string_val2 VARCHAR(100),
    string_val3 VARCHAR(100),
    num_val4 FLOAT,
    PRIMARY KEY (time_col, number_col, string_col, num_val1, num_val2, num_val3, string_val1, string_val2)
);

-- 添加6个不同组合的索引
CREATE INDEX idx_number_string ON composite_key_table(number_col, string_col);
CREATE INDEX idx_time_number ON composite_key_table(time_col, number_col);
CREATE INDEX idx_string_numval1 ON composite_key_table(string_col, num_val1);
CREATE INDEX idx_numval2_numval3 ON composite_key_table(num_val2, num_val3);
CREATE INDEX idx_stringval1_time ON composite_key_table(string_val1, time_col);
CREATE INDEX idx_all_strings ON composite_key_table(string_col, string_val1, string_val2);

-- 插入10条数据
INSERT INTO composite_key_table VALUES
(NOW(), 1001, 'SKU_A', 100, 99.99, 1000000, 'Product_A', 'Category_A', 'Active', 3.14),
(DATE_ADD(NOW(), INTERVAL 1 HOUR), 1002, 'SKU_B', 200, 199.99, 2000000, 'Product_B', 'Category_B', 'Inactive', 2.71),
(DATE_ADD(NOW(), INTERVAL 2 HOUR), 1003, 'SKU_C', 300, 299.99, 3000000, 'Product_C', 'Category_C', 'Active', 1.41),
(DATE_ADD(NOW(), INTERVAL 3 HOUR), 1004, 'SKU_D', 400, 399.99, 4000000, 'Product_D', 'Category_D', 'Pending', 2.23),
(DATE_ADD(NOW(), INTERVAL 4 HOUR), 1005, 'SKU_E', 500, 499.99, 5000000, 'Product_E', 'Category_E', 'Active', 1.62),
(DATE_ADD(NOW(), INTERVAL 5 HOUR), 1006, 'SKU_F', 600, 599.99, 6000000, 'Product_F', 'Category_F', 'Archived', 0.88),
(DATE_ADD(NOW(), INTERVAL 6 HOUR), 1007, 'SKU_G', 700, 699.99, 7000000, 'Product_G', 'Category_G', 'Active', 1.11),
(DATE_ADD(NOW(), INTERVAL 7 HOUR), 1008, 'SKU_H', 800, 799.99, 8000000, 'Product_H', 'Category_H', 'Inactive', 0.50),
(DATE_ADD(NOW(), INTERVAL 8 HOUR), 1009, 'SKU_I', 900, 899.99, 9000000, 'Product_I', 'Category_I', 'Active', 2.99),
(DATE_ADD(NOW(), INTERVAL 9 HOUR), 1010, 'SKU_J', 1000, 999.99, 10000000, 'Product_J', 'Category_J', 'Active', 1.73);
