import requests
import json
import math
import csv
import os

from professor import Professor
# This code has been tested using Python 3.6 interpreter and Linux (Ubuntu).
# It should run under Windows, if anything you may need to make some adjustments for the file paths of the CSV files.


class ProfessorNotFound(Exception):
    def __init__(self, search_argument, search_parameter: str = "Name"):

        # What the client is looking for. Ex: "Professor Pattis"
        self.search_argument = self.search_argument

        # The search criteria. Ex: Last Name
        self.search_parameter = search_parameter

    def __str__(self):

        return (
            f"Proessor not found"
            + f" The search argument {self.search_argument} did not"
            + f" match with any professor's {self.search_parameter}"
        )


class RateMyProfApi:
    def __init__(self, school_id: str = "1074", testing: bool = False):
        self.UniversityId = school_id
        if not os.path.exists("SchoolID_" + str(self.UniversityId)):
            os.mkdir("SchoolID_" + str(self.UniversityId))

        # dict of Professor
        self.professors= self.scrape_professors(testing)
        self.indexnumber = False
    
    def get_professor_list(self):
        return self.professors

    def scrape_professors(
        self,
        testing: bool = False
    ):  # creates List object that include basic information on all Professors from the IDed University
        professors = dict()
        num_of_prof = self.get_num_of_professors(self.UniversityId)
        num_of_pages = math.ceil(num_of_prof / 20)

        for i in range(1, num_of_pages + 1):  # the loop insert all professor into list
            page = requests.get(
                "http://www.ratemyprofessors.com/search/professor/?&page="
                + str(i)
                + "&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid="
                + str(self.UniversityId)
            )
            json_response = json.loads(page.content)
            temp_list = json_response["professors"]


            for json_professor in json_response["professors"]:
                print(json_professor)
                professor = professor = Professor(
                    json_professor["tid"],
                    json_professor["tFname"],
                    json_professor["tLname"],
                    json_professor["tNumRatings"],
                    json_professor["overall_rating"],
                    tDept=json_professor.get("tDept"),
                    tSid=json_professor.get("tSid"),
                    institution_name=json_professor.get("institution_name"),
                    tMiddlename=json_professor.get("tMiddlename"),
                    rating_class=json_professor.get("rating_class"),
                    contentType=json_professor.get("contentType"),
                    categoryType=json_professor.get("categoryType")
                )

                professors[professor.tid] = professor

            # for test cases, limit to 2 iterations
            if testing and (i > 1): break

        return professors

    def get_num_of_professors(
        self, id
    ):  # function returns the number of professors in the university of the given ID.
        page = requests.get(
            "http://www.ratemyprofessors.com/filter/professor/?&page=1&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid="
            + str(id)
        )  # get request for page
        temp_jsonpage = json.loads(page.content)
        num_of_prof = (
            temp_jsonpage["remaining"] + 20
        )  # get the number of professors at William Paterson University
        return num_of_prof

    # def search_professor(self, ProfessorName):
    #     self.indexnumber = self.get_professor_index(ProfessorName)
    #     self.print_professor_info()
    #     return self.indexnumber



    def get_professor_by_last_name(
        self, last_name
    ) -> Professor:
        '''
        Return the first professor with the matching last name.
        Case insenstive.
        '''
        last_name = last_name.lower()
        for name in professors:
            if last_name == professors[name].last_name.lower():
                return professors[name]

        # Raise error if no matching professor found
        raise ProfessorNotFound(last_name, "Last Name")


    def WriteProfessorListToCSV(self):
        csv_columns = [
            "tDept",
            "tSid",
            "institution_name",
            "tFname",
            "tMiddlename",
            "tLname",
            "tid",
            "tNumRatings",
            "rating_class",
            "contentType",
            "categoryType",
            "overall_rating"
        ]

        csv_file = "SchoolID_" + str(self.UniversityId) + ".csv"
        with open(csv_file, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            print('*'*30)
            print(self.professors)
            print('*'*30)
            for professor_id, professor in self.professors.items():
                writer.writerow(professor.to_dict())

    def create_reviews_list(self, tid):

        def add_tid_to_dicts(dict_list, tid_value):
            return [{**d, "tid": tid_value} for d in dict_list]
        
        tempreviewslist = []
        num_of_reviews = self.get_num_of_reviews(tid)
        # RMP only loads 20 reviews per page,
        # so num_of_pages tells us how many pages we need to get all the reviews
        num_of_pages = math.ceil(num_of_reviews / 20)
        i = 1
        while i <= num_of_pages:
            page = requests.get(
                "https://www.ratemyprofessors.com/paginate/professors/ratings?tid="
                + str(tid)
                + "&filter=&courseCode=&page="
                + str(i)
            )
            temp_jsonpage = json.loads(page.content)
            temp_list = temp_jsonpage["ratings"]
            tempreviewslist.extend(temp_list)
            i += 1
        
        tempreviewslist = add_tid_to_dicts(tempreviewslist, tid)

        return tempreviewslist
    
    def create_reviews_list_for_all(self):
        all_reviews_for_all_profs = []
        for professor_id, professor in self.professors.items():
            all_reviews_for_all_profs.extend(self.create_reviews_list(professor_id))
        
        return all_reviews_for_all_profs


    def get_num_of_reviews(self, id):
        page = requests.get(
            "https://www.ratemyprofessors.com/paginate/professors/ratings?tid="
            + str(id)
            + "&filter=&courseCode=&page=1"
        )
        num_of_reviews=0
        if page.content:
            temp_jsonpage = json.loads(page.content)
            num_of_reviews = temp_jsonpage["remaining"] + 20
        else:
            print("Empty response received for: "+id)
        
        return num_of_reviews

    def WriteReviewsListToCSV(self, rlist):
        csv_columns = [
            "tid",
            "attendance",
            "clarityColor",
            "easyColor",
            "helpColor",
            "helpCount",
            "id",
            "notHelpCount",
            "onlineClass",
            "quality",
            "rClarity",
            "rClass",
            "rComments",
            "rDate",
            "rEasy",
            "rEasyString",
            "rErrorMsg",
            "rHelpful",
            "rInterest",
            "rOverall",
            "rOverallString",
            "rStatus",
            "rTextBookUse",
            "rTimestamp",
            "rWouldTakeAgain",
            "sId",
            "takenForCredit",
            "teacher",
            "teacherGrade",
            "teacherRatingTags",
            "unUsefulGrouping",
            "usefulGrouping",
        ]
        csv_file = (
            "./SchoolID_" + str(self.UniversityId) + "_reviews.csv"
        )
        with open(csv_file, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in rlist:
                writer.writerow(data)


# Time for some examples!
if __name__ == '__main__':

    # Getting general professor info!
    # uci = RateMyProfApi(1074)


    # uci.search_professor("Pattis")
    # uci.print_professor_detail("overall_rating")
    
    # MassInstTech = RateMyProfApi(580)
    # MassInstTech.search_professor("Robert Berwick")
    # MassInstTech.print_professor_detail("overall_rating")

    # Let's try the above class out to get data from a number of schools!
    # William Patterson, Case Western, University of Chicago, CMU, Princeton, Yale, MIT, UTexas at Austin, Duke, Stanford, Rice, Tufts
    # For simple test, try tid 97904 at school 1205


    #schools = [278,298,675,1331,960,971,795,957,958,807,1325,4115,842,1223,992,1519,240,4070,413,747,389,82,252,563,883,453,1045,412,1223,907,970,6,240,847,527,4441,1053,973,228,398]
    schools = [883]
    for school in schools:
        print("=== Processing School " + str(school) + " ===")
        rmps = RateMyProfApi(school, False)
        rmps.WriteProfessorListToCSV()
        professors = rmps.get_professor_list()
        print(len(professors))
        # reviewList = rmps.create_reviews_list_for_all()
        # rmps.WriteReviewsListToCSV(reviewList)
        # print(len(reviewList))

