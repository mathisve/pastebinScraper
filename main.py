import os
import time
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

pastebin_public_page = "https://pastebin.com/archive"
save_folder = "/bins"


def scrapeArchive(link_history):
		response = requests.get(pastebin_public_page)
		content = BeautifulSoup(response.content, "html.parser")

		usable_links = []

		if(type(content) != None):
			try:
				maintable = content.find("table", {"class":"maintable"})
				for link in maintable.find_all("a"):
						sLink = str(link).split('"') #split link in array with " delimiter to get the link part
						nLink = "https://pastebin.com/raw" + sLink[1]
						if(nLink not in link_history):
							usable_links.append(nLink)
			except Exception as e:
				print(e)

			link_history = usable_links

		else:
			print("Content type is None, something is wrong!")
			exit()

		return usable_links, link_history


def main():
	os.chdir(os.getcwd() + save_folder)
	link_history = []
	iterations = 0

	while True:
		folder_dir = os.path.join(os.getcwd(), str(int(time.time())))
		os.mkdir(folder_dir)

		iterations += 1
		links, link_history = scrapeArchive(link_history)
		sleep_time = 120/len(links)
		
		print("{} iterations. {}sec per iteration - {}".format(iterations, round(sleep_time, 2), time.asctime()))
		for link in tqdm(links):
			try:
				response = requests.get(link)
				with open(os.path.join(folder_dir, link.split("/")[-1] + ".txt"), "w") as file:
					file.write(str(response.content).strip())
					file.close()
			except:
				pass

			time.sleep(sleep_time)


if __name__ == "__main__":
	main()