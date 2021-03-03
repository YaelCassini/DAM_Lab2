from flask import Flask, url_for, redirect, request
from flask import render_template
import os
app = Flask(__name__)

#catalog页面的数据类
class Data(object):
    index = ""
    html_addr = ""
    pic_addr = ""
    music_addr = ""
    name = ""
    singer = ""
    CD = ""
    singer_addr = ""
    CD_addr = ""

#音乐信息类
class MusicData(object):
    index=""
    pic_addr =""
    mp3_addr=""
    name=""
    singer=""
    CD=""
    singer_addr=""
    CD_addr=""
    last_addr=""
    next_addr=""


#主页
@app.route('/')
def home():
    return walkThough("all")

#分类索引页
@app.route('/<index>')
@app.route('/song/<index>')
def walkThough(index=""):

    datalist = []
    indexlist = []
    origin_path=".\static\src"   #资源所在路径
    if index=="all":
        index=""
        path=origin_path;
    else:
        path = origin_path + "\\" + index

    for root, dirs, files in os.walk(origin_path):
        for d in dirs:
            print(os.path.join(root, d))
            dirname, basename = os.path.split(os.path.join(root, d))
            #print(basename)
            indexlist.append(basename)

    for root, dirs, files in os.walk(path):
        split = "."
        # 遍历文件
        for filename in files:
            
            filepath = os.path.join(root, filename)
            name, category = os.path.splitext(filename)  # 分解文件扩展名
            dirname, basename = os.path.split(filepath)
            tmp_ls = dirname.lstrip(origin_path)

            if filename.endswith(".mp3"):
                temp=Data()
                temp.index=tmp_ls
                temp.html_addr="/"+temp.index+"/"+name;
                temp.pic_addr="src/"+temp.index+"/"+name+".png"
                temp.music_addr="src/"+temp.index+"/"+name+".mp3"
                txt_addr=temp.index+"/"+name+".txt"


                file=open(origin_path+"/"+txt_addr,"r" ,encoding='UTF-8')
                lines= file.readlines()
                for line in lines:
                    if line.startswith('\"description\"', 0, len(line)):
                        #从txt文件中提取歌名
                        i=0
                        str1="《"
                        str2="》"
                        index1 = line.find(str1, i, len(line))
                        index2 = line.find(str2, i, len(line))
                        temp.name=line[index1+1:index2]
                        i=index2

                        #提取歌手
                        str1 = "由"
                        str2 = "演唱"
                        index1 = line.find(str1, i, len(line))
                        index2 = line.find(str2, i, len(line))
                        temp.singer = line[index1 + 2:index2-1]
                        i=index2

                        #提取专辑名
                        str1 = "收录于《"
                        str2 = "》"
                        index1 = line.find(str1, i, len(line))
                        index2 = line.find(str2, i, len(line))
                        #没有查找到后书名号
                        if index2==-1:
                            index2=len(line-1)
                        temp.CD = line[index1 + 4:index2]

                temp.singer_addr="/singer/"+temp.singer;
                temp.CD_addr = "/CD/" + temp.CD;

                #在list中加入当前信息对象
                datalist.append(temp)

        # 遍历所有的文件夹
        for d in dirs:
            dirname, basename = os.path.split(os.path.join(root, d))

    return render_template('catalog.html', datalist=datalist, indexlist=indexlist)

