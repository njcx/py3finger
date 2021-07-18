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


使用方式3：

```python
    from py3finger import PyFinger
    html = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>菜鸟教程(runoob.com)</title></head><body><h1>我的第一个标题</h1><p>我的第一个段落。</p></body><script src="/wp-content/themes/runoob/assets/js/main.min.js?v=1.191"></script></html>'
    header = {'Server': 'Tengine', 'Content-Type': 'text/html; charset=UTF-8', 'Content-Length': '189777', 'Connection': 'keep-alive', 'Date': 'Sun, 18 Jul 2021 08:25:20 GMT', 'Vary': 'Accept-Encoding', 'Link': '<http://www.runoob.com/wp-json/>; rel="https://api.w.org/"', 'Content-Encoding': 'gzip', 'Ali-Swift-Global-Savetime': '1626596720', 'Via': 'cache31.l2hk71[0,11,200-0,H], cache11.l2hk71[12,0], cache4.hk6[0,1,200-0,H], cache8.hk6[3,0]', 'Age': '11468', 'X-Cache': 'HIT TCP_HIT dirn:9:355117788', 'X-Swift-SaveTime': 'Sun, 18 Jul 2021 09:59:53 GMT', 'X-Swift-CacheTime': '80727', 'Timing-Allow-Origin': '*', 'EagleId': '2ff6108c16266081883755579e'}
    if __name__ == "__main__":
        pyfinger = PyFinger()
        print(pyfinger.new_from_html(html,header))
```




![Image](https://raw.githubusercontent.com/njcx/py3finger/master/1sfx12.jpg)