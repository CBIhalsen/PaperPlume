import openai
import tiktoken
import yaml
# 每次调用token+20
openai.api_key = "xxxx"
# recommend = "You are a robot that specializes in writing research papers, following these rules :{You only need to generate the paper and avoid output of any text that is not relevant to the paper. The language should be rigorous and precise. There should be no literature review in the paper. }"
# first_recommend = "You're a robot that generates Outlines for research papers.  You just need to generate a detailed thesis outline.  References cannot appear in the outline ;  Starting with a space to indicate the hierarchy;  Level 1 headings begin with Chinese characters.   Secondary headings begin with a number. "
#
# summary_commend = ''
def load_config():
    with open('./config/prompt.yaml', 'r',encoding='utf-8') as config_file:
        config = yaml.safe_load(config_file)
    return config

# 加载配置
config = load_config()


#  Level 1 headings begin with Chinese characters.


class chat:

    def __init__(self,language=None,style=None,reference=None,model='gpt-3.5-turbo'):
        self.encoding = tiktoken.encoding_for_model(model)
        self.model =model
        if language == 'zh-CN':
            print("zhongwen 语言")
            self.first_recommend = config['zhf_recommend']
            self.recommend = config['zh_recommend']

            self.Stop_sequences = ["注：","注意：","Note:","以上是"]
            self.temperature = 0.7
            self.top_p = 1
            # 0.4 1.8
            self.presence_penalty = 0
            self.frequency_penalty = 1.9
        elif language == 'zh-TW':
            self.first_recommend = config['zh_tcf_recommend']
            self.recommend = config['zh_tc_recommend']

            self.Stop_sequences =  ["注：", "備註:", "Note:", "備註："]
            self.temperature=0.5
            self.top_p=1


            self.presence_penalty=0.5
            self.frequency_penalty=1.6

        elif language == 'ja':
            self.first_recommend = config['jaf_recommend']
            self.recommend = config['ja_recommend']

            self.Stop_sequences =  ["注：", "Note：", "Note:", "このアウトラ"]
            self.temperature = 1
            self.top_p = 1
            # 0.4 1.8
            self.presence_penalty = 0.3
            self.frequency_penalty = 1.7

        else:
            self.first_recommend = config['enf_recommend']
            self.recommend = config['en_recommend']

            self.Stop_sequences =  ["注：", "Note：", "Note:", "備註："]
            self.temperature=0.5
            self.top_p=1
