import os
import time
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

pastebin_public_page = "https://pastebin.com/archive"
save_folder = "/bins"

def scrapeArchive():
		response = requests.get(pastebin_public_page)
		content = BeautifulSoup(response.content, "html.parser")

		usable_links = []

		if(type(content) != None):
			maintable = content.find("table", {"class":"maintable"})
			for link in maintable.find_all("a"):
				try:
					sLink = str(link).split('"') #split link in array with " delimiter to get the link part
					usable_links.append("https://pastebin.com/raw" + sLink[1])
				except Exception as e:
					print(e)
		else:
			print("Content type is None, something is wrong!")
			exit()

		return usable_links


def main():
	os.chdir(os.getcwd() + save_folder)
	while True:
		folder_dir = os.path.join(os.getcwd(), str(int(time.time())))
		os.mkdir(folder_dir)
		links = scrapeArchive()

		sleep_time = 120/len(links)
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