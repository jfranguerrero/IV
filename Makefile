install:
	pip install -r requirements.txt

test:
	cd vuelaBot && python test_vuelabot.py

execute:
	cd vuelaBot && python vuelabot.py
