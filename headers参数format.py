headers = """
Accept: application/json, text/plain, */*
Origin: http://cg.cau.edu.cn
Referer: http://cg.cau.edu.cn/provider/
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36
"""
hs = headers.split('\n')
b = [k for k in hs if len(k)]
e = b
f = {(i.split(":")[0], i.split(":", 1)[1].strip()) for i in e}
g = sorted(f)
index = 0
print("{")
for k, v in g:
    print(repr(k).replace('\'', '"'), repr(v).replace('\'', '"'), sep=':', end=",\n")
print("}")