#0.4 1.8 0.3 1.7 0 1.7
            self.presence_penalty=0.2
            self.frequency_penalty=1.6


    def normal_chat(self, prompt, user_message=[], assistant_message=[]):
        # 限制历史记录长度
        # print(user_message, "nor user")
        # print(assistant_message, "nor sys")

        max_history = 10
        min_history = 9

        if len(assistant_message) > max_history:  # 历史长度最大为7
            assistant_message = [assistant_message[0]] + assistant_message[-min_history:]
            user_message = [user_message[0]] + user_message[-min_history:]
        messages = [{"role": "system", "content": config['normal_chat']}]

        for user_msg, system_msg in zip(user_message, assistant_message):
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": system_msg})



        # 检查总 token 数是否超出限制
        request_tokens = sum(len(self.encoding.encode(message['content'])) for message in messages)


        max_tokens = 1500
        if request_tokens > max_tokens:

            while request_tokens > max_tokens:

                if len(assistant_message) > 4:
                    del assistant_message[-4]
                    del user_message[-4]
                elif len(assistant_message) == 4:
                    del assistant_message[-3]
                    del user_message[-3]
                else:
                    del assistant_message[-2]
                    del user_message[-2]
                # 截断历史记录以适应模型的最大 token 数量
                # del history[-3:]
                del messages[1:]

                for user_msg, system_msg in zip(user_message, assistant_message):
                    messages.append({"role": "user", "content": user_msg})
                    messages.append({"role": "assistant", "content": system_msg})

                messages.append({"role": "user", "content": prompt})

        # request_tokens = sum(len(self.encoding.encode(message['content'])) for message in messages)

        messages.append({"role": "user", "content": prompt})
        # print(messages)
        print("normals model value")
        print(self.model)
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=1,
            max_tokens=600,
            top_p=1.0,
            frequency_penalty=0,
            presence_penalty=0

        )
        request_tokens = sum(len(self.encoding.encode(message['content'])) for message in messages)
        reply = response.choices[0].message['content']
        print('full response')
        print(response)
        response_tokens = len(self.encoding.encode(reply))
        total_tokens = request_tokens + response_tokens

        return reply, total_tokens + 30


    def summary_text(self,text):

        messages = [{"role": "system", "content": config['summary']}]
        messages.append({"role": "user", "content": text})
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.5
        )
        request_tokens = sum(len(self.encoding.encode(message['content'])) for message in messages)
        reply = response.choices[0].message['content']
        # testio = response.choices[0]
        response_tokens = len(self.encoding.encode(reply))
        total_tokens = request_tokens + response_tokens
        # history.append(reply)
        # print(history)
        return reply, total_tokens + 55


    def first_chat(self,prompt,title=None, history=[]):
        # 限制历史记录长度
        max_history = 8
        min_history = 7
        # print(len(history))
        #
        if len(history) == 1:
            history.append("Please note that the thesis title is:" + title)

        if len(history) > 2:
            history[-2], history[-1] = history[-1], history[-2]
        # print(history)
        if len(history) > max_history:  # 历史长度最大为7
            history = [history[0]] + history[-min_history:]
            # print(history)
            # print(len(history))

        messages = [{"role": "system","content": self.first_recommend}]    # 添加第一次的提示词到历史记录

        for message in history:
            messages.append({"role": "user", "content": message})

        messages.append({"role": "user", "content": prompt})
        # print(messages)
        # 检查总 token 数是否超出限制
        # request_tokens = sum(len(self.encoding.encode(message['content'])) for message in messages)
        # # print(title)
        # # print("First_Chat: ",request_tokens)
        # # print(history)
        # max_tokens = 2650
        # if request_tokens > max_tokens:
        #     # 截断历史记录以适应模型的最大 token 数量
        #     if len(history)>4:
        #         del history[-4]
        #     else:
        #         del history[-3]
            # (Note: The outline is written in Japanese as requested.)
            # del history[-4]  请注意，  以上是关于 Please note
            # Note: This outline is in Japanese, as requested.
        # 注意：このアウトラインは参考資料を含んでいません。ご了承ください。
        response = openai.ChatCompletion.create(

            model=self.model,
            messages=messages,
            temperature=0.5,
            max_tokens=1300,
            presence_penalty=0,
            stop= self.Stop_sequences
        )

        reply = response.choices[0].message['content']
        # print(response)
        print(response.usage['total_tokens'])
        # print(request_tokens)
        # testio = response.choices[0]
        # response_tokens = len(self.encoding.encode(reply))
        total_tokens =response.usage['total_tokens']
        history.append(reply)
        # print(history)
        return reply,total_tokens+30
    def chat_with_model(self,prompt, title=None ,messages=None):
        # 限制历史记录长度
        # max_history = 8
        # min_history = 7
        # # print(len(history))
        #
        # if title and len(history) == 1:
        #     history[0] = self.note+title+"\n"+history[0]
        #
        # if len(history) > max_history: #历史长度最大为9
        #     history = [history[0]] + history[-min_history:]
        #
        # messages = [{"role": "system", "content": self.recommend }]    #添加第一次的提示词到历史记录
        #
        # for message in history:
        #     messages.append({"role": "assistant", "content": message})

        messages.append({"role": "user", "content": prompt})

        # # 检查总 token 数是否超出限制
        # request_tokens =  sum(len(self.encoding.encode(message['content'])) for message in messages)
        # # print(total_tokens)
        # # print("history:",history)
        # max_tokens = 2650
        #
        # if request_tokens > max_tokens:
        #     # print("当前token数量:", request_tokens, "开始截断")
        #     i = 0
        #     while request_tokens > max_tokens:
        #         i = i+1
        #         if len(history) > 4:
        #             del history[-4]
        #         elif len(history) ==4:
        #             del history[-3]
        #         else:
        #             del history[-2]
        #         # 截断历史记录以适应模型的最大 token 数量
        #         # del history[-3:]
        #         del messages[1:]
        #
        #         for message in history:
        #             messages.append({"role": "assistant", "content": message})
        #
        #         messages.append({"role": "user", "content": prompt})
        #         # print("第{}截断后，history:".format(i),history)
        # request_tokens = sum(len(self.encoding.encode(message['content'])) for message in messages)

        print(messages)
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature= self.temperature,
            top_p=self.top_p,
            max_tokens=1300,
            presence_penalty=self.presence_penalty,
            frequency_penalty=self.frequency_penalty,
            stop=self.Stop_sequences

        )

        reply = response.choices[0].message['content']
        print(reply)

        # testio= "response.choices[0]"
        # response_tokens= len(self.encoding.encode(reply))
        # history.append(reply)
        total_tokens=response.usage['completion_tokens']
        # print(response.usage['completion_tokens'])
        print(total_tokens)

        del messages[-1]
        print(messages)
        return reply,total_tokens+55
