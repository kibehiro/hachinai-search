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
            for j in i[1]['スキル']:
                if skill in j:
                    search_result.append(i)
                    break

        self.search_json_data = search_result

    def search_talent(self, talent):
        search_result = []

        for i in self.search_json_data:
            for j in i[1]['才能']:
                if talent in j:
                    search_result.append(i)
                    break

        self.search_json_data = search_result

    def search_cinderella_card(self, cinderella):
        search_result = []

        for i in self.search_json_data:
            for j in i[1]['デレスト'].values():
                if cinderella in j[1]:
                    search_result.append(i)
                    break

        self.search_json_data = search_result
