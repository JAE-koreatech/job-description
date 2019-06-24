# Smart-Career Scraper v1.3


## Changelog v1.3:
### Additions:
+ Integration with the 2 new scripts.
+ Date Captured works for get_jobs, but not get_people not sure why.
+ Input is now automatic, to change, refer to the cfg.txt file.
  The first line is for the job title, the second line is period,
  the third and fourth lines are username and password respectively.
### Changes:
+ Config file changed to accomodate for login ID and password (Slots 2 and 3)
+ Period is now daily by default.
+ Script runs as long as it needs to, no hard limit unless I need to test.
### Removals:
+ The 2 old scripts, which have been replaced by these new ones.

## Changelog v1.2:
### Additions:
+ Added direct upload of any job description to MongoDB (and fixed weird issues with it)
+ Now ignores duplicates when adding data.
+ Added a config file where the first line = job description and second line = period
### Changes:
+ No longer takes user input. Use config file instead.
### Removals:
+ None

## Changelog v1.1:
### Additions:
+ Added direct upload of any job description to MongoDB
+ Filters results to past week only.
+ Added some comments to help understand code.
### Changes:
+ Changed hard limit to 100 job descriptions to A. Test and B. Avoid stalling.
+ Currently testing getting rid of duplicates.
### Removals (Just commented out):
+ Got rid of period selection as we are focusing on past week for now.

## Changelog v1.0:
+ Initial scraper
