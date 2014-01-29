edurepo
=======

Project to create a master repository of educational data, including descriptions and outlines for standard courses as well as a rich set of materials

See docs subdirectory for more background information.

## Requirements for an initial prototype

An initial prototype is required to illustrate the key concepts and allow a greater number of people to evaluate the usefulness.

### Repository

1. Store models
2. Store materials for the various models.

#### Not required at this stage

1. Provide queue for additions or replacements, with approval and rejection capabilities.

#### Repository users

At this stage, only superusers and anonymous access will be supported.

* Superusers can make any modifications to the repository.
* Anonymous access is sufficient to retrieve data from the repository.

### Models

E.g., the form of a glossary item, or the form of a course description, or the form of a certain type of math problem, or ...

The prototype should contain models for a course description as well as models for several types of educational materials.

*It isn't important that the models be editable at this time, though the models should be considered part of what the repository stores rather than something static.*

"Generator" models should be supported.  For example, a model for single digit multiplication problems doesn't require actual data to be stored, because the repository (or even client software) can generate the appropriate multiplication problems dynamically.  Contrast that with a word problem, which requires a human to generate the problems.

Note that generators may have very detailed constraints, such as would be required for students learning multiplication facts up through 5, or subtraction of single-digit numbers that __does__ allow negative numbers.  It is very valuable to have the constraints on generated problems stored in the repository.  (Why?  Look at all the math problem generators on the web that require you to respecify those constraints before creating the quiz/worksheet/test/whatever.)

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

1. Provide simple views of the contents of the repository, accessible by course description.
2. Provide a simple quiz capability that can quiz a user on several types of data associated with a lesson.

### Third-party consumption

Show examples of possible reuse of course materials by third-party software via REST API.

1. Create a simple JavaScript library that can be included in a mock course web page that automatically displays a few sample problems or definitions or ... of the type currently being taught in the course.  (That is a very down to earth way to describe to parents what the class is doing.)
2. Create a very basic version (rough hack) of some existing web-based quiz generator (printed and/or web-based quizzes) which allows a teacher to reuse educational materials in the repository (e.g., specify a collection of glossary terms) instead of reentering the data.
3. If practical, create a simple Android or iOS app which can reuse the materials.

*Showing disparate means of consumption will be important for allowing a wide audience to see the usefulness of the repository.*

### Reference code

Each model should have corresponding *reference* Python code illustrating retrieval and use of an item or collection from the repository.
