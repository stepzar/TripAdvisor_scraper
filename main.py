import sys
import grequests
import requests
import base64
from bs4 import BeautifulSoup
import re
import pandas as pd

headers = {
  'authority': 'www.tripadvisor.it',
  'cache-control': 'max-age=0',
  'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
  'sec-ch-ua-mobile': '?0',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-user': '?1',
  'sec-fetch-dest': 'document',
  'referer': 'https://www.tripadvisor.it/Tourism-g194690-Benevento_Province_of_Benevento_Campania-Vacations.html',
  'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
  'cookie': 'TADCID=4_52EyQbydRi3R50ABQCFdpBzzOuRA-9xvCxaMyI12fz7wIvfRB_-t9VOMGXbsKp73ZVJKl_X4AZeVFuBRd2L_t9z0Q1kY4mAMs; TAUnique=%1%enc%3A4GpBN2qRxoqQVLNpFbWskie%2FWY7aGCigZz%2FXmR%2BS6Fk2jHwltRJPGQ%3D%3D; TASSK=enc%3AAHDix8xRjsbbddSTBZZ%2BoAhNhJZ1ssSAFdUvcZAozkqA2IMwtC%2FYq7P30OaRHf%2FZVjR%2BeUtm7AOAVvrL3H%2FAUwTbQ8S%2BMUk5I56%2Fj3bQGfqmPmaDFgTc2sjuC6ZlsIrZ1A%3D%3D; PMC=V2*MS.27*MD.20210904*LD.20210904; TART=%1%enc%3AkFSzaRW1rJLfq5r2qJVxU%2B%2F8IiGZT49q59PpwvbU5z9mMaYu97SO%2BqypifwYQhpKZQnMIP2Q3mY%3D; ak_bmsc=9E26BC3DD93B9CDAF50782D17648BAD9~000000000000000000000000000000~YAAQrQ4VAmjMQxB7AQAAbYypsQ0SKIPYs4WwJogrsFqAbTr80/PPfJGEuAzfmlTKLXfbSvW+TH0sBog6Y/gkiF+R0D4M29kJAL3SF7UT0x/tkxYD+Py1qavYjL67UXltEEl6vZWR1ExN6lq8g4B0q8apjl4zH1PochFF8XM8HWgWex8UGpq8tC/MLvZwBmJp0TY5koyWXS72Gl4epwQB8o2SrZ0tt85HbVjxpkJgFGasyxhUo7WkVXVNPljd3oG4V5tSoU+PL22nKhpszdkXwItOlqkG4fnNjDh6A74SuktWRhwWmfjh36fzNm6V2Ae1cjpMhvukYAu8xRvj6hZVCKza2bnYYquOHEL1px/nJaF/J2DrBk286hHHfk22XJWEoTcW7j1dnsxONf5oww==; _evidon_consent_cookie={"consent_date":"2021-09-04T16:34:44.509Z","categories":{"7":true},"vendors":{"7":{"14":true,"17":true,"31":true,"36":true,"51":true,"56":true,"58":true,"64":true,"66":true,"80":true,"81":true,"82":true,"99":true,"103":true,"131":true,"139":true,"167":true,"168":true,"174":true,"237":true,"242":true,"243":true,"249":true,"253":true,"257":true,"259":true,"265":true,"286":true,"290":true,"292":true,"298":true,"307":true,"310":true,"321":true,"322":true,"348":true,"355":true,"364":true,"384":true,"395":true,"412":true,"433":true,"442":true,"457":true,"459":true,"464":true,"474":true,"480":true,"516":true,"529":true,"550":true,"560":true,"564":true,"606":true,"608":true,"631":true,"633":true,"635":true,"650":true,"667":true,"674":true,"735":true,"831":true,"853":true,"905":true,"920":true,"921":true,"948":true,"1028":true,"1095":true,"1256":true,"1455":true,"1635":true,"1647":true,"1812":true,"1872":true,"1879":true,"1904":true,"1955":true,"2191":true,"2253":true,"2449":true,"2516":true,"2521":true,"2609":true,"2770":true,"2937":true,"3110":true,"3173":true,"3222":true,"3437":true,"3490":true,"3568":true,"3622":true,"3794":true,"3857":true,"3952":true,"3994":true,"4100":true,"4160":true,"4166":true,"4548":true,"4668":true,"4782":true,"4902":true,"5037":true,"5129":true,"5181":true,"5205":true,"5277":true,"5431":true,"6171":true,"6423":true,"6609":true}},"cookies":{"7":true},"consent_type":1}; TATrkConsent=eyJvdXQiOiIiLCJpbiI6IkFMTCJ9; TATravelInfo=V2*AY.2021*AM.9*AD.12*DY.2021*DM.9*DD.13*A.2*MG.-1*HP.2*FL.3*DSM.1630773481464*RS.1*RY.2021*RM.9*RD.4*RH.20*RG.2; TASID=BE3B2E8D02B04AB989031718177BA4DF; ServerPool=C; __vt=jIin8mFJ6ENfBI2aABQCIf6-ytF7QiW7ovfhqc-AvRfR5Hq3BpgrzDdKWh14NBPU0ogS4jMJ_cJpXkplnXlDn-l7r2zqiADaGoO92RVFJBtKglI_2FNuxtcZm8c2L5AMq4pKVraTlW6zcenedOQsDGq7gqo; PAC=ANQJEqQkEDx5sJ4WGpjxgySii7m_Xxnf5Z6ISB8zhQ3v7wSAhmgIcgv_6EWOZUpf8Rthclae6G2Y-6WOR_fOQC_ZHd5iBD_NM_UYlQ6qJKfCB2PUuBRXsHaKDKZWQjP1YuXcyGWfnXqgfLYp-q-loyezH1dzBqXMB5iDc2gpBKwbx-H5_dajxyB3RL59y7ux4w%3D%3D; VRMCID=%1%V1*id.10568*llp.%2F*e.1631383146323; TAReturnTo=%1%%2FRestaurants-g194690-Benevento_Province_of_Benevento_Campania.html; roybatty=TNI1625u0021AHH851swXPWBKeorfIaXGzk2dLjDlP31gM5IC5jJS36zXj%2BNkYS5QLsa1JGs4cajt5Ot6XPBVP2cI%2BKgP7JelZ8MLPosAY0KdRNohtYZYnYyMYi%2Bncz1WZ3zEfJMGcJI1ZV4lS5PhPbepNS6B%2Ffbd82gWtFyPKwmhsIHu3jXX1qv%2C1; TASession=V2ID.BE3B2E8D02B04AB989031718177BA4DF*SQ.16*LS.DemandLoadAjax*GR.45*TCPAR.10*TBR.99*EXEX.63*ABTR.49*PHTB.79*FS.62*CPU.24*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*FA.1*DF.0*TRA.true*LD.194690*EAU._; TAUD=LA-1630773286629-1*RDD-1-2021_09_04*HDD-194694-2021_09_12.2021_09_13*RD-5168937-2021_09_05.194690*LD-5186944-2021.9.12.2021.9.13*LG-5186946-2.1.F.; bm_sv=38321481CCEDC3AD2CCC4E98EC3DBD32~092e9MCVgj+vp3frxevOWM9DWX6f5oDV+hQ6rzjME5oyEQzEYKewMG9VmlbKcz5ayokfo9k4nXJsI0ZEebTQH05oWzLTGu/1yoSgYHO5IXKmrk3mWq5zd35ksf0Fe4+phv5P6onDg+lwv1vQXuscLqolPHWddtg3NTjgpizuGbE=; CM=%1%PremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CSLMCSess%2C%2C-1%7CCrisisSess%2C%2C-1%7CUVOwnersSess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CRepTarMCSess%2C%2C-1%7CCCSess%2C%2C-1%7CCYLSess%2C%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7CTSMCPers%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CTADORSess%2C%2C-1%7CAdsRetPers%2C%2C-1%7CCOVIDMCSess%2C%2C-1%7CListMCSess%2C%2C-1%7CTARSWBPers%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CSPACMCSess%2C%2C-1%7CRBAPers%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPremRPers%2C%2C-1%7CSLMCPers%2C%2C-1%7CRevHubRMPers%2C%2C-1%7CUVOwnersPers%2C%2C-1%7Csh%2C%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCrisisPers%2C%2C-1%7CCYLPers%2C%2C-1%7CCCPers%2C%2C-1%7CRepTarMCPers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CTSMCSess%2C%2C-1%7CSPMCPers%2C%2C-1%7CRevHubRMSess%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CAdsRetSess%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CCOVIDMCPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CTADORPers%2C%2C-1%7CSPACMCPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CTARSWBSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CListMCPers%2C%2C-1%7C; TASession=V2ID.BE3B2E8D02B04AB989031718177BA4DF*SQ.17*LS.Restaurants*GR.45*TCPAR.10*TBR.99*EXEX.63*ABTR.49*PHTB.79*FS.62*CPU.24*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*FA.1*DF.0*RT.0*TRA.true*LD.194690*EAU._; TAUD=LA-1630773286629-1*RDD-1-2021_09_04*HDD-194694-2021_09_12.2021_09_13*RD-5168937-2021_09_05.194690*LD-5258919-2021.9.12.2021.9.13*LG-5258921-2.1.F.; bm_sv=38321481CCEDC3AD2CCC4E98EC3DBD32~092e9MCVgj+vp3frxevOWM9DWX6f5oDV+hQ6rzjME5oyEQzEYKewMG9VmlbKcz5ayokfo9k4nXJsI0ZEebTQH05oWzLTGu/1yoSgYHO5IXK29XMvt0pvC//cQ0yHCDtBQffjPUJsjqEsab5FUQ7gQ3MfalR1wd3R/z5U6u2HFkk=; TASID=BE3B2E8D02B04AB989031718177BA4DF'
}

