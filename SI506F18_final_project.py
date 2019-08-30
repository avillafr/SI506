import requests
import json
import csv

NYT_API_KEY = '694d81930a324098a1229a74a3487692'
GUARDIAN_API_KEY = '7a3019f7-486b-429c-88f0-91b23ae1692e'

CACHE_FNAME = 'cache1.json'

try:
    file_obj = open(CACHE_FNAME,'r')
    file_contents = file_obj.read()
    CACHE_DICTION = json.loads(file_contents)
    file_obj.close()
except:
    CACHE_DICTION = {}
# I am using code I wrote from Problem Set 10.

def params_unique_combination(baseurl, params_d, private_keys=["api_key"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)
# I am using code given to us from Problem Set 10.

def get_NYT(query_item):
    baseurl = 'http://api.nytimes.com/svc/search/v2/articlesearch.json'
    parameter = {}
    parameter['api-key'] = NYT_API_KEY
    parameter['q'] = query_item
    unique_ident = params_unique_combination(baseurl,parameter)

    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]

    else:
        resp = requests.get(baseurl, params = parameter)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

python_object = get_NYT('Houston Astros')
x = json.dumps(python_object)
a_dictionary = python_object['response']['docs'][7]
# I am using code we did together during Discussion Section 13.

def get_Guardian(query):
    base = 'https://content.guardianapis.com/search'
    param_dict = {}
    param_dict['api-key'] = GUARDIAN_API_KEY
    param_dict['q'] = query
    unique_id = params_unique_combination(base, param_dict)

    if unique_id in CACHE_DICTION:
        return CACHE_DICTION[unique_id]

    else:
        resp = requests.get(base, params = param_dict)
        CACHE_DICTION[unique_id] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_id]

python = get_Guardian('Houston Astros')
y = json.dumps(python)
dictionary = python['response']['results'][9]
# I am using code similar to what we did together during Discussion Section 13.

class NYTArticle(object):

    def __init__(self, a_dictionary):
        self.title = a_dictionary['headline']['main']
        for item in a_dictionary:
            try:
                self.author = a_dictionary['byline']['original']
            except:
                self.author = 'by an Unkown Author'
        self.url = a_dictionary['web_url']
        self.document_type = a_dictionary['document_type']
        self.score = a_dictionary['score']
        for item in a_dictionary:
            try:
                self.sectionname = a_dictionary['section_name']
            except:
                self.sectionname = 'Unkown Section'
        self.snippet = a_dictionary['snippet']
        for item in a_dictionary:
            try:
                self.pub_date = a_dictionary['pub_date']
            except:
                self.pub_date = 'Unkown Publication Date'
    # I am using code similar to what I wrote in Problem Set 11.

    def len_of_snippet(self):
        length = len(self.snippet)
        return length

    def len_title(self):
            length = len(self.title)
            return length

    def csv_row_lst(self):
        lst_result = [self.title, self.sectionname, self.url, self.pub_date, self.len_title()]
        return lst_result
    # I am using code given to us from Lecture 23.

    def __str__(self):
        return "The article '{}' written {} has a score of {} on the New York Times.".format(self.title, self.author, self.score)

one_instance = NYTArticle(a_dictionary)
# print(one_instance)
print(one_instance.len_of_snippet())
# print(one_instance.len_title())

class GuardianArticle(object):

    def __init__(self, dictionary):
        self.title_name = dictionary['webTitle']
        self.weburl = dictionary['webUrl']
        self.documenttype = dictionary['type']
        self.section = dictionary['sectionName']
        self.pubdate = dictionary['webPublicationDate']
    # I am using code similar to what I wrote in Problem Set 11.

    def most_common_letter(self):
        common_lett = {}
        for item in self.title_name:
            if item != " ":
                if item in common_lett:
                    common_lett[item] = common_lett[item] + 1
                else:
                    common_lett[item] = 1
        keys = list(common_lett.keys())
        largest = keys[0]
        for this in keys:
            if common_lett[item] > common_lett[largest]:
                largest = this
        return largest
    # I am using code I wrote from Problem Set 11.

    def len_of_title(self):
        length = len(self.title_name)
        return length

    def csv_lst(self):
        lst = [self.title_name, self.section, self.weburl, self.pubdate, self.len_of_title()]
        return lst
    # I am using code given to us from Lecture 23.

    def __str__(self):
        return "The title '{}' is a/an {} document type and has a publication date of {} on the Guardian.".format(self.title_name, self.documenttype, self.pubdate)

instance = GuardianArticle(dictionary)
# print(instance)
print(instance.most_common_letter())
# print(instance.len_of_title())

article_instances = []
for inst in python_object['response']['docs']:
    article_instances.append(NYTArticle(inst))
# print(article_instances[0])
for inst in article_instances:
	print(inst)
# I am using code given to us from Lecture 23.

art_instances = []
for instance in python['response']['results']:
    art_instances.append(GuardianArticle(instance))
# print(article_instances[0])
# print('Guardian Instances Begin')
for insta in art_instances:
	print(insta)
# I am using code similar to what was given to us from Lecture 23.

with open('articles.csv', 'w', newline = '') as csvfile:
    samplecsvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
    samplecsvwriter.writerow(['Article Title', 'Section', 'Website', 'Publication Date', 'Number of Characters in Title'])
    for each_inst in article_instances:
        samplecsvwriter.writerow(each_inst.csv_row_lst())
    for each in art_instances:
        samplecsvwriter.writerow(each.csv_lst())
# I am using code similar to what was given to us from Lecture 23.
