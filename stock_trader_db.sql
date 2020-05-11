CREATE database if not exists STOCK_TRADER;
use STOCK_TRADER;

CREATE table if not exists CUSTOMER(user_ID int NOT NULL, user_name varchar(20) NOT NULL, 
password varchar(20) NOT NULL, first_name varchar(30) NOT NULL, last_name varchar(30) NOT NULL,
primary key(user_ID, user_name));

CREATE table if not exists STOCK(user_ID int NOT NULL, stock_ID varchar(5) NOT NULL,
quantity int NOT NULL, market_value DECIMAL (12,2) NOT NULL,
primary key(stock_ID),
foreign key(user_ID) references CUSTOMER(user_ID));

CREATE table if not exists STOCK_ORDER(order_num int NOT NULL, stock_ID varchar(5) NOT NULL,
date_of_transaction datetime NOT NULL, num_of_shares int NOT NULL, total_cost DECIMAL (12,2) NOT NULL, 
cost_of_share DECIMAL (12,2) NOT NULL,
primary key(order_num),
foreign key(stock_ID) references STOCK(stock_ID));

CREATE table if not exists BALANCE(user_ID int NOT NULL, net_cash DECIMAL(12,2),
transaction_type varchar(10), date_of_deposit datetime, deposit_amount DECIMAL (12,2),
date_of_withdrawal datetime, withdrawal_amount DECIMAL (12,2),
primary key(user_ID),
foreign key(user_ID) references CUSTOMER(user_ID));

show tables;


/*if using phpmyadmin: Server: sql3.freemysqlhosting.net
Name: sql3336583
Username: sql3336583
Password: lV73A1HxhE
Port number: 3306 */
