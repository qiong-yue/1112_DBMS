-- User
-- is_seller default設定false（註冊只有買家）
CREATE TABLE User
(
user_id     INTEGER             PRIMARY KEY  AUTOINCREMENT,
address     VARCHAR(255)      NOT NULL,
phone       VARCHAR(32)      NOT NULL,
email       VARCHAR(255)      NOT NULL UNIQUE,
Bdate       DATE             NOT NULL,
password    VARCHAR(255)     NOT NULL,
is_seller   BOOLEAN          DEFAULT FALSE
);

-- Locate
CREATE TABLE Locate
(
Locate_id   INTEGER           PRIMARY KEY  AUTOINCREMENT,
address     VARCHAR(255)      NOT NULL,
phone       VARCHAR(32)      NOT NULL
);

-- Type
CREATE TABLE Type
(
type_id     INTEGER           PRIMARY KEY  AUTOINCREMENT,
name        VARCHAR(32)
);

-- Prduct
CREATE TABLE Product
(
product_id      INTEGER           PRIMARY KEY  AUTOINCREMENT,
seller_email    VARCHAR(255)      NOT NULL,
product_name    VARCHAR(255)      NOT NULL,
type_id         INTEGER           NOT NULL,
store           INTEGER           NOT NULL,
price           INTEGER           NOT NULL,
origin          VARCHAR(255)      NOT NULL,
FOREIGN KEY(type_id) REFERENCES Type(type_id)
FOREIGN KEY(seller_email) REFERENCES User(email)
);

-- Orders
-- 我用Orders(因為我的電腦不知道為啥Order就會出錯)
CREATE TABLE Orders
(
user_id         INTEGER          NOT NULL,
product_id      INTEGER          NOT NULL,
price           INTEGER          NOT NULL,
locate_id       INTEGER          NOT NULL,
amount          INTEGER          NOT NULL,
PRIMARY KEY(user_id, product_id)
FOREIGN KEY(user_id) REFERENCES User(user_id)
FOREIGN KEY(product_id) REFERENCES Product(product_id)
FOREIGN KEY(locate_id) REFERENCES Locate(locate_id)
);


