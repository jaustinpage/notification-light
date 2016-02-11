deps:
	virtualenv env
	sudo pip install -r requirements.txt
	git clone https://github.com/todbot/blink1
	cd blink1
	git checkout v1.98
	cd commandline
	make
	
	echo "Run source env/bin/activate"

clean:
	pyclean .

lint:
	pep8 --show-source --show-pep8 ./*.py

freeze:
		pip freeze > requirements.txt

init: deps clean
