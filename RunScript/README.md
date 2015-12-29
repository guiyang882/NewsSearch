# 相关脚本操作

## 定时抓取脚本
- 将启动的脚本写在本地文件中
- 可以在crontab -e 中添加相应的自动化启动脚本
```
0 */6 * * * /bin/bash command_file.sh
```

## 对数据库的操作
- 使用如下命令对mongodb进行数据备份
```
mongodump -h 127.0.0.1 -d python -o ~/Document/
```
- 使用如下命令对mongodb进行数据恢复
```
mongorestore -h 127.0.0.1 -d python --directoryperdb ~/python/
```
