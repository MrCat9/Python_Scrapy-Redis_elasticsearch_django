# head����൱��Navicat�����ڹ������ݿ⣬���������

# ��װhead���
# https://github.com/mobz/elasticsearch-head



# npm������python��pip�����ڰ�װ������

# �Ȱ�װnodejs��npm        https://nodejs.org/en/        

# ����nodejs�Ƿ�װ
# cmder ��
C:\Users\admin
�� node -v
v8.11.1

# ����npm�Ƿ�װ
# cmder ��
C:\Users\admin
�� npm -v
5.6.0

C:\Users\admin
�� npm -l



# ��װ cnpm        #ͨ�� https://npm.taobao.org/ �ľ��񣬼���npm
# cmder��
C:\Users\admin
�� npm install -g cnpm --registry=https://registry.npm.taobao.org

# ����cnpm�Ƿ�װ
# cmder ��
C:\Users\admin
�� cnpm



# head�����װ����
git clone git://github.com/mobz/elasticsearch-head.git
cd elasticsearch-head
npm install
npm run start
open http://localhost:9100/    # ��9100�˿ڼ���

C:\Users\admin
�� f:

F:\cmder\vendor\git-for-windows
�� cd F:\elasticsearch-head-master

F:\elasticsearch-head-master  (elasticsearch-head@0.0.0)
�� cnpm install

F:\elasticsearch-head-master  (elasticsearch-head@0.0.0)
�� cnpm run start    # ����    # ��9100�˿ڼ���

# ��chrome��127.0.0.1:9100
# ���� elasticsearch �� head�ǲ��������ӵģ�Ҫȥ����

# ����elasticsearch��heade��ͨ
F:\elasticsearch-rtf-master\config\elasticsearch.yml
# ���������������ݣ�
http.cors.enabled: true
http.cors.allow-origin: "*"
http.cors.allow-methods: OPTIONS, HEAD, GET, POST, PUT, DELETE
http.cors.allow-headers: "X-Requested-With, Content-Type, Content-Length, X-User"

#���� elasticsearch 
ctrl+c

y

C:\Users\admin
�� f:

F:\cmder\vendor\git-for-windows
�� cd F:\elasticsearch-rtf-master\bin

F:\elasticsearch-rtf-master\bin
�� elasticsearch.bat

# ˢ�� 127.0.0.1:9100 �������ӳɹ�






# ��װ kibana  http://www.elastic.co/downloads/kibana  http://www.elastic.co/downloads/past-releases/kibana-5-1-2
# kibana �İ汾��Ҫ�� elasticsearch �İ汾һ��

# ���� kibana
# cmder��
C:\Users\admin
�� f:

F:\cmder\vendor\git-for-windows
�� cd F:\kibana-5.1.2-windows-x86\bin

F:\kibana-5.1.2-windows-x86\bin
�� kibana.bat        # �� 127.0.0.1:5601�˿�������  #Server running at http://localhost:5601

# ��chrome�� 127.0.0.1:5601

# dev tools

# get to work