## �ٶ��Ʒ��������Զ����ؽű�
ʾ����
```python
import BDCLND

s = '����: https://pan.baidu.com/s/1xxxxxx ����: ****'
s = 'https://pan.baidu.com/s/1xxxxxx ����: ****'
s = '����: https://pan.baidu.com/s/1xxxxxx' # ��������(������)
s = 'https://pan.baidu.com/s/1xxxxxx' # ��������(������)
# ������ʽ���ɣ�ǰ�󻹿����������ַ�
path = 'C:\\'

r = BDCLND.download(s, path) # path����ʡ��
print(r)
```