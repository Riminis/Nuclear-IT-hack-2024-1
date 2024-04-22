from tg_bot import *


class Main:
    file = 'MosTrans.xlsx'
    df = pd.read_excel(file, header=0)
    names_stations = []
    ban_words = ["Сколько", "сколько", "Много", "много", "люди", "людей", "ли", "было", "будет", "на", "станции",
                 "станция", "встреча", "метро", "народу", "народ", "количество", "какое", "Какое", "там", "Я", "я"]
    for i in range(len(df)):
        names_stations.append(df.iloc[i, 0])

    def get_val(self, name_station, date):
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
        words = s1.split()
        mx = -9999
        name_find_station = ''
        for i in range(len(words)):
            for elem in self.names_stations:
                matcher = SequenceMatcher(None, words[i], elem)
                if matcher.ratio() * 100 > mx and matcher.ratio() * 100 > 70:
                    mx = matcher.ratio() * 100
                    name_find_station = elem

        return name_find_station

    def clean_string(self, sin):
        words = sin.split()
        answers = []
        for elem in words:
            flag = 1
            for ban_word in self.ban_words:
                if elem == ban_word:
                    flag = 0
            if flag == 1:
                answers.append(elem)
        # ''.join(map(str, words))
        return ' '.join(map(str, answers))

    def predict(self, name_station, date):
        if date[3] == '2':
            return 0
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


def trim_list(input_list, start_index, end_index):
    return input_list[:start_index] + input_list[end_index + 1:]


def find_date_in_parts(input_str):
    words = input_str.split()
    A = []
    for i in range(len(words)):
        for j in range(len(words), i + 1, -1):
            partial_str = ' '.join(words[i:j])
            parsed_date = dateparser.parse(partial_str, settings={'PREFER_DATES_FROM': 'past'}, languages=['ru'])
            if parsed_date:
                A.append(parsed_date.strftime('%Y-%m-%d'))
                words = trim_list(words, i, j)
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            partial_str = ' '.join(words[i:j])
            parsed_date = dateparser.parse(partial_str, settings={'PREFER_DATES_FROM': 'past'}, languages=['ru'])
            if parsed_date:
                A.append(parsed_date.strftime('%Y-%m-%d'))
    if len(A) == 0:
        return None
    return A


def query(s, chat_id):
    x = Main()
    sentence = 'a ' + x.clean_string(s) + ' a'
    stantion = str(x.similar(sentence))
    a = find_date_in_parts(sentence)
    if a is None or stantion == '':
        bot.send_message(chat_id, "К сожалению мы не смогли обработать ваш запрос.\n"
                                  "Пожалуста попробуйте переформулировать ваш запрос и написать его снова.")
        return
    elif len(a) == 1 or a[0] == a[1]:
        data = a[0]
        val = 0
        gener = 0
        if data is not None and stantion is not None:
            val = x.get_val(stantion, data)
            if len(val) == 0:
                gener = 1
                val = x.predict(stantion, data)
        valstr = ''
        if len(val) == 1:
            valstr = str(val[0])
        else:
            for i in range(0, len(val), 2):
                valstr = valstr + '*' + str(val[i]) + '-' + str(val[i+1]) + "\n"
        if gener == 0:
            text = (data + " числа, на станции " + stantion + " было следущее количество пасажиров:\n " + str(valstr))
        else:
            text = ("Могу предположить что " + data + " числа на станции " + stantion +
                    " будет следущее количество пасажиров: \n" + str(valstr))
        bot.send_message(chat_id, text)
    elif len(a) > 1:
        data1 = a[0]
        data2 = a[1]
        gener = 0
        u = datetime.datetime(int(data2[:4]), int(data2[5:7]), int(data2[8:10]))
        y = datetime.datetime(int(data1[:4]), int(data1[5:7]), int(data1[8:10]))
        print(data1, data2, 'k')
        if u > y:
            val = x.get_vales(stantion, data1, data2)
        else:
            val = x.get_vales(stantion, data2, data1)
        if val == 0:
            gener = 1
            if u > y:
                val = x.predicts(stantion, data1, data2)
            else:
                val = x.predicts(stantion, data2, data1)
        print(val)
        valstr = ''
        for i in range(0, len(val), 3):
            valstr = (valstr + '*' + str(val[i]) + '| среднее - ' + str(val[i + 1]) + "\n*" +
                      str(val[i]) + "|сумма за всё время - " + str(val[i+2]) + "\n")
        if gener == 0:
            bot.send_message(chat_id, "C " + data1 + " по " + data2 + " на стнации " + stantion +
                             " побывало следующие количество пасажиров:\n" + valstr)
        else:
            bot.send_message(chat_id, "Предположительно, c " + data1 + " по " + data2 + " на стнации " + stantion +
                             " побывало следующие количество пасажиров:\n" + valstr)