@app.route('/<index>/<name>')
@app.route('/song/<index>/<name>')
def song(name='001', index=""):
    music=MusicData()


    origin_path=".\static\src"   #资源所在路径
    if index=="all":
        index=""
        path=origin_path;
    else:
        path = origin_path + "\\" + index

    for root, dirs, files in os.walk(path):
        split = "."
        # 遍历文件
        last_name=""
        now_name=""
        for filename in files:
            temp_name, category = os.path.splitext(filename)  # 分解文件扩展名
            if filename.endswith(".mp3"):
                now_name=temp_name
                if last_name==name:
                    music.next_addr="/"+index+"/"+temp_name
                if now_name==name:
                    music.last_addr="/"+index+"/"+last_name
                last_name=temp_name


    if music.last_addr=="/Chinese/":
        music.last_addr=""
    if music.next_addr == "/Chinese/":
        music.next_addr = ""
    print("$$last:" + music.last_addr)
    print("$$next:" + music.next_addr)


    music.index=index
    music.mp3_addr='src/'+index+"/"+name+'.mp3'
    music.pic_addr='src/'+index+"/"+name+'.png'
    txt_addr='src/'+index+"/"+name+'.txt'
    origin_path = "./static"
    file=open(origin_path+"/"+txt_addr,"r" ,encoding='UTF-8')
    lines = file.readlines()
    for line in lines:
        if line.startswith('\"description\"', 0, len(line)):
            #提取歌名
            i = 0
            str1 = "《"
            str2 = "》"
            index1 = line.find(str1, i, len(line))
            index2 = line.find(str2, i, len(line))
            music.name = line[index1 + 1:index2]
            i = index2

            #提取歌手名
            str1 = "由"
            str2 = "演唱"
            index1 = line.find(str1, i, len(line))
            index2 = line.find(str2, i, len(line))
            music.singer = line[index1 + 2:index2 - 1]
            i = index2

            #提取专辑名
            str1 = "收录于《"
            str2 = "》"
            index1 = line.find(str1, i, len(line))
            index2 = line.find(str2, i, len(line))
            if index2 == -1:
                index2 = len(line - 1)
            music.CD = line[index1 + 4:index2]

            music.singer_addr = "/singer/" + music.singer
            music.CD_addr = "/CD/" + music.CD

    return render_template('music.html', name=name, musicdata=music)


#歌手页面
@app.route('/singer/<singer>')
def walkSinger(singer=""):

    return walkChoice(2, singer)


#专辑页面
@app.route('/CD/<CD>')
def walkCD(CD=""):

    return walkChoice(3, CD)


@app.route('/searchname', methods=['post', 'get'])
def search_name():
    content = request.form.get('content')

    datalist = []

    origin_path = ".\static\src"
    path = origin_path;

    for root, dirs, files in os.walk(path):
        split = "."
        # 遍历文件
        for filename in files:
            filepath = os.path.join(root, filename)
            name, category = os.path.splitext(filename)  # 分解文件扩展名

            dirname, basename = os.path.split(filepath)
            tmp_ls = dirname.lstrip(origin_path)

            if filename.endswith(".mp3"):
                temp = Data()
                temp.index = tmp_ls
                temp.html_addr = "/song/" + temp.index + "/" + name;
                temp.pic_addr = "src/" + temp.index + "/" + name + ".png"
                temp.music_addr = "src/" + temp.index + "/" + name + ".mp3"
                txt_addr = temp.index + "/" + name + ".txt"
                file = open(origin_path + "/" + txt_addr, "r", encoding='UTF-8')
                lines = file.readlines()
                for line in lines:
                    if line.startswith('\"description\"', 0, len(line)):

                        i = 0
                        str1 = "《"
                        str2 = "》"
                        index1 = line.find(str1, i, len(line))
                        index2 = line.find(str2, i, len(line))
                        temp.name = line[index1 + 1:index2]
                        i = index2

                        str1 = "由"
                        str2 = "演唱"
                        index1 = line.find(str1, i, len(line))
                        index2 = line.find(str2, i, len(line))
                        temp.singer = line[index1 + 2:index2 - 1]
                        i = index2

                        str1 = "收录于《"
                        str2 = "》"
                        index1 = line.find(str1, i, len(line))
                        index2 = line.find(str2, i, len(line))
                        if index2 == -1:
                            index2 = len(line - 1)
                            # print(name)
                        temp.CD = line[index1 + 4:index2]

                temp.singer_addr = "/singer/" + temp.singer;
                temp.CD_addr = "/CD/" + temp.CD

                if content in temp.name:
                    datalist.append(temp)

        # 遍历所有的文件夹
        for d in dirs:
            print(os.path.join(root, d))

    return render_template('catalog.html', datalist=datalist)


