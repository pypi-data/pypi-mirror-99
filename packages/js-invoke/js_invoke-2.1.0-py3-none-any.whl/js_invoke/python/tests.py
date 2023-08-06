# -*- coding: utf-8 -*-
# pylint: disable=bad-continuation

"""
Invoke tasks for Python development.

Copyright ©  2018 Justin Stout <justin@jstout.us>

"""
from pathlib import Path

from invoke import task


def _get_pkg_dir(ctx):
    return 'src/{}'.format(ctx.python.pkg_name)


def _get_test_dir(ctx):
    return '{}/tests'.format(_get_pkg_dir(ctx))


def _run_pytest(ctx, test_dir):
    if Path(test_dir).is_dir():
        cmd = 'PYTHONPATH={PKG_DIR} pytest {TEST_DIR}'.format(
                PKG_DIR=_get_pkg_dir(ctx),
                TEST_DIR=test_dir
                )

        ctx.run(cmd)


@task()
def test_pylint_errors(ctx):
    """Run pylint errors-only."""
    print('Run pylint errors-only')

    cmd = 'PYTHONPATH={PKG_DIR} /usr/local/bin/pylint --errors-only {PKG_DIR}/{PKG_NAME}'.format(
        PKG_DIR=_get_pkg_dir(ctx),
        PKG_NAME=ctx.python.pkg_name
        )
    ctx.run(cmd)


@task()
def test_pylint(ctx):
    """Run pylint style test."""
    print('Run pylint linter')

    options = '--disable=duplicate-code'

    cmd = 'PYTHONPATH={PKG_DIR} /usr/local/bin/pylint {OPTIONS} {PKG_DIR}/{PKG_NAME}'.format(
        OPTIONS=options,
        PKG_DIR=_get_pkg_dir(ctx),
        PKG_NAME=ctx.python.pkg_name
        )
    ctx.run(cmd)


@task()
def test_codestyle(ctx):
    """Run pycodestyle (pep8) tests."""
    print('Run pycodestyle linter')
    cmd = '/usr/local/bin/pycodestyle --max-line-length=120 {PKG_DIR}'.format(
        PKG_DIR=_get_pkg_dir(ctx)
        )
    ctx.run(cmd)


@task()
def test_docstyle(ctx):
    """Run pydocstyle test."""
    print('Run pydocstyle linter')
    cmd = '/usr/local/bin/pydocstyle {PKG_DIR}'.format(PKG_DIR=_get_pkg_dir(ctx))
    ctx.run(cmd)


@task
def test_unit(ctx):
    """Run unit tests."""
    _run_pytest(ctx, '{}/unit'.format(_get_test_dir(ctx)))


@task
def test_integration(ctx):
    """Run integration tests."""
    _run_pytest(ctx, '{}/integration'.format(_get_test_dir(ctx)))


@task
def test_regression(ctx):
    """Run regression tests."""
    _run_pytest(ctx, '{}/regression'.format(_get_test_dir(ctx)))


@task
def test_refactor(ctx):
    """Run pylint duplicate code checker."""
    print('Run duplicate code checker')

    options = (
        '--disable=all',
        '--enable=duplicate-code'
        )

    cmd = 'PYTHONPATH={PKG_DIR} /usr/local/bin/pylint {OPTIONS} {PKG_DIR}/{PKG_NAME}'.format(
        OPTIONS=' '.join(options),
        PKG_DIR=_get_pkg_dir(ctx),
        PKG_NAME=ctx.python.pkg_name
        )
    ctx.run(cmd)


@task
def test_tox(ctx):
    """Run test in tox environment."""
    with ctx.cd('{PKG_DIR}'.format(PKG_DIR=_get_pkg_dir(ctx))):
        ctx.run('/usr/local/bin/tox')
