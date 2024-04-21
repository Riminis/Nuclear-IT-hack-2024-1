from lib import *


class Main:
    file = 'MosTrans.xlsx'
    df = pd.read_excel(file, header=0)
    names_stations = []
    ban_words = []

    for i in range(len(df)):
        names_stations.append(df.iloc[i, 0])

    def get_val(self, name_station, date):
        date_gg = datetime.datetime(int(date[:4]), int(date[5:7]), int(date[8:10]))
        if date_gg <= self.df.columns.tolist()[3]:
            answer = []
            answer_st = []
            for i in range(len(self.df)):
                if name_station == self.df.iloc[i, 0]:
                    for j in range(len(self.df.columns.tolist())):
                        if date == str(self.df.columns.tolist()[j])[:10]:
                            answer.append(self.df.iloc[i, 2])
                            answer.append(self.df.iloc[i, j])
            if len(answer) == 2:
                answer_st.append(answer[-1])
                return answer_st
            return answer
        return False

    def get_vales(self, name_station, date_start, date_end):
        end_date = datetime.datetime(int(date_end[:4]), int(date_end[5:7]), int(date_end[8:10]))
        if end_date <= self.df.columns.tolist()[3]:
            answers = []
            j_start = -1
            i_start = -1
            for i in range(len(self.df)):
                s = 0
                n = 0
                if name_station == self.df.iloc[i, 0]:
                    for j in range(len(self.df.columns.tolist())):
                        if date_start == str(self.df.columns.tolist()[j])[:10]:
                            s += int(self.df.iloc[i, j])
                            j_start = j
                            i_start = i
                    answers.append(self.df.iloc[i, 2])
                    while str(self.df.columns.tolist()[j_start])[:10] != str(date_end):
                        s += int(self.df.iloc[i_start, j_start])
                        j_start -= 1
                        n += 1
                    n += 1
                    s += int(self.df.iloc[i_start, j_start])
                    answers.append(s // n)
                    answers.append(s)
            return answers
        return False

    def similar(self, s1):
        mx = -9999
        name_find_station = ''
        for elem in self.names_stations:
            matcher = SequenceMatcher(None, s1, elem)
            if matcher.ratio() * 100 > mx and matcher.ratio() * 100 > 70:
                mx = matcher.ratio() * 100
                name_find_station = elem
        return name_find_station

    def clean_string(self, sin):
        sin.split()
        answers = []
        for elem in sin:
            for ban_word in self.ban_words:
                if elem != ban_word:
                    answers.append(elem)
        return answers

    def predict(self, name_station, date):
        date_gg = datetime.datetime(int(date[:4]), int(date[5:7]), int(date[8:10]))
        if date_gg > self.df.columns.tolist()[3]:
            delta = datetime.timedelta(days=7)
            answers = []
            answers_st = []
            for i in range(len(self.df)):
                s = 0
                n = 0
                date_1 = datetime.datetime(int(date[:4]), int(date[5:7]), int(date[8:10]))
                if name_station == self.df.iloc[i, 0]:
                    bufer = str(self.df.columns.tolist()[3])
                    date_2 = datetime.datetime(int(bufer[:4]), int(bufer[5:7]), int(bufer[8:10]))
                    while date_1 >= date_2:
                        date_1 -= delta
                    for j in range(3, len(self.df.columns.tolist())):
                        if date_1 == self.df.columns.tolist()[j]:
                            date_1 -= delta
                            s += self.df.iloc[i, j]
                            n += 1
                    answers.append(self.df.iloc[i, 2])
                    answers.append(s // n)

            if len(answers) == 2:
                answers_st.append(answers[-1])
                return answers_st
            return answers
        return False

    def predicts(self, name_station, date_start, date_end):
        end_date = datetime.datetime(int(date_end[:4]), int(date_end[5:7]), int(date_end[8:10]))
        if end_date > self.df.columns.tolist()[3]:
            start_date = datetime.datetime(int(date_start[:4]), int(date_start[5:7]), int(date_start[8:10]))
            end_date = datetime.datetime(int(date_end[:4]), int(date_end[5:7]), int(date_end[8:10]))
            delta = datetime.timedelta(days=7)
            answers = []
            answers_st = []
            for i in range(len(self.df)):
                s = 0
                n = 0
                date_1 = datetime.datetime(int(date_start[:4]), int(date_start[5:7]), int(date_start[8:10]))
                if name_station == self.df.iloc[i, 0]:
                    bufer = str(self.df.columns.tolist()[3])
                    date_2 = datetime.datetime(int(bufer[:4]), int(bufer[5:7]), int(bufer[8:10]))
                    difference = end_date - start_date
                    while date_1 >= date_2:
                        date_1 -= delta
                    for j in range(3, len(self.df.columns.tolist())):
                        if date_1 == self.df.columns.tolist()[j]:
                            for _ in range(difference.days):
                                if j + _ < len(self.df.columns.tolist()):
                                    s += self.df.iloc[i, j + _]
                                    n += 1
                            date_1 -= delta
                    answers.append(self.df.iloc[i, 2])
                    answers.append(s // n)
                    answers.append(s)

            if len(answers) == 2:
                answers_st.append(answers[-1])
                return answers_st
            return answers
        return False


A = Main()
print(A.get_vales('Каширская', '2024-02-21', '2024-03-21'))
print(A.predicts('Каширская', '2025-02-21', '2025-03-21'))
