edurepo
=======

Project to create a master repository of educational materials, including descriptions and outlines for standard courses

See the docs for more background information.

## Requirements for an initial prototype

### Repository

1. Store models
2. Store materials for the various models.
3. Provide queue for additions or replacements, with approval and rejection capabilities.

### Models

E.g., the form of a glossary item, or the form of a course description

The prototype should contain models for a course description as well as models for several types of educational materials.

*It isn't important that the models be editable at this time, though they should be considered part of what the repository stores rather than something static.*

Include a model that is a generator.  For example, a model for single digit multiplication problems doesn't require actual data to be stored; it can generate the appropriate additional problems dynamically.  Contrast that with a word problem, which requires a human to generate the problems.

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

Show reuse of course materials by third-party software.

1. Create a simple JavaScript library that can be included in a mock course web page that automatically displays a few sample problems of the type currently being used in the class.
2. Create a very basic version (rough copy) of an existing web-based quiz generator (printed and web-based quizzes) which allows a teacher to reuse educational materials in the repository (e.g., specify a collection of glossary terms) instead of reentering the data.
3. Provide reference Python code for each model illustrating retrieval and use of an item or collection from the repository.

