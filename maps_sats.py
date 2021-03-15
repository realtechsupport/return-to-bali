# Python program to get an asset from a public folder on pCloud
# ------------------------------------------------------------------------------
# Python program to get a (the newest) image asset from a public folder on pCloud
# add real time data and create an Image
# Return to Bali - AI for Earth
# June 2020
# trying out asynch to do this
# https://lucumr.pocoo.org/2016/10/30/i-dont-understand-asyncio/
# https://xinhuang.github.io/posts/2017-07-31-common-mistakes-using-python3-asyncio.html#:~:text=2%20RuntimeWarning%3A%20coroutine%20foo%20was%20
#never%20awaited&text=This%20is%20because%20invoking%20foo,all%20previous%20tasks%20are%20finished.
# ------------------------------------------------------------------------------
import os, sys, re
import aiohttp, asyncio

#-------------------------------------------------------------------------------
async def get_map_sat(app, source_url):
    info = {}
    n_name = ''
    async with aiohttp.ClientSession() as session:
        #get the name of the latest map asset from the pCloud maps folder
        async with session.get(source_url) as resp:
            if(resp.status == 200):
                html = await resp.content.read()
                html = html.decode('utf-8')
                start = html.rfind('<script>')          #rfind... last entry
                end = html.rfind('</script>')
                script_s = html[start:end]
                #print(script_s)
                t_names = [stamps.start() for stamps in re.finditer('name', script_s)]
                t_starts = [stamps.start() for stamps in re.finditer('modified', script_s)]
                t_ends = [stamps.start() for stamps in re.finditer('\+0000', script_s)]

                for i in range (0, len(t_starts)):
                    t = script_s[t_starts[i]:t_ends[i]]
                    n = script_s[t_names[i]:t_starts[i]]
                    ts = (t.split('"')[-1]).strip()
                    n = n.split('"')[2]
                    info.update({ts : n})

                sorted_info = sorted(info.items(), key=lambda x:x[0])
                n_name = sorted_info[0][1]
                print('sat image time and name: ', sorted_info[0])
                source_url2 = source_url + n_name

        #download that latest asset
        async with session.get(source_url2) as resp:
            if(resp.status == 200):
                image = await resp.content.read()
                n_name = os.path.join(app.config['CONTEXT'], n_name)
                f = open(n_name, 'wb')
                f.write(image)
                f.close()
                print('\ngot latest map from pcloud: ', n_name)

    return(n_name)
loop = asyncio.get_event_loop()

#-------------------------------------------------------------------------------
