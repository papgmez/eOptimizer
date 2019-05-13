run:
	cd app/ && python3 run.py runserver -h 172.31.81.252 -p 5000 -d
local:
	cd app/ && python3 run.py runserver -d
test:
	cd app/ && nosetests test/
install:
	 pip3 install -r requirements.txt
clean:
	$(RM) -rf $(shell find . -name *~)
	$(RM) -rf $(shell find . -name *pyc)
	$(RM) -rf *~ *.pyc
	$(RM) -rf app/__pycache__
	$(RM) -rf app/config/__pycache__
	$(RM) -rf app/helpers/__pycache__
	$(RM) -rf app/test/__pycache__
	$(RM) -rf app/test/factories/__pycache__
	$(RM) app/simulations/*
	$(RM) app/consumptions/*
