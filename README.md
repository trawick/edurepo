edurepo
=======

**See the text at http://edjective.org/ for a better song and dance.  There are a number of use cases of the system
and I change my mind from time to time about which use cases are more valuable or should be stressed to a particular
audience.**

# Project to create a master repository of educational data, including descriptions and outlines for standard courses as well as a rich set of materials

See docs subdirectory for more background information.

## Requirements for an initial prototype of the repository

An initial prototype is required to illustrate the key concepts and allow a greater number of people to evaluate the usefulness of the idea.  More specifically, the prototype should show that

* The data can be stored using existing technologies.
* Collaboration is possible initially and there are clear paths for making collaboration easy for non-technical users.
* A variety of educational materials can be stored.
* The data can be easily accessed by client software, to illustrate the feasibility of exploitation
of the data by third-party software.

### Repository

1. Store models (*conceptually*; models might be hard-coded into the
repository software at this sage)
2. Store materials for the various models.
3. Provide machine-readable access.

#### Repository users

* Users who edit the repository data will be able to make any modifications.
(Fine-grained access will be implemented in the future.)  These users will
need to create a user id.
* Anyone can retrieve data from the repository, either in source form or from
the database (machine-readable format).

#### Initial implementation

Github.com will be used to store the raw data initially, and anyone with a free
github id can be granted access to edit the data.  At github, the data will be
represented in plain text files with a relatively easy to understand format.
(In the future, specialized software can be provided to more easily create and
update these text files.)  Github/git gives us the collaboration and history 
mechanisms for free.  (In the future, specialized software can provide a
simpler interface to the collaboration mechanisms.)

Data validation software will be provided alongside the data in the git 
repository; before committing changes the software will ensure that it is
in the proper format.  (Future specialized editing software will remove most
errors.)

A database is needed for read access to the data, including searching.  At
intervals, recent modifications to the git repository will be loaded into the
database in a machine-readable format (generally JSON, but possibly XML for
some models).

### Models

E.g., the form of a glossary item, or the form of a course description, or the form of a certain type of math problem, or ...

The prototype should contain models for a course description as well as models for several types of educational materials.  A couple of "generator" models should be supported as well.

It isn't important that the models be separately represented and editable
at this time, though the models should be considered part of what the 
repository stores rather than something static.  Eventually the validation
software should be able to read a representation of the model but at this
stage the supported models will be hard-coded in the validation script.

### Materials

This is data that fits some model.

Initial data should include a course description and data for several types of 
educational materials which are associated with the course description.

### Material collections

As an example, consider a bank of 500 glossary terms associated with a high school biology course.  A default collection would be the entire bank of terms, but other types of collections are necessary.

#### Static collections

A teacher should be able to define and name a custom collection of glossary items that pertain to a particular unit.

*The goal would be to have predefined collections corresponding to a typical unit that most teachers would use as-is, with custom collections covering the materials for a particular teacher's test or mid-term exam.*

#### Dynamic collections

Client software should be able to access a randomly chosen subset of some type of material (e.g., word problem), with the size of the subset (e.g., number of problems) specified by the client software.

### Repository views

At a minimum, the a web site associated with the repository must provide reference views in order for the data to be audited.  It should provide some more meaningful ways to consume the data as an interim step until third-party software can consume the data.

1. Provide simple views of the contents of the repository, accessible by course description.  Data should be represented in an appropriate manner according to the corresponding model.
2. Provide a simple quiz capability that can quiz a user on several types of data associated with a lesson.

### Third-party consumption

Show examples of possible reuse of course materials by third-party software via REST API.  *Showing disparate means of consumption is very important for showing the practical impact of a common repository.*

1. Create a simple JavaScript library that can be included in a mock course web page that automatically displays a few sample math problems or definitions or other materials of the type currently being taught in the course.  (That is a very down to earth way to describe to parents what the class is doing.)
In the prototype the teacher must specify the learning objective explicitly, though 
theoretically the JavaScript code could consult a calendar maintained by the
teacher to find the learning objective automatically.
2. Create a very basic version (rough hack) of an existing web-based quiz generator (printed and/or web-based quizzes) which allows a teacher to reuse educational materials in the repository (e.g., specify a collection of glossary terms) instead of reentering the data.
3. Create a mobile web side which can reuse the materials to administer a practice quiz for a
student.

### Reference code

Each model should have corresponding *reference* Python code illustrating retrieval and use of an item or collection from the repository
using only the Python standard library.
