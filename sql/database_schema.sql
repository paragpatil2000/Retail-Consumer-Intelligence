PRAGMA foreign_keys = ON;


-- ==========================================
-- 1. CUSTOMERS
-- ==========================================

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    age INT,
    gender VARCHAR(20),
    marital_status VARCHAR(20),
    education VARCHAR(50),
    occupation VARCHAR(50),
    annual_income DECIMAL(12,2),
    family_size INT,
    children INT,
    city VARCHAR(50),
    state VARCHAR(50),
    region VARCHAR(20),
    membership_type VARCHAR(20),
    join_date DATE,
    preferred_payment VARCHAR(20),
    preferred_channel VARCHAR(20)
);


-- ==========================================
-- 2. PRODUCTS
-- ==========================================

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    brand VARCHAR(50),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    package_size DECIMAL(10,2),
    unit VARCHAR(20),
    mrp DECIMAL(10,2),
    cost_price DECIMAL(10,2),
    selling_price DECIMAL(10,2),
    gst_percent DECIMAL(5,2),
    shelf_life_days INT
);


-- ==========================================
-- 3. STORES
-- ==========================================

CREATE TABLE stores (
    store_id INT PRIMARY KEY,
    store_name VARCHAR(100),
    store_type VARCHAR(50),
    city VARCHAR(50),
    state VARCHAR(50),
    region VARCHAR(20),
    pincode VARCHAR(10),
    area_sqft INT,
    opening_date DATE,
    daily_footfall INT,
    total_employees INT,
    parking_available BOOLEAN
);


-- ==========================================
-- 4. PROMOTIONS
-- ==========================================

CREATE TABLE promotions (
    promotion_id INT PRIMARY KEY,
    campaign_name VARCHAR(100),
    campaign_type VARCHAR(50),
    discount_percent DECIMAL(5,2),
    start_date DATE,
    end_date DATE,
    target_category VARCHAR(50),
    target_brand VARCHAR(50),
    coupon_code VARCHAR(30),
    festival VARCHAR(50),
    promotion_budget DECIMAL(12,2),
    advertising_channel VARCHAR(50)
);


-- ==========================================
-- 5. CALENDAR
-- ==========================================

CREATE TABLE calendar (
    date DATE PRIMARY KEY,
    date_key INT UNIQUE,
    year INT,
    quarter VARCHAR(5),
    month INT,
    month_name VARCHAR(20),
    week_number INT,
    day INT,
    day_name VARCHAR(20),
    day_of_week INT,
    is_weekend BOOLEAN,
    financial_year VARCHAR(20),
    season VARCHAR(30),
    festival VARCHAR(50)
);


-- ==========================================
-- 6. TRANSACTIONS - FACT TABLE
-- ==========================================

CREATE TABLE transactions (
    transaction_id BIGINT PRIMARY KEY,
    transaction_date DATE NOT NULL,
    transaction_time TIME,

    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    store_id INT NOT NULL,
    promotion_id INT,

    quantity INT,
    mrp DECIMAL(10,2),
    selling_price DECIMAL(10,2),
    discount_percent DECIMAL(5,2),
    total_amount DECIMAL(12,2),

    payment_method VARCHAR(30),
    sales_channel VARCHAR(30),
    coupon_used BOOLEAN,
    return_flag BOOLEAN,

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    FOREIGN KEY (store_id)
        REFERENCES stores(store_id),

    FOREIGN KEY (promotion_id)
        REFERENCES promotions(promotion_id),

    FOREIGN KEY (transaction_date)
        REFERENCES calendar(date)
);