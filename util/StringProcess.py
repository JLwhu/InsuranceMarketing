import re

class StringProcess():
    def findColNames(self, text):
        colName_list = re.findall(r"@[A-Z,a-z,' ']+@", text)
        ret_list = []
        for colName in colName_list:
            colName = colName[1:-1]
            if colName not in ret_list:
                ret_list.append(colName)
        print(ret_list)
        return ret_list

    def replaceRegexWithString(self, regex, replace_str, text):
        re.sub(regex, replace_str, text)
        return text