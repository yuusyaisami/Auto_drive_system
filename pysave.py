import os
class SaveText:
    def __init__(self):
        pass
    # add関数は変数を保存する関数です
    # 引数は変数名 : name , データ : data , ファイルパス : pathです
    # nameに ":" を入れないでください
    # nameをFalseまたはTrueにしないでください
    # 同じ名前がある場合上書き保存をしなかった場合新しく変数を作ります
    def add(self, name, data, path):
        self.create_text_file(path)
        lines = []
        name_lines = []
        data_lines = []
        if os.path.isfile(path):
            lines = self.textfile_data_list(path) # textfile内のデータを行ずつリストに入れる
            self.clear(path) # ファイル内を削除
            name_lines, data_lines = self.separate_data_and_names(lines) # name と dataでリストに分ける
            existvariable = False
            for lineindex in range(len(lines)):
                if name_lines[lineindex] == name: # 同じ名前のリストを探す
                    existvariable = True
                    name_lines[lineindex] = str(name) # namelistに変数名を書き込む
                    data_lines[lineindex] = str(data) # datalistに新しいデータを書き込む
                    break
            if not existvariable: # 変数が存在しなかったら
                name_lines.append(str(name)) # 変数を追加する
                data_lines.append(str(data))
            self.write_to_text_file(name_lines, data_lines, path) # テキストファイルにnameとdataを関連させて保存する

    def delete(self,name, path):
        lines = []
        name_lines = []
        data_lines = []
        if os.path.isfile(path):
            lines = self.textfile_data_list(path)
            self.clear(path)
            name_lines, data_lines = self.separate_data_and_names(lines)
            for lineindex in range(len(lines)):
                if name_lines[lineindex] == name:
                    del name_lines[lineindex]
                    del data_lines[lineindex]
                    break
        self.write_to_text_file(name_lines, data_lines, path)
    # typeは出力時の変数の型を指定するための引数です
    # 初期値はstring or bool string型またはbool型で出力します
    # int はint型で出力します
    # float はfloat型で出力します
    # bool はbool型で出力します
    # string はstring型で出力します
    def search(self,name , path, type = "string or bool"):
        """type: int, float, bool, string"""
        lines = []
        name_lines = []
        data_lines = []
        if os.path.isfile(path):
            lines = self.textfile_data_list(path)
            name_lines, data_lines = self.separate_data_and_names(lines)
            for lineindex in range(len(lines)):
                if name_lines[lineindex] == name:
                    if type == "string or bool":
                        if data_lines[lineindex] == "True":
                            return True
                        if data_lines[lineindex] == "False":
                            return False
                        return data_lines[lineindex]
                    if type == "int":
                        return int(data_lines[lineindex])
                    if type == "float":
                        return float(data_lines[lineindex])
                    if type == "bool":
                        if data_lines[lineindex] == "True":
                            return True
                        if data_lines[lineindex] == "False":
                            return False
                    if type == "string":
                        return data_lines[lineindex]
    def create_text_file(self,path):
        with open(path, 'r', encoding='utf-8') as file:
            pass

    # 開発者用
    def clear(self,path):
        with open(path, 'w', encoding='utf-8') as file:
            file.write('')  # ファイルの内容を削除
    def textfile_data_list(self,path):
        lines = []
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                lines.append(line.strip()) # すべてのデータをlistに追加する
        return lines
    def separate_data_and_names(self,lines):
        """name と dataでリストに分ける"""
        name_lines = []
        data_lines = []
        for line in lines:
            try:
                namelength = line.index(":")
                datalength = len(line)
                name_lines.append(line[:namelength])
                data_lines.append(line[namelength + 1:datalength])
            except:
                pass
        return name_lines, data_lines
    def write_to_text_file(self,name, data, path):
        with open(path, 'w', encoding='utf-8') as file:
            for index in range(len(name)):
                file.write(name[index] + ":" + data[index] + '\n')  # 各要素を一行ずつ書き込む
if __name__ == '__main__':
    sv = SaveText()
    sv.create_text_file("savedata.txt")
    newvariable = 120
    newvariable_modoki = 10
    hanbetuD = True
    print("----------------ファイル入出力前--------------------")
    print("modoki" + " : " + str(newvariable_modoki))
    print("not modoki" + " : " + str(newvariable))
    sv.add("newvariable", newvariable, "savedata.txt")
    sv.add("D", hanbetuD, "savedata.txt")
    sv.add("pokemon", 11, "savedata.txt")
    sv.add("dorakue", 110, "savedata.txt")
    sv.add("ぴゅーた", 2525, "savedata.txt")

    print("----------------ファイル入出力あと--------------------")
    newvariable_modoki = sv.search("newvariable", "savedata.txt", "int") + 10
    hanbetuD = sv.search("D", "savedata.txt")
    print("modoki" + " : " + str(newvariable_modoki))
    print("not modoki" + " : " + str(newvariable))
    print(sv.search("ぴゅーた", "savedata.txt"))
    print(hanbetuD)