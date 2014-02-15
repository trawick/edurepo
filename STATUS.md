Current Status
==============

As of January 29, I've been thinking about this for a couple of weeks, talked over the ideas with a family member who teaches
in a college of education, written up a couple of ideas (see docs subdirectory), and shared them with a colleague
of that family member who has experience in this area.

Next steps: Determine a set of features for an initial prototype (see README.md), implement it.  Look for existing
resources with similar capabilities.

Next stage
==========

"Learning objective" client takes teacher id and date and class as input, retrieves learning objective(s) for closest date <= input date, retrieves statement for objective(s), displays.

* TODO add REST API for teacher events to retrieve current classes for teacher
* TODO add REST API for teacher events to retrieve learning objective(s) for class for date
* TODO add REST API for learning objective to retrieve statement
* TODO reference client in Python to glue it together
* TODO web page to take teacher id as input and allow selection of course and date range of interest and retrieve learning objectives and display description of each objective