def get_pages_urls(url):
    urls = [url]
    codice = re.search("-g\d+-", url).group(0)
    link = url.replace(codice, codice + "oa30-")
    urls.append(link)
    for x in range(60, 500, 30):
        new_link = re.sub(r"-oa\d+-", "-oa" + str(x) + "-", link)
        urls.append(new_link)

    return urls


def get_locals_urls(r):
    s = BeautifulSoup(r.text, "lxml")

    lista = s.find("div", {"data-test-target":"restaurants-list"})

    regex = re.compile('.*_list_item')
    locali = lista.find_all("div", {"data-test":regex})

    urls = []
    for locale in locali:
        link = locale.find("a")["href"]
        urls.append("https://www.tripadvisor.it" + link)

    return urls


def get_data(urls):
    # for every pages
    reqs = [grequests.get(link, headers=headers) for link in urls]
    resp = grequests.map(reqs)

    count = 1
    responses = []
    for r in resp:
        if r.url == url and count != 1:
            break

        responses.append(r)
        count += 1

    l = len(responses)
    print(f"Found {l} pages:")
    resps = []

    for i, r in enumerate(responses):
        reqs_locals = [grequests.get(link, headers=headers) for link in get_locals_urls(r)]
        resp_locals = grequests.map(reqs_locals)
        resps.append(resp_locals)
        sys.stdout.write(f"\r{round(float(i/l)*100)} %")
        sys.stdout.flush()

    return resps    # all response of all locals


