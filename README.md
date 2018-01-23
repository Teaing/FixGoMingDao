# mingdaoproxy
一个给明道APP上下班打卡功能打补丁的代理  

实现原理：  
**APP请求接口-->代理拦截返回请求并且修改(距离)-->点击打卡按钮-->拦截请求并修改(修改提交的经纬度为打卡公司经纬度以及位置中文说明)-->打卡成功**


存放路径：/data/MingDao/

计划任务使用:  

    */2 * * * * /usr/sbin/ntpdate time.windows.com time-a.nist.gov time-b.nist.gov time-nw.nist.gov
    30 07 * * 1-5 /usr/bin/python /data/MingDao/mingdaoproxy.py -d
    30 09 * * 1-5 /usr/bin/python /data/MingDao/mingdaoproxy.py -stop -pid /tmp/MingDao.pid

第一条： 同步时间  
第二条： 工作日07:30开启代理  
第三条： 工作日09:30关闭代理  

只开两个小时是因为没有认证跟安全策略，临时方案，大家可以自己设置  
默认端口：62000  

config.py 文件中的address_info就填写公司打卡位置  

    # 打卡地址信息分别是地址信息的unicode编码, longitude经度, latitude纬度
    address_info = [u'\u65b9\u821f\u5927\u53a6', '121.4815163612', '31.2649791194']

utils/handle.py 文件中的200000是能打卡的距离,默认设置这个数值    

Android端跟IOS端都需要取ssl下面的目录安装好证书  
IOS需要越狱，因为APP做了双向验证  
Android,我的设备是越狱的,不越狱也可以试试,证书都是必装  

然后再设置WIFI代理，你的机器IP:62000端口,打开明道就可以打卡了  

别忘了安装requirements.txt的模块 


直接拿的wyproxy的代码改的,谢谢猪猪侠:  
[**https://github.com/ring04h/wyproxy**](https://github.com/ring04h/wyproxy "https://github.com/ring04h/wyproxy")  
