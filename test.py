# -*- coding: utf-8 -*-
import os
import sys
	
try:
	#questo crea un processo zombie, ma almeno il processo chiamante (la pagina php) può andare avanti
	if os.fork() > 0:
		print "Ricerca avviata"
		sys.exit(0)

	# elementi del nostro spider
	from spider.spiders.spider import MySpider
	from spider.gestioneDatabase import ManagerDB
	from spider import settings

	# scrapy api
	from scrapy import signals
	from twisted.internet import reactor
	from scrapy.crawler import Crawler
	from scrapy.settings import Settings
	from scrapy.utils.project import get_project_settings
	bloccaProcesso = reactor

	with open("log.txt", "a") as myfile:
		myfile.write("ok1")
		myfile.close()

	#creazione del gestore del database
	managerDB = ManagerDB()
	managerDB.connetti()

	#lista dei siti su cui avviare gli spider
	websites = managerDB.leggiUrl()

	# crawlers in esecuzione
	crawlers = []
	crawlersCompletati = 0;


	with open("log.txt", "a") as myfile:
		myfile.write("ok2")
		myfile.close()

	#funzione per gestire l'evento sulla chiusura dello spider
	def spider_closing(spider):
		crawlersCompletati = crawlersCompletati+1
		
		#se hanno completato tutti i gli esecutori degli spider chiudo il programma
		if crawlersCompletati == len(websites):
			print "finito"
			
			
			with open("log.txt", "a") as myfile:
				myfile.write("ok4")
				myfile.close()
		
			bloccaProcesso.stop()

	#per ogni sito lancio uno spider tramite un suo esecutore
	for i in range(len(websites)):	
		# crawl responsibly
		#settings.set("USER_AGENT", "Kiran Koduru (+http://kirankoduru.github.io)")

		#imposto le impostazioni
		setting = get_project_settings()
		setting.setmodule(settings, 300)
	
		#creo un nuovo esecutore di uno spider	
		crawler = Crawler(MySpider, setting)
	
		crawlers.append(crawler)
	
		#aggiungo all'esecutore dello spider una funzione sull'evento di chiusura dello spider
		crawler.signals.connect(spider_closing, signal=signals.spider_closed)
	
		#avvio dello spider passando gli appositi parametri
		crawler.crawl(websites[i][0], websites[i][1])
	
	
		with open("log.txt", "a") as myfile:
			myfile.write("ok3")
			myfile.close()
	
	#per bloccare il processo, altrimenti terminerebbe prima dei crawler
	bloccaProcesso.run()
except Exception as e:
	print e
