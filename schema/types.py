import datetime


class Segment:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description


class PlacerSalesPerson:
    def __init__(self, name: str, cellphone: str, email: str) -> None:
        self.name = name
        self.cellphone = cellphone
        self.email = email


class Company:
    def __init__(self, name: str, website: str, description: str, relevancyscore: int, searchid: int, segmentid: int) -> None:
        self.name = name
        self.website = website
        self.description = description
        self.relevancyscore = relevancyscore
        self.searchid = searchid
        self.segmentid = segmentid


class Search:
    def __init__(self, source: str, searchterm: str, searchdate: datetime, results: str) -> None:
        self.source = source
        self.searchterm = searchterm
        self.searchdate = searchdate
        self.results = results


class LeadPerson:
    def __init__(self, name: str, title: str, email: str, workphone: str, cellphone: str, locationid: int, companyid: int, placersalesperson: int) -> None:
        self.name = name
        self.title = title
        self.email = email
        self.workphone = workphone
        self.cellphone = cellphone
        self.locationid = locationid
        self.companyid = companyid
        self.placersalesperson = placersalesperson


class Location:
    def __init__(self, address: str, city: str, state: str, postalcode: str, pobox: str, country: str, hours: str, companyid: int) -> None:
        self.address = address
        self.city = city
        self.state = state
        self.postalcode = postalcode
        self.pobox = pobox
        self.country = country
        self.hours = hours
        self.companyid = companyid