@app.route('/searchsinger', methods=['post', 'get'])
def search_singer():
    content = request.form.get('content2')


    datalist = []

    origin_path = ".\static\src"
    path = origin_path;

    for root, dirs, files in os.walk(path):
        split = "."
        # 遍历文件
        for filename in files:
            filepath = os.path.join(root, filename)
            name, category = os.path.splitext(filename)  # 分解文件扩展名

            dirname, basename = os.path.split(filepath)
            tmp_ls = dirname.lstrip(origin_path)
            tmp_re = filepath.replace(path, "", 1)
            tmp_sp = filepath.split(path, 1)[1]
            if filename.endswith(".mp3"):
                temp = Data()
                temp.index = tmp_ls
                temp.html_addr = "/song/" + temp.index + "/" + name
                temp.pic_addr = "src/" + temp.index + "/" + name + ".png"
                temp.music_addr = "src/" + temp.index + "/" + name + ".mp3"

                txt_addr = temp.index + "/" + name + ".txt"
                # print(origin_path+txt_addr)
                file = open(origin_path + "/" + txt_addr, "r", encoding='UTF-8')
                lines = file.readlines()
                for line in lines:
                    if line.startswith('\"description\"', 0, len(line)):
                        # print(line)
                        # print(name)
                        i = 0
                        str1 = "《"
                        str2 = "》"
                        index1 = line.find(str1, i, len(line))
                        index2 = line.find(str2, i, len(line))
                        temp.name = line[index1 + 1:index2]
                        # print(temp.name)
                        i = index2

                        str1 = "由"
                        str2 = "演唱"
                        index1 = line.find(str1, i, len(line))
                        index2 = line.find(str2, i, len(line))
                        temp.singer = line[index1 + 2:index2 - 1]
                        # print(temp.singer)
                        i = index2

                        str1 = "收录于《"
                        str2 = "》"
                        index1 = line.find(str1, i, len(line))
                        index2 = line.find(str2, i, len(line))
                        if index2 == -1:
                            index2 = len(line - 1)
                            # print(name)
                        temp.CD = line[index1 + 4:index2]
                        # print(temp.CD)

                temp.singer_addr = "/singer/" + temp.singer
                temp.CD_addr = "/CD/" + temp.CD
                # print("###"+temp.CD_addr)

                if content in temp.singer:
                    datalist.append(temp)

                # print(temp.html_addr)
                # print(temp.pic_addr)
        # 遍历所有的文件夹
        for d in dirs:
            print(os.path.join(root, d))

    return render_template('catalog.html', datalist=datalist)

