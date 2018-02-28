## 百度云分享链接自动下载脚本
示例：
```python
import BDCLND

s = '链接: https://pan.baidu.com/s/1xxxxxx 密码: ****'
s = 'https://pan.baidu.com/s/1xxxxxx 密码: ****'
s = '链接: https://pan.baidu.com/s/1xxxxxx' # 公开分享(无密码)
s = 'https://pan.baidu.com/s/1xxxxxx' # 公开分享(无密码)
# 以上形式均可，前后还可以有其它字符
path = 'C:\\'

r = BDCLND.download(s, path) # path可以省略
print(r)
```