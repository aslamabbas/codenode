import uuid

from django.contrib.auth.models import User

from codenode.frontend.notebook import models
from codenode.frontend.notebook import views


# this stores fixture data
f = {}


def setup():
    f['user1'] = User.objects.get(username__exact='test')
    f['user2'] = User.objects.get(username__exact='test2')

def teardown():
    f = {}


def test_a_new_notebook_is_assigned_a_guid():
    nb = models.Notebook(owner=f['user1'])
    nb.save()
    assert nb.guid is not None
    

def test_adding_a_cell_to_a_notebook_updates_the_last_modified_time():
    nb = models.Notebook(owner=f['user1'])
    nb.save()
    first_time = nb.last_modified_time()
    
    print nb.created_time
    
    cell = models.Cell(
        guid=str(uuid.uuid4()).replace("-", ""), 
        notebook=nb,
        owner=nb.owner
        )
    cell.save()
    
    print nb.cell_set.all()
    print cell.last_modified
    
    second_time = nb.last_modified_time()
    assert second_time > first_time
    

def test_notebook_last_modified_by_returns_last_cell_modifier():
    nb = models.Notebook(owner=f['user1'])
    nb.save()
    assert nb.last_modified_by() == f['user1']
    
    cell = models.Cell(
        guid=str(uuid.uuid4()).replace("-", ""), 
        notebook=nb,
        owner=f['user2']
        )
    cell.save()
    assert nb.last_modified_by() == f['user2']
    
    