@app.route('/searchCD', methods=['post', 'get'])
def search_CD():
    content = request.form.get('content3')

    datalist = []

    origin_path = ".\static\src"
    path = origin_path;

    for root, dirs, files in os.walk(path):
        split = "."
        # 遍历文件
        for filename in files:
            filepath = os.path.join(root, filename)
            name, category = os.path.splitext(filename)  # 分解文件扩展名

            dirname, basename = os.path.split(filepath)
            tmp_ls = dirname.lstrip(origin_path)
            tmp_re = filepath.replace(path, "", 1)
            tmp_sp = filepath.split(path, 1)[1]
            if filename.endswith(".mp3"):
                temp = Data()
                temp.index = tmp_ls
                temp.html_addr = "/song/" + temp.index + "/" + name
                temp.pic_addr = "src/" + temp.index + "/" + name + ".png"
                temp.music_addr = "src/" + temp.index + "/" + name + ".mp3"

                txt_addr = temp.index + "/" + name + ".txt"
                # print(origin_path+txt_addr)
                file = open(origin_path + "/" + txt_addr, "r", encoding='UTF-8')
                lines = file.readlines()
                for line in lines:
                    if line.startswith('\"description\"', 0, len(line)):
                        # print(line)
                        # print(name)
                        i = 0
                        str1 = "《"
                        str2 = "》"
                        index1 = line.find(str1, i, len(line))
                        index2 = line.find(str2, i, len(line))
                        temp.name = line[index1 + 1:index2]
                        # print(temp.name)
                        i = index2

                        str1 = "由"
                        str2 = "演唱"
                        index1 = line.find(str1, i, len(line))
                        index2 = line.find(str2, i, len(line))
                        temp.singer = line[index1 + 2:index2 - 1]
                        # print(temp.singer)
                        i = index2

                        str1 = "收录于《"
                        str2 = "》"
                        index1 = line.find(str1, i, len(line))
                        index2 = line.find(str2, i, len(line))
                        if index2 == -1:
                            index2 = len(line - 1)
                            # print(name)
                        temp.CD = line[index1 + 4:index2]
                        # print(temp.CD)

                temp.singer_addr = "/singer/" + temp.singer
                temp.CD_addr = "/CD/" + temp.CD
                # print("###"+temp.CD_addr)

                if content in temp.CD:
                    datalist.append(temp)

                # print(temp.html_addr)
                # print(temp.pic_addr)
        # 遍历所有的文件夹
        for d in dirs:
            print(os.path.join(root, d))

    return render_template('catalog.html', datalist=datalist)


def walkChoice(choice=0, message=""):
    datalist = []
    indexlist = []

    origin_path = ".\static\src"
    path = origin_path

    for root, dirs, files in os.walk(origin_path):
        for d in dirs:
            #print(os.path.join(root, d))
            dirname, basename = os.path.split(os.path.join(root, d))
            indexlist.append(basename)

    for root, dirs, files in os.walk(path):
        split = "."
        # 遍历文件
        for filename in files:
            filepath = os.path.join(root, filename)
            name, category = os.path.splitext(filename)  # 分解文件扩展名
            dirname, basename = os.path.split(filepath)
            tmp_ls = dirname.lstrip(origin_path)

            if filename.endswith(".mp3"):
                temp = Data()
                temp.index = tmp_ls
                temp.html_addr = "/song/" + temp.index + "/" + name
                temp.pic_addr = "src/" + temp.index + "/" + name + ".png"
                temp.music_addr = "src/" + temp.index + "/" + name + ".mp3"
                txt_addr = temp.index + "/" + name + ".txt"

                file = open(origin_path + "/" + txt_addr, "r", encoding='UTF-8')
                lines = file.readlines()
                for line in lines:
                    if line.startswith('\"description\"', 0, len(line)):
                        # 提取歌名
                        i = 0
                        str1 = "《"
                        str2 = "》"
                        index1 = line.find(str1, i, len(line))
                        index2 = line.find(str2, i, len(line))
                        temp.name = line[index1 + 1:index2]
                        i = index2

                        # 提取歌手名
                        str1 = "由"
                        str2 = "演唱"
                        index1 = line.find(str1, i, len(line))
                        index2 = line.find(str2, i, len(line))
                        temp.singer = line[index1 + 2:index2 - 1]
                        i = index2

                        # 提取专辑名
                        str1 = "收录于《"
                        str2 = "》"
                        index1 = line.find(str1, i, len(line))
                        index2 = line.find(str2, i, len(line))
                        if index2 == -1:
                            index2 = len(line - 1)
                        temp.CD = line[index1 + 4:index2]

                        temp.singer_addr = "/singer/" + temp.singer
                        temp.CD_addr = "/CD/" + temp.CD

                if choice==2:
                    if temp.singer==message:
                        datalist.append(temp)
                if choice==3:
                    if temp.CD == message:
                        datalist.append(temp)

        # 遍历所有的文件夹
        for d in dirs:
            print(os.path.join(root, d))

    return render_template('catalog.html', datalist=datalist, indexlist=indexlist)


if __name__ == '__main__':
    app.run(debug=True)