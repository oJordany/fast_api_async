from dataclasses import asdict

from sqlalchemy import select

from fast_zero_async.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as times:
        new_user = User(
            username='test',
            email='test@test',
            password='teste',
        )

        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.username == 'test'))

        assert asdict(user) == {
            'id': 1,
            'username': 'test',
            'email': 'test@test',
            'password': 'teste',
            'created_at': times[0],
            'updated_at': times[0],
        }


def test_update_user(session, mock_db_time):
    with mock_db_time(model=User) as times:
        new_user = User(
            username='test',
            email='test@test',
            password='teste',
        )

        session.add(new_user)
        session.commit()

        user_created = session.scalar(
            select(User).where(User.username == 'test')
        )

        assert asdict(user_created) == {
            'id': 1,
            'username': 'test',
            'email': 'test@test',
            'password': 'teste',
            'created_at': times[0],
            'updated_at': times[0],
        }

        user_created.username = 'jordany'
        session.commit()

        user_updated = session.scalar(
            select(User).where(User.username == 'jordany')
        )

        assert asdict(user_updated) == {
            'id': 1,
            'username': 'jordany',
            'email': 'test@test',
            'password': 'teste',
            'created_at': times[0],
            'updated_at': times[1],
        }
