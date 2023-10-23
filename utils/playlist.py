
def PlaylistCount(url):
    if not '/playlist?' in url: url = pUrl + 'UU' + url.split('/UC')[1]
    json = InitialData(url)
    yield J(J(json,'co'),'rt')
