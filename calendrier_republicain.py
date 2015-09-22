#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
Daniel Clerc <mail@clerc.eu> - 2014-09-03
Translates the current date and time to date and time in Calendrier républicain
see: http://fr.wikipedia.org/wiki/Calendrier_r%C3%A9publicain
"""

from datetime import datetime
from datetime import date
import json

def heure_republicain():
    timeobj = datetime.now()
    dec_sec_of_day = (timeobj.hour * 3600 + timeobj.minute * 60 + timeobj.second) / 0.864
    dec_hours = dec_sec_of_day / 10000
    dec_minutes = (dec_sec_of_day - int(dec_hours) * 10000) / 100
    dec_seconds = ((dec_sec_of_day - int(dec_hours) * 10000) - int(dec_minutes) * 100)
    return (int(dec_hours), int(dec_minutes), int(dec_seconds))

def date_republicain():
    today=date.today()
    """
    for reference:
    -Mois d'automne (terminaison en aire)
    Vendémiaire (22 septembre ~ 21 octobre) - Période des vendanges
    Brumaire (22 octobre ~ 20 novembre) - Période des brumes et des brouillards
    Frimaire (21 novembre ~ 20 décembre) - Période des froids (frimas)
    -Mois d'hiver (terminaison en ose à l'origine, abusivement orthographiée ôse par la suite)
    Nivôse (21 décembre ~ 19 janvier) - Période de la neige
    Pluviôse (20 janvier ~ 18 février) - Période des pluies
    Ventôse (19 février ~ 20 mars) - Période des vents
    -Mois du printemps (terminaison en al)
    Germinal (21 mars ~ 19 avril) - Période de la germination
    Floréal (20 avril ~ 19 mai) - Période de l'épanouissement des fleurs
    Prairial (20 mai ~ 18 juin) - Période des récoltes des prairies
    -Mois d'été (terminaison en idor)
    Messidor (19 juin ~ 18 juillet) - Période des moissons
    Thermidor (19 juillet ~ 17 août) - Période des chaleurs
    Fructidor (18 août ~ 16 septembre) - Période des fruits
    """
    mois = ((u"Vendémiaire", (22, 9, 21, 10)),
            (u"Brumaire", (22, 10, 20, 11)),
            (u"Frimaire", (21, 11, 20, 12)),
            (u"Nivôse", (21, 12, 19, 1)),
            (u"Pluviôse", (20, 1, 18, 2)),
            (u"Ventôse", (19, 2, 20, 3)),
            (u"Germinal", (21, 3, 19, 4)),
            (u"Floréal", (20, 4, 19, 5)),
            (u"Prairial", (20, 5, 18, 6)),
            (u"Messidor", (19, 6, 18, 7)),
            (u"Thermidor", (19, 7, 17, 8)),
            (u"Fructidor", (18, 8, 16, 9)),
            (u"complementaire", (17,9,22,9)))

    complementaires = ["Jour de la vertu", "Jour du génie", "Jour du travail", "Jour de l'opinion", "Jour des récompenses", "Jour de la révolution"]


    input_file  = file("jours.json", "r")
    jours = json.loads(input_file.read(), 'utf-8')

    def current_year(today=today):
    # FIXME: the year start on the 22nd of september each year
        year = today.year - 1792
        if today.month >= 9 and today.day >= 22:
            year = year + 1
        return year
    def in_mois((start_day, start_month, end_day, end_month), today=today):

        """
        if today is in between start and end date return day of month,
        else return 0
        """
        start_date = date(today.year, start_month, start_day)
        #Afin de prendre en compte un mois à cheval sur deux années
        if(start_month > end_month):
            start_date = date(today.year-1, start_month, start_day)
        end_date = date(today.year, end_month, end_day)
        if today >= start_date and today <= end_date:
            return (today - start_date).days + 1

        return 0
    # just indices to access the tuple of tuples easier, ugly but they do the job:

    date_range = 1
    name = 0

    for m in mois:
        day_of_month = in_mois(m[date_range])
        if day_of_month != 0:
            if m[name] == "complementaire":
                day = complementaires[day_of_month-1]
                numbername = "e"
                if day_of_month == 1:
                    numbername = "er"
                return day_of_month.__str__()+numbername, "jour complémentaire de l'année", current_year(), day
            else:
                day = jours[m[name]][day_of_month-1]
                return day_of_month.__str__(), m[name], current_year(), day.encode('utf8', 'replace')
def main():
    print "%s %s %d, %s" % date_republicain() + " %02d:%02d:%02d" % heure_republicain()

def getStr():
    return "%s %s %d, %s" % date_republicain() + " %02d:%02d:%02d" % heure_republicain()


if __name__ == '__main__':
    main()
