import nox

nox.options.sessions = ['lint', 'mypy', 'test']
nox.options.reuse_existing_virtualenvs = True


@nox.session
def lint(session: nox.Session) -> None:
    session.install('pre-commit')
    session.run('pre-commit', 'run', '--all-files')


@nox.session
def mypy(session: nox.Session) -> None:
    pyproject = nox.project.load_toml('pyproject.toml')
    session.install(*nox.project.dependency_groups(pyproject, 'mypy', 'test'))
    session.run('mypy', *session.posargs)


@nox.session
def test(session: nox.Session) -> None:
    session.install('tox', 'tox-uv')
    session.run('tox', 'run-parallel', *session.posargs)
