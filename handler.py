#from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import re
import json
import datetime

class Tools:
	def __init__(self):
		self.df = pd.read_csv('/home/mbib/mysite/all_data.csv', sep=';').fillna('')
		self.df["GroupId"] = self.df.groupby(['nfull']).ngroup()

	def save_res(self, formres):
		formres = dict(formres)
		fullname = re.sub('ё', 'е', formres['nfull'][0].lower())
		fullname = fullname.capitalize()
		ff = open('is_unique.txt', 'a', encoding='utf-8')
		if fullname in list(self.df['nfull'].unique()):
			mygroup = self.df[self.df['nfull'] == fullname].iloc[0]
			groupid = mygroup['GroupId']
			ff.write(fullname + " is already catched with id " + str(groupid) + "\n")
			formres['GroupId'] = groupid
		else:
			groupid = int(self.df['GroupId'].max()) + 1
			ff.write(fullname + " is new and unique with id " + str(groupid) + "\n")
			formres['GroupId'] = groupid
		ff.close()
		clean_form = {}
		for f in list(formres.keys()):
		    x = formres[f]
		    if isinstance(x, list):
		        x = x[0]
		    if f == "opinion":
		        fc = open("comments.txt", "a", encoding="utf-8")
		        fc.write(">>>>>>\n" + fullname + "\n" + str(datetime.datetime.now()) + "\n" + x + "\n<<<<<<")
		        fc.close()
		    else:
		        clean_form[f] = x
		self.df = self.df.append(clean_form,ignore_index=True)
		self.df.to_csv('/home/mbib/mysite/all_data.csv', sep=';', index=False)

		return groupid


	def create_cloud(self, all_occ, groupid):
		text = ' '.join(all_occ)
		cloud = WordCloud(background_color="white", max_words=2000)
		cloud.generate(text)
		plt.imshow(cloud, interpolation='bilinear')
		plt.axis("off")
		cloud_name = "cloud_" + str(groupid) + ".jpg"

		cloud.to_file("/home/mbib/mysite/static/" + cloud_name)
		return cloud_name

	def create_visuals_ind(self, name, groupid):
		my_name = self.df[self.df["nfull"] == name]
		answers_num = my_name.shape[0]
		all_occ = []
		for c in ['nfull', 'nshort', 'rname1', 'dname1', 'dname2', 'dname3', 'oname1', 'oname2', 'oname3', 'jname1', 'jname2', 'jname3', 'oldname']:
			all_occ += my_name[c].tolist()
		cloud_name = self.create_cloud(all_occ, groupid)
		return answers_num, cloud_name

	def create_piechart(self, df, param, titel):
		plt.figure(figsize=(7, 7))
		df[param].value_counts().plot(kind='pie');
		plt.title(titel)
		pie_name = "/home/mbib/mysite/static/" + param + "_collected.png"
		plt.savefig(pie_name)
		return pie_name

	def display_all(self):
		self.create_piechart(self.df, 'nfull', "Names collected")
		self.create_piechart(self.df, 'ngender', "Genders collected")

		dnames = dict(self.df['nfull'].value_counts())
		#genders = dict(self.df['nfull'].value_counts())
		lnames = []
		for name in set(list(dnames.keys())):
			lnames.append([name, dnames[name], 'cloud_' + str(self.df[self.df['nfull'] == name].iloc[0]["GroupId"]) + ".jpg"])
		return lnames

