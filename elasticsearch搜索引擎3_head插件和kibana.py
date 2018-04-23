# head插件相当于Navicat，用于管理数据库，基于浏览器

# 安装head插件
# https://github.com/mobz/elasticsearch-head



# npm类似与python的pip，用于安装依赖包

# 先安装nodejs和npm        https://nodejs.org/en/        

# 测试nodejs是否安装
# cmder 下
C:\Users\admin
λ node -v
v8.11.1

# 测试npm是否安装
# cmder 下
C:\Users\admin
λ npm -v
5.6.0

C:\Users\admin
λ npm -l



# 安装 cnpm        #通过 https://npm.taobao.org/ 的镜像，加速npm
# cmder下
C:\Users\admin
λ npm install -g cnpm --registry=https://registry.npm.taobao.org

# 测试cnpm是否安装
# cmder 下
C:\Users\admin
λ cnpm



# head插件安装方法
git clone git://github.com/mobz/elasticsearch-head.git
cd elasticsearch-head
npm install
npm run start
open http://localhost:9100/    # 在9100端口监听

C:\Users\admin
λ f:

F:\cmder\vendor\git-for-windows
λ cd F:\elasticsearch-head-master

F:\elasticsearch-head-master  (elasticsearch-head@0.0.0)
λ cnpm install

F:\elasticsearch-head-master  (elasticsearch-head@0.0.0)
λ cnpm run start    # 运行    # 在9100端口监听

# 用chrome打开127.0.0.1:9100
# 现在 elasticsearch 和 head是不能相连接的，要去配置

# 配置elasticsearch与heade互通
F:\elasticsearch-rtf-master\config\elasticsearch.yml
# 在最后加上以下内容：
http.cors.enabled: true
http.cors.allow-origin: "*"
http.cors.allow-methods: OPTIONS, HEAD, GET, POST, PUT, DELETE
http.cors.allow-headers: "X-Requested-With, Content-Type, Content-Length, X-User"

#重启 elasticsearch 
ctrl+c

y

C:\Users\admin
λ f:

F:\cmder\vendor\git-for-windows
λ cd F:\elasticsearch-rtf-master\bin

F:\elasticsearch-rtf-master\bin
λ elasticsearch.bat

# 刷新 127.0.0.1:9100 发现连接成功






# 安装 kibana  http://www.elastic.co/downloads/kibana  http://www.elastic.co/downloads/past-releases/kibana-5-1-2
# kibana 的版本需要与 elasticsearch 的版本一致

# 运行 kibana
# cmder下
C:\Users\admin
λ f:

F:\cmder\vendor\git-for-windows
λ cd F:\kibana-5.1.2-windows-x86\bin

F:\kibana-5.1.2-windows-x86\bin
λ kibana.bat        # 在 127.0.0.1:5601端口上运行  #Server running at http://localhost:5601

# 用chrome打开 127.0.0.1:5601

# dev tools

# get to work