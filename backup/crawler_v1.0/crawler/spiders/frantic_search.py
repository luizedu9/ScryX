# -*- coding: utf-8 -*-

#   CIÊNCIA DA COMPUTAÇÃO
#
#   USO DE METAHEURÍSCA EM UMA FERRAMENTA DE COTAÇÃO PARA COMPRAS DE CARTAS DE MAGIC: THE GATHERING
#   
#   Luiz Eduardo Pereira    
#
#   frantic_search.py:
#   Este modulo extrai os dados necessarios das cartas 
#   É utilizado o site ligamagic como raiz para o scrapy

import scrapy

# GERA O LINK DA CARTA
def card_link_mount(card):
    return ('https://www.ligamagic.com.br/?view=cards%2Fsearch&card=' + card.replace(' ', '+'))

# GERA O LINK DA LOJA    
def store_link_mount(store):
    return ('https://www.ligamagic.com.br/' + store)

class LigamagicSpider(scrapy.Spider):
    name = 'frantic_search'
    start_urls = ['https://www.ligamagic.com.br/']

    # REFERENTE A CARTA
    def parse(self, response):

        cards = []
        card_file = open('crawler/requests/' + self.request, 'r', encoding="utf-8")
        cards = card_file.read().splitlines()
        card_file.close()
        
        for card in cards:
            if (str(card).strip()): # SE VAZIO, IGNORA
                card = card.split(" ", 1)[1] # IGNORA A QUANTIDADE DA CARTA
                yield scrapy.Request(url=card_link_mount(card), callback=self.parse_page, meta={'card': card})
        
    # REFERENTE A LOJA
    def parse_page(self, response):

        lines = response.xpath('//div[@class="e-col1"]/a')
        links = lines.xpath('./@href').extract()
        names = lines.xpath('./img/@title').extract()

        for link, name in zip(links, names):
            yield scrapy.Request(url=store_link_mount(link), callback=self.parse_item, meta={'card_store': (response.meta['card'], name)})

    # REFERENTE AOS VALORES DA CARTA EM DETERMINADA LOJA
    def parse_item(self, response):
        card, store = response.meta['card_store']

        # EXISTEM DOIS PADRÕES DE HTML, UM COM O MENU "EXTRA" E OUTRO SEM. ISSO INFLUENCIA EM QUAL INDEX DO 'TD' DEVE SER ESCOLHIDO PARA ENCONTRAR OS valueES
        option = response.xpath('//td[@class="tdHeader"]/text()').extract()
        op = 0
        if ("Extras" in option):
            op = 1

        tr = response.xpath('//*[starts-with(@onmouseover, "itemMouseOver")]')
        quantity = tr.xpath('./td[' + str(4 + op) + ']/text()').extract() # SE EXISTE O NO MENU A OPÇÃO "EXTRA", ENTÃO A QUANTIDADE DE CARTAS ESTARÁ LOCALIZADA NO TD[5]
        value = tr.xpath('./td[' + str(5 + op) + ']')

        for i in range(0, len(value)):
            if ('0 unid.' in quantity[i]): # NÃO EXISTE ESTOQUE DESTA CARTA
                pass
            elif ("desconto" in value[i].extract()): # POSSUI DESCONTO, MODO DE SCRAPYING DIFERENTE
                yield {'card': card, 'store': store, 'quantity': quantity[i].split()[0], 'value': (''.join(value[i].xpath('./font/text()').extract())).split()[1].replace('.', '').replace(',', '.')}
            else:
                yield {'card': card, 'store': store, 'quantity': quantity[i].split()[0], 'value': (''.join(value[i].xpath('./text()').extract())).split()[1].replace('.', '').replace(',', '.')}