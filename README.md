# DBMS 五星好蘋-團購系統資料庫
1112 Database Management System Final Project

## 專案描述
此為[1112-資料庫系統]課程的期末專案。網站名稱為｢五星好蘋」。  
這是一個團購平台系統，服務的對象為平台會員，旨在提供一個方便且簡單易使用的團購網站。會員們可選擇是否擔任開團主或僅參與團購，並依照自己的需求使用下列的功能。

## 主要功能
-  註冊：用戶可透過註冊成為會員，其中email為帳號
-  登入：email為帳號，密碼自訂  
-  修改會員資料：可進入會員資料的畫面修改資料  
-  團購主上架商品：新增產品資訊以上架商品  
-  會員查找商品：依商品的種類進行查找，以快速找到符合自己需求的商品  
-  會員訂購商品：進入各商品類別後將商品加入購物車
-  會員查看訂單：在購物車畫面中，可檢視自己的加入的商品並修改數量

## 系統架構
-  開發語言：Python +Ｈtml + Css
-  開發框架：Flask
-  DBMS語言：SQLite3
-  開發工具：vscode

## 下載並使用
### 下載資料夾
git clone <repository_url>  
cd <repository_name>  
### 安裝虛擬環境(choise)
pip install virtualenv  
virtualenv --version  
virtualenv venv  
### 啟動虛擬環境(choise)
venv\Scripts\activate
### 安裝flask
pip install flask
### Run
python -m flask run
### 離開虛擬環境(choise)
deactivate

## 小組資訊
-  組名：五星好蘋
-  成員：
    -  110703057 資科二 陳芎月(組長)
    -  110703024 資科二 許可蓁
    -  110703049 資科二 曾毓雯
    -  110703002 資科二 黃甄浥
    -  110703033 資科二 張發貴
    -  110207413 資科二 黃思璇
    -  107103035 歷史四 江曉陽
