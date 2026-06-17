from http import HTTPStatus

import factory
import factory.fuzzy
import pytest

from fast_zero_async.models import Todo, TodoState

factory.Faker._DEFAULT_LOCALE = 'pt_BR'


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


def test_create_todo(client, token, mock_db_time):
    with mock_db_time(model=Todo) as times:
        response = client.post(
            '/todos',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'title': 'Test Todo',
                'description': 'Test description',
                'state': 'draft',
            },
        )

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            'id': 1,
            'title': 'Test Todo',
            'description': 'Test description',
            'state': 'draft',
            'created_at': times[0].isoformat(),
            'updated_at': times[0].isoformat(),
        }


@pytest.mark.asyncio
async def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_pagination_should_return_2_todos(
    session, client, user, token
):
    expected_todos = 2
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todos?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_title_should_return_5_todos(
    session, client, user, token
):
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, title='Test todo 1')
    )
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todos?title=Test todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_description_should_return_5_todos(
    session, client, user, token
):
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, description='Test todo 1')
    )
    session.add_all(TodoFactory.create_batch(5, user_id=user.id))
    await session.commit()

    response = client.get(
        '/todos?description=Test todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_list_todos_filter_state_should_return_5_todos(
    session, client, user, token
):
    expected_todos = 5
    session.add_all(
        TodoFactory.create_batch(5, user_id=user.id, state='draft')
    )
    await session.commit()

    response = client.get(
        '/todos?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_read_todo(session, client, user, token, mock_db_time):
    with mock_db_time(model=Todo) as times:
        todo = TodoFactory(user_id=user.id)
        session.add(todo)
        await session.commit()

        response = client.get(
            '/todos/',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == HTTPStatus.OK
        responsed_todo = response.json()['todos'][0]
        assert len(response.json()['todos']) == 1
        assert responsed_todo['title'] == todo.title
        assert responsed_todo['description'] == todo.description
        assert responsed_todo['state'] == todo.state
        assert responsed_todo['created_at'] == times[0].isoformat()
        assert responsed_todo['updated_at'] == times[0].isoformat()
        assert responsed_todo['id'] == todo.id


@pytest.mark.asyncio
async def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    await session.commit()
    await session.refresh(todo)

    response = client.delete(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task has been deleted successfully'}


def test_delete_todo_error(client, token):
    response = client.delete(
        '/todos/100',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


@pytest.mark.asyncio
async def test_delete_other_user_todo(
    session, client, user, other_user, token
):
    todo_user = TodoFactory(user_id=user.id)
    todo_other_user = TodoFactory(user_id=other_user.id)
    session.add_all([todo_user, todo_other_user])

    await session.commit()
    response = client.delete(
        f'/todos/{todo_other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


def test_patch_todo_error(client, token):
    response = client.patch(
        '/todos/100', headers={'Authorization': f'Bearer {token}'}, json={}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


@pytest.mark.asyncio
async def test_patch_other_user_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    await session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'teste!'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'teste!'
