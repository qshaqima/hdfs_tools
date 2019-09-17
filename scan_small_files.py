import os

if __name__ == '__main__':

# 统计hdfs上小于20MB的文件分布情况 执行以下命令
# python3 getSmallFiles.py
# 下载当前目录下的small_files_stat.csv文件至本地用excel打开按文件数量降序排序即可

 cur_path=os.getcwd()
file_path=cur_path+'/small_files_stat.txt'

with open(cur_path+'/small_files_stat.csv', 'w') as file_to_write:
 file_to_write.write('目录总大小,文件数量,路径,文件平均大小')

 r = os.system('hadoop fs -ls -R / | grep ^- > '+cur_path+'/small_files_stat.txt')
 print('hadoop fs -ls -R result is '+str(r))

 with open(file_path, 'r') as file_to_read:
  i =0 #当前数据条数
  n =0 #目录下的数据条数
  path = "" #路径
  dir_size = 0 #目录大小
  for line in file_to_read:
   i = i+1
   split = line.split()

   if int(split[4])< 20971520:#如果文件小于20MB
    file_name = split[7].split("/") #将路径按"/"切分成数组
    file_name = file_name[0:len(file_name)-2] #获取去除最后两个/后的路径 （一般去除后精确到表名）

    if i == 1: #如果是第一条数据
     path= '/'.join(file_name);
     dir_size = dir_size +int(split[4]) #累加文件的大小
     n = n+1;
    else:
     if path == '/'.join(file_name): #如果与上条记录的路径一致
      dir_size = dir_size +int(split[4]) #累加文件的大小
      n = n+1;
     else: #如果与上条记录的路径不一致
      avg = round(dir_size/n/1024,1)#平均文件大小
      sum = round(dir_size/1024/1024,1)# 每个目录的总大小
      file_to_write.write('\n'+str(sum)+'MB,'+str(n)+','+path+','+str(avg)+"KB")#输出统计结果
      n =1; dir_size=0 # 归零
      path = '/'.join(file_name)