def get_local_info(resps):
    locali = []
    for i, x in enumerate(resps):
        for j, r in enumerate(x):
            s = BeautifulSoup(r.text, "lxml")
            try:
                nome = s.find("h1", {"data-test-target":"top-info-header"}).text
            except:
                continue

            s = s.find("div", {"data-tab":"TABS_OVERVIEW"}).find("div").find_all("div", recursive=False)[2].find("div").find("div")

            h2 = s.find("h2")

            indirizzo = h2.find_next_siblings()[1].text

            facebook = ""
            try:
                divs = h2.find_next_siblings()[2:]
                for div in divs:
                    if len(div.find_all("div", recursive=False)) > 1:
                        sito = div.find_all("div", recursive=False)[0].find("a")["data-encoded-url"]

                        base64_bytes = sito.encode('ascii')
                        message_bytes = base64.b64decode(base64_bytes)
                        sito = message_bytes.decode('ascii')[4:-5]

                        if sito[-1] == 'i':
                            sito += "t"
                        if sito[-2:] == "co":
                            sito += "m"

                        if sito.startswith("https://www.facebook.com") or sito.startswith("http://www.facebook.com"):
                            facebook = sito
                            sito = ""
            except:
                sito = ""

            try:
                telefono = h2.find_next_siblings("div")[-1].find("a")["href"].strip().replace("tel:+39", "")
            except:
                telefono = ""

            locale = {"nome":nome, "link":r.url, "indirizzo":indirizzo, "sito":sito, "facebook":facebook,"telefono":telefono}
            #print(locale)
            locali.append(locale)
            sys.stdout.write(f"\rPage {i} : {round(float(j/len(x))*100)} %")
            sys.stdout.flush()

    return locali


if __name__ == '__main__':
    # search on google
    scelta = input("Ricerca (formato: città attività): ")
    scelta += " tripadvisor"
    query = scelta.replace(" ","+")
    r = requests.get(f"https://www.google.com/search?q={query}", headers=headers)
    s = BeautifulSoup(r.text, "lxml")
    url = s.find("div", {"class":"g"}).find("a")["href"]
    #print(url)

    # scraping
    pages_urls = get_pages_urls(url)

    resp = get_data(pages_urls)
    print("\n\nStarting scraping...")
    locals = get_local_info(resp)

    # saving the csv
    df = pd.DataFrame(locals)
    nome_file = scelta.replace(" tripadvisor", "").replace(" ","-")
    df.to_csv(nome_file + ".csv")



