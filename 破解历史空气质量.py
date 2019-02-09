import PyV8

func = '''
    (function loaddata() {
  var method = 'GETDAYDATA';
  var param = {};
  param.city = '广州';
  param.month = '2';
  getServerData(method, param, function(obj) {
    // console.log(obj);
    obj = obj.data;
    items = obj.items;
  }, 6);
    return items;
})
'''

execute = PyV8.JSContext()
execute.enter()


# with open('weather01.js')as f:
#     a = f.read()
#
# with open('weather02.js')as f:
#     b = f.read()
#
# with open('weather03.js')as f:
#     c = f.read()

with open('weather04.js')as f:
    d = f.read()

# with open('weather05.js')as f:
#     e = f.read()


result = execute.eval(d + func)
print(result())
