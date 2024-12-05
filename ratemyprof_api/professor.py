
class Professor:
    def __init__(self, tid, tFname, tLname, tNumRatings, overall_rating, tDept=None, tSid=None, institution_name=None, tMiddlename=None, rating_class=None, contentType=None, categoryType=None):
        self.tid = tid
        self.tFname = tFname
        self.tLname = tLname
        self.tNumRatings = tNumRatings
        if self.tNumRatings < 1:
            self.overall_rating = 0

        else:
            self.overall_rating = float(overall_rating)
        self.tDept = tDept
        self.tSid = tSid
        self.institution_name = institution_name
        self.tMiddlename = tMiddlename
        self.rating_class = rating_class
        self.contentType = contentType
        self.categoryType = categoryType

    def to_dict(self):
        return {
            "tDept": self.tDept,
            "tSid": self.tSid,
            "institution_name": self.institution_name,
            "tFname": self.tFname,
            "tMiddlename": self.tMiddlename,
            "tLname": self.tLname,
            "tid": self.tid,
            "tNumRatings": self.tNumRatings,
            "rating_class": self.rating_class,
            "contentType": self.contentType,
            "categoryType": self.categoryType,
            "overall_rating": self.overall_rating
        }
