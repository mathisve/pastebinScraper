import os
import time
import requests

from bs4 import BeautifulSoup

from tqdm import tqdm

pastebin_public_page = "https://pastebin.com/archive"
save_folder = "/bins"

history_depth = 5


def scrapeArchive(link_history):
		response = requests.get(pastebin_public_page)
		content = BeautifulSoup(response.content, "html.parser")

		usable_links = []

		if(type(content) != None):
			try:
				maintable = content.find("table", {"class":"maintable"})
				for link in maintable.find_all("a"):
						sLink = str(link).split('"')
						nLink = "https://pastebin.com/raw" + sLink[1]

						in_history = False
						for x in link_history:
							if(nLink in x):
								in_history = True
								break

						if(in_history == False):		
							usable_links.append(nLink)

			except Exception as e:
				print(e)

			if(len(usable_links) != 0):
				link_history.append(usable_links)
				if(len(link_history) >= history_depth):
					link_history.pop(0)

		else:
			print("Content type is None, something is wrong!")
			exit()

		return usable_links, link_history


def main():
	os.chdir(os.getcwd() + save_folder)
	link_history = []
	iterations = 0

	while True:
		iterations += 1
		links, link_history = scrapeArchive(link_history)
		if(len(links) != 0):

			folder_dir = os.path.join(os.getcwd(), str(int(time.time())))
			os.mkdir(folder_dir)

			sleep_time = 60/len(links)
		
			print("{} iterations. {}sec per iteration. {} new links found - {}".format(iterations, round(sleep_time, 2),len(links), time.asctime()))
			for link in tqdm(links):
				try:
					response = requests.get(link)
					with open(os.path.join(folder_dir, link.split("/")[-1] + ".txt"), "w") as file:
						file.write(str(response.content).strip())
						file.close()
				except:
					pass

				time.sleep(sleep_time)

		else:
			print("{} iterations. No new links found, sleeping ...".format(iterations))
			time.sleep(30)


if __name__ == "__main__":
	main()