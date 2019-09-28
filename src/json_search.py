class JsonSearch:

    def __init__(self, json_data):
        self.search_json_data = []
        # 検索しやすい形にデータを変更
        for i in json_data:
            for j in i[1]:
                self.search_json_data.append([i[0], j])

    def search_element(self, element):
        search_result = []
        for i in self.search_json_data:
            for j in i[1]['属性']:
                if j in element:
                    search_result.append(i)

        self.search_json_data = search_result

    def search_name(self, name):
        search_result = []
        for i in self.search_json_data:
            if name in i[1]['カード名']:
                search_result.append(i)

        self.search_json_data = search_result

    def search_skill(self, skill):
        search_result = []
        for i in self.search_json_data:
            flag = 0  # 検索に使うFlag
            for j in skill:  # 検索したいワードの方を回す
                for k in i[1]['スキル']:  # 今検索しているカードのスキルを一つ一つ見ていく(計算効率最悪)
                    if j in k:  # もし、検索したいワードが今のスキル名に含まれていたらFlagを追加
                        flag += 1
                        break
            if flag == len(skill):  # flagが検索スキル数と同じ、つまり全ての検索ワードにヒットしていたら検索しているカードを検索結果に追加
                search_result.append(i)
        self.search_json_data = search_result

    def search_talent(self, talent):
        search_result = []
        for i in self.search_json_data:
            flag = 0
            for j in talent:
                for k in i[1]['才能']:
                    if j in k:
                        flag += 1
                        break
            if flag == len(talent):
                search_result.append(i)
        self.search_json_data = search_result

    def search_cinderella_card(self, cinderella):
        search_result = []
        for i in self.search_json_data:
            for j in i[1]['デレスト'].values():
                if cinderella in j[1]:
                    search_result.append(i)
                    break

        self.search_json_data = search_result
