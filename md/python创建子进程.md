## python 创建子进程

### subprocess模块

直接创建子进程

```python
file_path = 'python /home/1.py'		#文件命令
subprocess.Popen(file_path)			#创建子进程,不要回显
```

获取子进程输出

```python
proc = subprocess.Popen('ipconfig', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
stdout = proc.stdout.read()
print stdout
```



