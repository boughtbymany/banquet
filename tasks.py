from invoke import task


@task
def test_static(c, fix=False):
    if fix:
        c.run("black .", echo=True)
        c.run("isort .", echo=True)

    c.run("black --check .", echo=True)
    c.run("isort . --check --diff", echo=True)


@task
def test_unit(c, tb=False):
    if tb:
        c.run("pytest")
    else:
        c.run("pytest --tb=no")
