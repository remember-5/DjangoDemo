# freeze 查询各种安装包的版本， > 重定向到requirements文本，文本名字可随意命名

pip freeze > requirements.txt

# 安装导出的各种安装包， -r 表示逐行读取安装
pip install -r requirements.txt