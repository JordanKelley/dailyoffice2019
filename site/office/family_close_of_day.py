import datetime

from django.utils.functional import cached_property
from django.utils.safestring import mark_safe

from office.canticles import EP2
from office.compline import ComplinePrayers
from office.evening_prayer import EPInvitatory, EPCommemorationListing, EPReading2, EPCollectsOfTheDay, EPCollects
from office.morning_prayer import MPCommemorationListing
from office.offices import Office, OfficeSection
from psalter.utils import get_psalms


class FamilyCloseOfDay(Office):

    name = "Family Prayer at the Close of Day"
    office = "family_close_of_day_prayer"

    start_time = "8:00 PM"

    family = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = "Office: {}, Date: {}, Commemoration: {}, Prayer Book: {}".format(
            self.name,
            self.get_formatted_date_string(),
            self.date.primary_evening.name,
            "The Book of Common Prayer (2019), Anglican Church in North America",
        )

        self.start_time = datetime.datetime.combine(self.date.date, datetime.time())
        self.start_time = self.start_time.replace(minute=0, hour=16, second=0)
        self.end_time = self.start_time.replace(minute=59, hour=23, second=59)

        self.start_time = datetime.datetime.combine(self.date.date, datetime.time())
        self.start_time = self.start_time.replace(minute=0, hour=16, second=0)
        self.end_time = self.start_time.replace(minute=59, hour=23, second=59)

    @cached_property
    def modules(self):
        return [
            (FCDHeading(self.date), "office/heading.html"),
            (EPCommemorationListing(self.date), "office/commemoration_listing.html"),
            (FCDOpeningSentence(self.date, self.office_readings), "office/opening_sentence.html"),
            (FCDPsalms(self.date, self.office_readings), "office/minor_office_psalms.html"),
            (FCDScripture(self.date, self.office_readings), "office/family_scripture.html"),
            (Pater(self.date, self.office_readings), "office/family_lords_prayer.html"),
            (FCDCollect(self.date, self.office_readings), "office/family_collect.html"),
            (FCDNunc(self.date, self.office_readings), "office/simple_canticle.html"),
            (FCDClosingSentence(self.date, self.office_readings), "office/opening_sentence.html"),
        ]


class FCDHeading(OfficeSection):
    @cached_property
    def data(self):
        return {"heading": mark_safe("Family Prayer<br>at the Close of Day"), "calendar_date": self.date}


class FCDOpeningSentence(OfficeSection):
    def get_sentence(self):
        return {
            "sentence": "I will lay me down in peace, and take my rest; for you, LORD, only, make me dwell in safety.",
            "citation": "PSALM 4:8",
        }

    @cached_property
    def data(self):
        return {"heading": "Opening Sentence", "sentence": self.get_sentence()}


class FCDPsalms(OfficeSection):
    @cached_property
    def data(self):
        return {"heading": "The Psalm", "psalms": get_psalms("134")}


class FCDScripture(OfficeSection):
    def get_scripture(self):

        day_of_year = self.date.date.timetuple().tm_yday
        number = day_of_year % 2

        scriptures = [
            {
                "sentence": "You keep them in perfect peace whose minds are stayed on you, because they trust in you. Trust in the LORD for ever, for the LORD God is an everlasting rock.",
                "citation": "ISAIAH 26:3-4",
            },
            {
                "sentence": "Now may the God of peace himself sanctify you completely, and may your whole spirit and soul and body be kept blameless at the coming of our Lord Jesus Christ.",
                "citation": "1 THESSALONIANS 5:23",
            },
        ]

        return scriptures[number]

    @cached_property
    def data(self):
        ep_reading = EPReading2(self.date, self.office_readings)
        return {
            "heading": "A READING FROM HOLY SCRIPTURE",
            "long": ep_reading.data,
            "brief": self.get_scripture(),
            "hide_closing": True,
        }


class Pater(OfficeSection):
    @cached_property
    def data(self):
        return {"heading": "The Lord's Prayer"}


class FCDCollect(OfficeSection):
    def get_day_of_week_collect(self):
        collects = ComplinePrayers.collects
        number = self.date.date.weekday()
        if number == 4:
            number = 5
        elif number == 5:
            number = 4
        collect = collects[number]
        return (collect[0], None, collect[1])

    @cached_property
    def data(self):

        day_of_year = next(EPCollectsOfTheDay(self.date, self.office_readings).data["collects"])
        day_of_week = self.get_day_of_week_collect()

        return {
            "heading": "The Collect",
            "time_of_day": "Visit this place, O Lord, and drive far from it all snares of the enemy; let your holy angels dwell with us to preserve us in peace; and let your blessing be upon us always; through Jesus Christ our Lord.",
            "day_of_year": day_of_year,
            "day_of_week": day_of_week,
        }


class FCDNunc(OfficeSection):
    @cached_property
    def data(self):
        return EP2


class FCDClosingSentence(OfficeSection):
    def get_sentence(self):
        return {
            "sentence": "The almighty and merciful Lord, Father, Son, and Holy Spirit, bless us and keep us, this night and evermore.",
            "citation": "PSALM 4:8",
        }

    @cached_property
    def data(self):
        return {"heading": "Closing Sentence", "sentence": self.get_sentence()}
