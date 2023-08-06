import json, datetime, time, random
from datetime import datetime


class Parse():
    def sizes(text,sku):
        try:
            prod = json.loads(text)
            for line in prod['variantAttributes']:
                if sku == line['sku']:
                    productcode = line['code']
                    break

            availsizes = [] 
            availids = []
            for line in prod['sellableUnits']:
                if productcode == str(line['attributes'][1]['id']):
                    if line['stockLevelStatus'] == 'inStock':
                        try:
                            availsizes.append(str(line['attributes'][0]['value']))
                        except KeyError:
                            availsizes.append('ONE SIZE')

                        availids.append(str(line['attributes'][0]['id']))
            

            return {"sizes": availsizes,"ids":availids}
        except Exception as e:
            return 'error'

        
    def info(text,sku):
        try:
            if type(text) == str:
                price = None

                name = json.loads(text)['name']
                image = f"https://images.footlocker.com/pi/{sku}/large/{sku}.jpeg"
                prod = json.loads(text)
                for line in prod['variantAttributes']:
                    if sku == line['sku']:
                        productcode = line['code']
                        break

                for x in prod['sellableUnits']:
                    if productcode == str(x['attributes'][1]['id']):
                        price = str(x['price']['originalPrice'])

                
                info_dict = {"name": name,"price": price,"image": image}
                return info_dict
            else:
                return 'error'
        except Exception as e:
            return 'error'

    
    def launch(text):
        try:
            monthfixlist = []
            if '"displaycountdowntimer":true,"' in text.lower():
                jsontext = json.loads(text)
                launchdate = jsontext['variantAttributes'][0]['skuLaunchDate'].split(' GMT')[0]
                
                newmonth = datetime.strptime(launchdate.split(' ')[0], "%b")
                fixedmonth = str(newmonth.month)
                if len(fixedmonth) == 1:
                    monthfixlist.append('0')
                
                monthfixlist.append(fixedmonth)
                finalmonth = ''.join(monthfixlist)

                timenow = datetime.utcnow()
                filteredtimenow = timenow.strftime('%Y %m %d %H:%M:%S')

                fixinglist = []
                finalstringcheck = launchdate.split(' ')
                for z in finalstringcheck:
                    if len(z) == 4:
                        fixinglist.append(z)

                for p in finalstringcheck:
                    if len(p) != 4:
                        fixinglist.append(p)
                
                fixinglist[1] = finalmonth
                fixedfootsitetimestamp = ' '.join(fixinglist)
        
                coolprinterlocal = filteredtimenow.replace(':',' ')
                coolprintersite = fixedfootsitetimestamp.replace(':',' ')

                localcalc = 0
                splitloc = coolprinterlocal.split(' ')
                for x in splitloc:
                    unit = int(x)
                    xindex = splitloc.index(x)
                    if xindex == 0:
                        localcalc += (unit * 31556926)
                    elif xindex == 1:
                        localcalc += (unit * 2629743)
                    elif xindex == 2:
                        localcalc += (unit * 86400 )
                    elif xindex == 3:
                        localcalc += (unit * 3600)      
                    elif xindex == 4:
                        localcalc += (unit * 60)
                    elif xindex == 5:
                        localcalc += unit
                
                sitecalc = 0
                splitsite = coolprintersite.split(' ')
                for x in splitsite:
                    unit = int(x)
                    xindex = splitsite.index(x)
                    if xindex == 0:
                        sitecalc += (unit * 31556926)
                    elif xindex == 1:
                        sitecalc += (unit * 2629743)
                    elif xindex == 2:
                        sitecalc += (unit * 86400 )
                    elif xindex == 3:
                        sitecalc += (unit * 3600)      
                    elif xindex == 4:
                        sitecalc += (unit * 60)
                    elif xindex == 5:
                        sitecalc += unit      
                        
                launched = int(int(sitecalc) - int(localcalc))

                if launched > 0:
                    return launched
                else:
                    return 0
            else:
                return 0
        except Exception as e:
            return 'error'

    def random_size(text,sku):
        try:
            prod = json.loads(text)
            for line in prod['variantAttributes']:
                if sku == line['sku']:
                    productcode = line['code']
                    break

            availsizes = [] 
            availids = []
            for line in prod['sellableUnits']:
                if productcode == str(line['attributes'][1]['id']):
                    if line['stockLevelStatus'] == 'inStock':
                        try:
                            availsizes.append(str(line['attributes'][0]['value']))
                        except KeyError:
                            availsizes.append('ONE SIZE')

                        availids.append(str(line['attributes'][0]['id']))
            
            if len(availsizes) > 0:
                size = random.choice(availsizes)
                pid = random.choice(availids)
            else:
                size = 'oos'
                pid = 'oos'
            return {'size':size, 'pid': pid}
        except Exception as e:
            return 'error'

    def specific_size(text,sku,user_entries):
        try:
            prod = json.loads(text)
            for line in prod['variantAttributes']:
                if sku == line['sku']:
                    productcode = line['code']
                    break

            availsizes = [] 
            availids = []
            for line in prod['sellableUnits']:
                if productcode == str(line['attributes'][1]['id']):
                    if line['stockLevelStatus'] == 'inStock':
                        try:
                            availsizes.append(str(line['attributes'][0]['value']))
                        except KeyError:
                            availsizes.append('ONE SIZE')

                        availids.append(str(line['attributes'][0]['id']))
        except Exception as e:
            return 'error'



        passed_sizes = []
        passed_ids = []
        try:
            joined_sizes = ','.join(user_entries)

            split_sizes = joined_sizes.split(",")

            for x in split_sizes:
                for size in availsizes:
                    if x.lower() == size.lower():
                        passed_sizes.append(x)
            
            for x in passed_sizes:
                sizeindex = passed_sizes.index(x)
                passed_ids.append(availids[sizeindex])
            
            return {'size':passed_sizes, 'pid': passed_ids}
        except Exception as e:
            return 'error'