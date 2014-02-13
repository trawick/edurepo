__author__ = 'trawick'

from repo.models import Course, LearningObjective, GlossaryItem


c = Course(id='LIAMSAX01', description='private tutoring from Liam Trawick')
c.save()

lo1 = c.learningobjective_set.create(id='LSC0001', formal_description='how to put it together, how to clean it, how to store it', simple_description='zzz')
lo2 = c.learningobjective_set.create(id='LSC0002', formal_description='proper embouchure, making a full sound', simple_description='zzz')
lo3 = c.learningobjective_set.create(id='LSC0002', formal_description='how to read music', simple_description='zzz')

lo1.glossaryitem_set.create(term='ligature', definition='holds reed to mouthpiece')
lo3.glossaryitem_set.create(term='fingering chart', definition='shows you what notes go with what fingering')
lo1.glossaryitem_set.create(term='saxophone', definition='miracle of metal')
