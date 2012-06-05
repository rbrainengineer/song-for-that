from xml.dom.minidom import parse

def parseSenticNet(filename='senticnet-1.0/senticnet.rdf.xml'):
    senticDict = {}
    dom = parse(filename)
    textNodes = dom.getElementsByTagName('text')
    polarNodes = dom.getElementsByTagName('polarity')
    for t, p in zip(textNodes, polarNodes):
        concept = t.childNodes[0].nodeValue.encode('ascii').lower()
        senticDict[concept] = p.childNodes[0].nodeValue
    return senticDict
