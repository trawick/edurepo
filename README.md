edurepo
=======

Project to create a master repository of educational data, including descriptions and outlines for standard courses as well as a rich set of materials

See docs subdirectory for more background information.

## Requirements for an initial prototype

An initial prototype is required to illustrate the key concepts and allow a greater number of people to evaluate the usefulness of the idea.  More specifically, the prototype should show that

* Collaboration is possible initially and there are clear paths for making collaboration easy for non-technical users.
* The data can be stored using existing technologies.
* A wide variety of educational materials can be stored.
* The data can be accessed easily enough by client software that it can be integrated into existing resources as well as exploited by software specifically designed to rely on the repository for materials.

### Repository

1. Store models
2. Store materials for the various models.

#### Not required at this stage

1. Provide queue for additions or replacements, with approval and rejection capabilities.

#### Repository users

At this stage, only superusers and anonymous access will be supported.

* Superusers can make any modifications to the repository.
* Anonymous access is sufficient to retrieve data from the repository.

#### Possible implementation

A version control system (e.g., git) gives us the collaboration and history mechanisms for free.  A database is needed for read access and searching.  All data is represented in a text file and recent changes will be loaded into the database at intervals (e.g., every hour if not on demand).

### Models

E.g., the form of a glossary item, or the form of a course description, or the form of a certain type of math problem, or ...

The prototype should contain models for a course description as well as models for several types of educational materials.  A couple of "generator" models should be supported as well.

*It isn't important that the models be editable at this time, though the models should be considered part of what the repository stores rather than something static.*

### Materials

This is data that fits some model.

Initial data should include a course description and data for several types of models that is associated with the course description.

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
2. Create a very basic version (rough hack) of an existing web-based quiz generator (printed and/or web-based quizzes) which allows a teacher to reuse educational materials in the repository (e.g., specify a collection of glossary terms) instead of reentering the data.
3. If practical, create a simple Android or iOS app which can reuse the materials.

### Reference code

Each model should have corresponding *reference* Python code illustrating retrieval and use of an item or collection from the repository.
