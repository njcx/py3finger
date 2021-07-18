# Py3finger

是一个HTTP指纹识别类库


使用方式1：

```python
    from py3finger import PyFinger
    if __name__ == "__main__":
        pyfinger = PyFinger()
        print(pyfinger.new_from_url('https://www.runoob.com/'))
```



使用方式2：

```python
    from py3finger import PyFinger
    import requests
    if __name__ == "__main__":
        pyfinger = PyFinger()
        req = requests.get('https://www.runoob.com/')
        print(pyfinger.new_from_response(req))
```




![Image](https://raw.githubusercontent.com/njcx/py3finger/master/1sfx12.jpg)